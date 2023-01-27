import pathlib

from .pascal_voc_dataset_instance import PascalVocDatasetInstance


class PascalVocDataset:
    def __init__(self, image_dir_path: str, annotation_dir_path: str, image_file_format: str = ".jpg",
                 annotation_file_format: str = ".xml") -> None:
        self.image_dir_path: pathlib.Path = pathlib.Path(image_dir_path)
        self.annotation_dir_path: pathlib.Path = pathlib.Path(annotation_dir_path)
        self.image_file_format: str = image_file_format
        self.annotation_file_format: str = annotation_file_format

        # Check directories existence
        if not self.image_dir_path.exists():
            raise Exception(f"Specified image directory does not exist: {self.image_dir_path}")

        if not self.annotation_dir_path.exists():
            raise Exception(f"Specified annotation directory does not exist: {self.annotation_dir_path}")

        # Loading images and annotations
        self.image_files: list[pathlib.Path] = self._load_images()
        self.annotation_files: list[pathlib.Path] = self._load_annotations()
        self.dataset_instances: list[PascalVocDatasetInstance] = self.get_dataset_instances()

    def _load_images(self) -> list[pathlib.Path]:
        """
        Load images from the specified images directory
        """
        image_name_pattern: str = f"*{self.image_file_format}"
        return list(self.image_dir_path.glob(image_name_pattern))

    def _load_annotations(self) -> list[pathlib.Path]:
        """
        Load annotations from the specified annotations directory
        """
        annotation_name_pattern: str = f"*{self.annotation_file_format}"
        return list(self.annotation_dir_path.glob(annotation_name_pattern))

    def get_dataset_instances(self) -> list[PascalVocDatasetInstance]:
        """
        A list of PascalVocDatasetInstance which contains image and annotation file

        Returns:
            [ PascalVocDatasetInstance, ... ]
        """
        dataset_instances: list[PascalVocDatasetInstance] = []

        for image_file_path in self.image_files:
            image_name_without_extension = image_file_path.stem
            annotation_file_path = self.annotation_dir_path / (image_name_without_extension +
                                                               self.annotation_file_format)
            if annotation_file_path in self.annotation_files:
                dataset_instances.append(PascalVocDatasetInstance(image_file_path, annotation_file_path))
        return dataset_instances

    def get_labels(self) -> dict:
        labels: dict = {}
        count = 1
        for dataset_instance in self.dataset_instances:
            file_labels = dataset_instance.xml_handler.get_annotation_classes_details()
            for key, val in file_labels.items():
                if key in labels:
                    labels[key] += val
                else:
                    labels[key] = val
            print(f"Processing: {count} / {len(self.dataset_instances)}", end="\r")
            count += 1
        return labels

    def remove_labels(self, labels_to_remove: list[str]) -> None:
        count = 1
        for dataset_instance in self.dataset_instances:
            dataset_instance.xml_handler.remove_class(labels_to_remove)
            print(f"Processing: {count} / {len(self.dataset_instances)}", end="\r")
            count += 1

    def save_labels(self, output_directory: str = "output") -> None:
        # Creating output directory if not exists
        output_directory_path = pathlib.Path(output_directory)
        output_directory_path.mkdir(exist_ok=True, parents=True)

        count = 1
        for dataset_instance in self.dataset_instances:
            annotation_file_name = dataset_instance.xml_handler.get_xml_file_name(include_extension=True)
            dataset_instance.xml_handler.save_xml_file(output_directory_path / annotation_file_name)
            print(f"Processing: {count} / {len(self.dataset_instances)}", end="\r")
            count += 1
