# KITTI Reference: https://docs.nvidia.com/tao/archive/tlt-20/tlt-user-guide/text/preparing_data_input.html

import json
import logging
import re
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, cast

import cv2
import numpy as np
import pandas as pd
from encord import Project as EncordProject
from encord.objects.common import Shape
from encord.objects.ontology_object import Object
from encord.objects.ontology_structure import OntologyStructure
from pandas.errors import EmptyDataError
from PIL import Image
from tqdm.auto import tqdm

from encord_active.lib.model_predictions.writer import PredictionWriter
from encord_active.lib.project import Project

logger = logging.getLogger(__name__)
KITTI_COLUMNS = [
    ("class_name", str),
    ("truncation", float),  # [0, 1]
    ("occlusion", int),  # [0, 3], [ 0 = fully visible, 1 = partly visible, 2 = largely occluded, 3 = unknown]
    ("alpha", float),  # [-pi, pi]
    # bbox
    ("xmin", float),  # [0, img_width]
    ("ymin", float),  # [0, img_height]
    ("xmax", float),  # [0, img_width]
    ("ymax", float),  # [0, img_height]
    # 3-D dimensions (in meters
    ("height", float),
    ("width", float),
    ("length", float),
    # 3-D object location x, y, z in camera coordinates (in meters)
    ("location_x", float),
    ("location_y", float),
    ("location_z", float),
    # Rotation ry around the Y-axis in camera coordinates
    ("rotation_y", float),  # [-pi, pi]
]

KITTI_FILE_NAME_REGEX = r"^(?P<data_hash>[a-f0-9\-]*)__(?P<image_name>.*)$"
PNG_FILE_NAME_REGEX = r"^(?P<stem>.*?)\.png$"


def import_mask_predictions(
    project: EncordProject,
    data_root: Path,
    cache_dir: Path,
    prediction_writer: PredictionWriter,
    class_map: Optional[Dict[str, int]] = None,
    file_name_regex: str = PNG_FILE_NAME_REGEX,
    du_hash_name_lookup: Callable[[Path], Tuple[str, int]] = None,
):
    """
    Will look for mask
    :param project: The project for which to which the predictions are associated
    :param data_root: The root folder of the segmentation masks
    :param cache_dir: The cache directory of the (potentially) cached label rows, images, etc.
    :param prediction_writer: The writer to store the predictions with.
    :param class_map: A Dictionary which contains ``(featureNodeHash, class_idx)`` pairs, such that if
        a pixel in a mask has value 1 and corresponds to ``featureNodeHash == "abcdef01``, then
        ``class_map["abcdef01"] == 1``.
        If the ``class_map`` is not specified, it will be generated by::

            polygon_classes = sorted({
                    o for o in OntologyStructure.from_dict(project.ontology).objects if o.shape == Shape.POLYGON
                },
                key=lambda x: int(x.id)
            )
            {o.feature_node_hash: i+1 for o in enumerate(polygon_classes) if o.shape == "polygon"}

    :param file_name_regex: A regex pattern to match annotation masks. As default, all pngs in the `data_root`
        will be considered as predictions. Example strings that are matched are::

            "/path/to/data_root/masks/some_name.png"
            "/path/to/data_root/some_name.png"

    :param du_hash_name_lookup: A transform ``f(file_path) -> (data_unit_hash: str, frame: int)`` to translate between
        data units and their associated mask file names. You can omit this argument if you

            #. Store masks with identical filenames to the uploaded files.
            #. (only required for videos) append a frame number for video predictions with two under scores.

        For example, if you have predictions for the video ``my_video.mp4``, then you should store prediction masks as
        ``my_video__0.png``, ``my_video__1.png``, etc.

        If you, on the other hand, store files with other naming conventions, we need to be able to match files with
        specific data units (and frames if videos). For example, you may store predictions in folder structures like::

            predictions
            ├── 00115807-3206-4301-b513-026de3f2015e  # data unit hash
            │   ├── 0.png  # Frame number.
            │   └── 1.png
            └── 001722b8-1624-4169-bb11-5977127dcea9
                ├── 0.png
                └── 1.png

        You will then need to specify a lambda function like the following::

            du_hash_name_lookup = lambda file_pth: (file_pth.parent.name, int(file_pth.name))


    """
    label_rows = Project(cache_dir).from_encord_project(project).label_rows
    du_hash_lookup: Dict[str, Tuple[str, int]] = {}

    if not class_map:
        ontology = OntologyStructure.from_dict(project.ontology)
        ontology_polygons: List[Object] = [o for o in ontology.objects if o.shape == Shape.POLYGON]
        class_map = {o.feature_node_hash: i + 1 for i, o in enumerate(ontology_polygons)}

    ontology_hash_lookup: Dict[int, str] = {v: k for k, v in class_map.items()}

    if du_hash_name_lookup is None:
        du_hash_lookup = {}
        for label_row in label_rows.values():
            for du in label_row["data_units"].values():
                fname = du["data_title"].rsplit(".", 1)[0]  # File name without the extension
                if isinstance(du["labels"], list):  # Videos
                    for frame_num in du["labels"]:
                        du_hash_lookup[f"{fname}__{frame_num:05d}"] = du["data_hash"], int(frame_num)
                else:  # Images
                    du_hash_lookup[fname] = du["data_hash"], 0

    queue = [data_root]
    with tqdm(total=None, desc="Importing masks", leave=False) as pbar:
        while queue:
            pth = queue.pop()
            if pth.is_dir():
                queue += list(pth.iterdir())
                continue
            elif pth.is_file():
                match = re.match(file_name_regex, pth.as_posix())
                if not match:
                    continue

                if du_hash_name_lookup:
                    du_hash, frame = du_hash_name_lookup(pth)
                else:
                    du_hash, frame = du_hash_lookup.get(pth.stem, ("", -1))

                if not du_hash:
                    logger.warning(f"Couldn't match file {pth} to any data unit.")
                    continue

                try:
                    input_mask = np.array(Image.open(pth))
                except Exception:
                    continue
                for cls in np.unique(input_mask):
                    if cls == 0:  # background
                        continue

                    class_hash = ontology_hash_lookup[cls]

                    mask = np.zeros_like(input_mask)
                    mask[input_mask == cls] = 1

                    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

                    for contour in contours:
                        if len(contour) < 3 or cv2.contourArea(contour) < 4:
                            continue
                        _mask = np.zeros_like(mask)
                        _mask = cv2.fillPoly(_mask, [contour], 1)

                        prediction_writer.add_prediction(du_hash, class_hash, confidence_score=1.0, polygon=_mask)

                pbar.update(1)


