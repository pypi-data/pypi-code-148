
def bounding_box(bbox, *args):
    """
    Preset Bounding Box
    :param bbox: list()
    :param args: dict()
    :return:  dict()
    """
    tmp_json = dict()

    tmp_json["annotation"] = "BOX"

    tmp_json["object"] = dict()
    tmp_json["object"]["left"] = bbox[0]
    tmp_json["object"]["top"] = bbox[1]
    tmp_json["object"]["width"] = bbox[2] - bbox[0]
    tmp_json["object"]["height"] = bbox[3] - bbox[1]
    tmp_json["object"]["angle"] = 0
    if len(args) != 0:
        tmp_json.update(args[0])

    return tmp_json

def polygon(point, *args, annotation_type="POLYGONS"):
    """
    Preset Segmentation type
    :param point: list()
    :param annotation_type: default --> POLYGONS
    :param args: dict()
    :return: dict()
    """
    tmp_json = dict()

    tmp_json["annotation"] = annotation_type

    tmp_json["points"] = list()
    for i in range(int(len(point)/2)):
        tmp_json["points"].append({"x": point[2*i],"y": point[2*i+1]})

    if len(args) != 0:
        tmp_json.update(args[0])

    return tmp_json


def keypoint(point, *args):
    tmp_json = dict()

    tmp_json["annotation"] = "DOTS"

    tmp_json["points"] = list()
    tmp_json["hiddens"] = list()
    # tmp_json["disables"] = list()

    for i in range(int(len(point) / 3)):
        tmp_json["points"].append({"x": point[3 * i], "y": point[3 * i + 1]})
        tmp_json["hiddens"].append(True if point[3 * i + 2] == 1 else False)
        # tmp_json["disables"].append(True if polygon[3*i+2]==2 else False)

    if len(args) != 0:
        tmp_json.update(args[0])

    return tmp_json

def yolo_to_bbox(yolo_bbox, size):
    w, h = size
    center_x = float(yolo_bbox[1])
    center_y = float(yolo_bbox[2])
    relative_width = float(yolo_bbox[3])
    relative_height = float(yolo_bbox[4])
    
    width = relative_width * w
    height = relative_height * h
    
    x = center_x * w - (width / 2)
    y = center_y * h - (height / 2)
    
    return [x, y, width + x, height + y]
