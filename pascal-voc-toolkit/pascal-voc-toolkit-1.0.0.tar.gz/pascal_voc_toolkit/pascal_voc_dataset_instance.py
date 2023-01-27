import pathlib

from .image_handler import ImageHandler
from .xml_handler import XmlHandler


class PascalVocDatasetInstance:
    def __init__(self, image_file_path: pathlib.Path, annotation_file_path: pathlib.Path) -> None:
        self.image_file_path = image_file_path
        self.annotation_file_path = annotation_file_path

        if not self.image_file_path.exists():
            raise Exception(f"Specified image file does not exist: {self.image_file_path}")

        if not self.annotation_file_path.exists():
            raise Exception(f"Specified annotation file does not exist: {self.annotation_file_path}")

        self.xml_handler = XmlHandler(self.annotation_file_path)
        self.image_handler = ImageHandler(self.image_file_path)