def import_KITTI_labels(
    project: EncordProject,
    data_root: Path,
    prediction_writer: PredictionWriter,
    file_name_regex: str = KITTI_FILE_NAME_REGEX,
):

    label_files = [f for f in (data_root / "labels").iterdir() if f.suffix == ".txt"]

    # === Prepare ontology lookup === #
    with (data_root / "ontology_label_map.json").open("r", encoding="utf-8") as f:
        label_name_map = json.load(f)

    object_name_to_hash = {
        o["name"]: o["featureNodeHash"] for o in project.ontology["objects"] if o["shape"] == "bounding_box"
    }
    hash_lookup: Dict[str, Optional[str]] = {v: object_name_to_hash.get(k) for k, v in label_name_map.items()}

    for file in tqdm(label_files, desc="Importing label files"):
        match = re.match(file_name_regex, file.name)
        if not match:
            logger.info(f"Couldn't match file {file.name} to specified regex")
            continue

        data_hash, image_name = match.groups()
        try:
            df = pd.read_csv(file, sep=" ", header=None)
        except EmptyDataError:
            continue

        headers = list(map(lambda x: x[0], KITTI_COLUMNS))
        # Hack to account for additional "custom" columns
        headers += [f"undefined{i}" for i in range(df.shape[1] - len(headers))]
        df.columns = headers

        for _, row in df.iterrows():
            class_name = cast(str, hash_lookup[row["class_name"]])
            bbox = {
                "x": row["xmin"],
                "y": row["ymin"],
                "w": row["xmax"] - row["xmin"],
                "h": row["ymax"] - row["ymin"],
            }
            conf = row["undefined0"]
            prediction_writer.add_prediction(data_hash, class_name, confidence_score=conf, bbox=bbox)
