import pathlib

import pytest

from pascal_voc_toolkit import XmlHandler


# Pytest naming convention needs Test to prepend in class name
class TestXmlHandler:
    """
    Xml handler test class
    """

    def setup_class(self):
        """
        This will run once before test cases are run
        """
        self.current_file_path = pathlib.Path(__file__).resolve().parent
        self.invalid_file_path = pathlib.Path(
            self.current_file_path / "./res/invalid.xml")
        self.no_object_xml_file_path = pathlib.Path(
            self.current_file_path / "./res/no_annotated_object.xml")
        self.single_object_xml_file_path = pathlib.Path(
            self.current_file_path / "./res/single_annotated_object.xml")
        self.multiple_objects_xml_file_path = pathlib.Path(
            self.current_file_path / "./res/multiple_annotated_objects.xml")

    def test_xml_file_exists(self):
        """
        Test to check file existence
        """
        # Valid object
        XmlHandler(self.multiple_objects_xml_file_path)

        # Should throw exception for invalid file path
        with pytest.raises(Exception) as e_info:
            XmlHandler(self.invalid_file_path)

    def test_bounding_boxes_count_0(self):
        """
        Test case to check bounding boxes count for XML file with no object
        """
        no_object_xml_handler = XmlHandler(self.no_object_xml_file_path)
        assert no_object_xml_handler.get_bounding_boxes_count() == 0

    def test_bounding_boxes_count_1(self):
        """
        Test case to check bounding boxes count for XML file with single object
        """
        single_object_xml_handler = XmlHandler(self.single_object_xml_file_path)
        assert single_object_xml_handler.get_bounding_boxes_count() == 1

    def test_bounding_boxes_count_2(self):
        """
        Test case to check bounding boxes count for XML file with multiple objects
        """
        multiple_objects_xml_handler = XmlHandler(self.multiple_objects_xml_file_path)
        assert multiple_objects_xml_handler.get_bounding_boxes_count() == 87

    def test_xml_file_name_with_ext_0(self):
        """
        Test case to check file name including extension
        """
        xml_handler = XmlHandler(self.no_object_xml_file_path)
        assert xml_handler.get_xml_file_name(include_extension=True) == "no_annotated_object.xml"

    def test_xml_file_name_with_ext_1(self):
        """
        Test case to check file name including extension without passing any argument
        """
        xml_handler = XmlHandler(self.no_object_xml_file_path)
        assert xml_handler.get_xml_file_name() == "no_annotated_object.xml"

    def test_xml_file_name_without_ext(self):
        """
        Test case to check file name excuding extension
        """
        xml_handler = XmlHandler(self.no_object_xml_file_path)
        assert xml_handler.get_xml_file_name(include_extension=False) == "no_annotated_object"

    def test_annotation_classes_details_0(self):
        """
        Test case to check annotation classes details in XML file with no annotation boxes
        """
        xml_handler = XmlHandler(self.no_object_xml_file_path)
        annotated_class_details = xml_handler.get_annotation_classes_details()

        # Should be an empty dictionary
        # bool({}) will return False
        assert isinstance(annotated_class_details, dict)
        assert not bool(annotated_class_details)

    def test_annotation_classes_details_1(self):
        """
        Test case to check annotation classes details in XML file with single annotation boxes
        """
        expected_output_dict = {
            "person": 1
        }

        xml_handler = XmlHandler(self.single_object_xml_file_path)
        available_classes = xml_handler.get_annotation_classes_details()
        assert expected_output_dict == available_classes

    def test_annotation_classes_details_2(self):
        """
        Test case to check annotation classes details in XML file with multiple annotation boxes
        """
        expected_output_dict = {
            "person": 24,
            "small_vehicle": 13,
            "person_occluded_visible": 2,
            "heavy_vehicle": 48
        }

        xml_handler = XmlHandler(self.multiple_objects_xml_file_path)
        available_classes = xml_handler.get_annotation_classes_details()
        assert expected_output_dict == available_classes

    def test_bbox_coordinates_0(self):
        """
        Test case to check bounding box coordinates in XML file with no annotation boxes
        """
        xml_handler = XmlHandler(self.no_object_xml_file_path)
        bbox_details = xml_handler.get_all_bbox_coordinates_list()

        # The list should be empty
        assert isinstance(bbox_details, list)
        assert len(bbox_details) == 0

    def test_bbox_coordinates_1(self):
        """
        Test case to check bounding box coordinates in XML file with single annotation box
        """
        expected_output = [[676, 418, 693, 454, 'person']]

        xml_handler = XmlHandler(self.single_object_xml_file_path)
        bbox_details = xml_handler.get_all_bbox_coordinates_list()
        assert isinstance(bbox_details, list)
        assert expected_output == bbox_details

    def test_bbox_coordinates_2(self):
        """
        Test case to check bounding box coordinates in XML file with multiple annotation boxes
        """
        expected_output = [[651, 647, 673, 707, 'person'], [673, 651, 696, 703, 'person'],
                           [714, 450, 733, 483, 'person'],
                           [718, 467, 732, 498, 'small_vehicle'], [654, 370, 664, 393, 'person'],
                           [644, 364, 654, 391, 'person'],
                           [645, 365, 654, 382, 'person_occluded_visible'], [653, 354, 664, 385, 'person'],
                           [653, 354, 664, 373, 'person_occluded_visible'], [577, 204, 585, 220, 'person'],
                           [692, 180, 700, 197, 'person'],
                           [699, 127, 705, 139, 'person'], [904, 128, 914, 144, 'person'],
                           [1015, 156, 1024, 176, 'person'],
                           [121, 672, 147, 718, 'person'], [388, 686, 549, 761, 'heavy_vehicle'],
                           [428, 629, 556, 695, 'heavy_vehicle'],
                           [450, 566, 585, 643, 'heavy_vehicle'], [582, 581, 671, 692, 'heavy_vehicle'],
                           [604, 483, 661, 569, 'heavy_vehicle'],
                           [611, 443, 692, 500, 'heavy_vehicle'], [607, 390, 660, 444, 'heavy_vehicle'],
                           [469, 404, 518, 477, 'heavy_vehicle'],
                           [422, 310, 489, 348, 'heavy_vehicle'], [723, 282, 756, 324, 'heavy_vehicle'],
                           [740, 388, 787, 449, 'heavy_vehicle'],
                           [988, 464, 1054, 538, 'heavy_vehicle'], [1025, 549, 1101, 637, 'heavy_vehicle'],
                           [1063, 670, 1149, 765, 'heavy_vehicle'], [1136, 437, 1205, 494, 'heavy_vehicle'],
                           [1091, 370, 1162, 433, 'heavy_vehicle'], [1145, 333, 1235, 368, 'heavy_vehicle'],
                           [1122, 307, 1207, 340, 'heavy_vehicle'], [1101, 273, 1145, 310, 'heavy_vehicle'],
                           [895, 273, 929, 310, 'heavy_vehicle'], [871, 240, 909, 269, 'heavy_vehicle'],
                           [865, 184, 921, 209, 'heavy_vehicle'],
                           [950, 168, 1000, 191, 'heavy_vehicle'], [938, 161, 984, 180, 'heavy_vehicle'],
                           [914, 129, 959, 150, 'heavy_vehicle'],
                           [928, 119, 968, 139, 'heavy_vehicle'], [871, 103, 912, 120, 'heavy_vehicle'],
                           [648, 266, 677, 306, 'heavy_vehicle'],
                           [617, 241, 671, 272, 'heavy_vehicle'], [658, 195, 683, 223, 'heavy_vehicle'],
                           [726, 218, 752, 254, 'heavy_vehicle'],
                           [760, 139, 779, 158, 'heavy_vehicle'], [760, 126, 781, 142, 'heavy_vehicle'],
                           [797, 150, 819, 172, 'heavy_vehicle'],
                           [790, 129, 813, 149, 'heavy_vehicle'], [843, 158, 869, 187, 'heavy_vehicle'],
                           [731, 80, 766, 94, 'heavy_vehicle'],
                           [716, 49, 730, 68, 'heavy_vehicle'], [706, 71, 737, 90, 'heavy_vehicle'],
                           [487, 220, 557, 248, 'heavy_vehicle'],
                           [490, 211, 546, 232, 'heavy_vehicle'], [496, 196, 550, 222, 'heavy_vehicle'],
                           [505, 188, 558, 210, 'heavy_vehicle'],
                           [508, 181, 564, 204, 'heavy_vehicle'], [515, 170, 568, 194, 'heavy_vehicle'],
                           [529, 166, 578, 188, 'heavy_vehicle'],
                           [553, 119, 578, 147, 'heavy_vehicle'], [665, 142, 686, 166, 'heavy_vehicle'],
                           [186, 634, 236, 663, 'small_vehicle'],
                           [211, 608, 267, 642, 'small_vehicle'], [206, 561, 244, 606, 'small_vehicle'],
                           [326, 426, 361, 457, 'small_vehicle'],
                           [341, 411, 374, 435, 'small_vehicle'], [351, 386, 394, 412, 'small_vehicle'],
                           [376, 378, 405, 404, 'small_vehicle'],
                           [375, 360, 403, 384, 'small_vehicle'], [389, 350, 421, 368, 'small_vehicle'],
                           [429, 289, 457, 310, 'small_vehicle'],
                           [439, 279, 467, 294, 'small_vehicle'], [1089, 234, 1102, 254, 'small_vehicle'],
                           [375, 299, 386, 332, 'person'],
                           [384, 307, 396, 340, 'person'], [402, 312, 416, 344, 'person'],
                           [527, 144, 533, 158, 'person'],
                           [864, 244, 874, 268, 'person'], [854, 244, 867, 272, 'person'],
                           [870, 295, 888, 318, 'person'],
                           [725, 124, 733, 138, 'person'], [739, 110, 746, 125, 'person'],
                           [720, 97, 726, 109, 'person'],
                           [750, 111, 756, 124, 'person'], [706, 62, 712, 75, 'person']]

        xml_handler = XmlHandler(self.multiple_objects_xml_file_path)
        bbox_details = xml_handler.get_all_bbox_coordinates_list()
        assert isinstance(bbox_details, list)
        assert expected_output == bbox_details

    def test_update_bbox_coordinates_1(self):
        """
        Test case to check updating bounding box coordinates functionality in
        XML file with single annotation box
        """
        new_coordinates = [[647, 389, 664, 425, 'person_standing']]

        xml_handler = XmlHandler(self.single_object_xml_file_path)
        xml_handler.update_all_bounding_box_coordinates(new_coordinates)
        bbox_coordinates = xml_handler.get_all_bbox_coordinates_list()
        assert bbox_coordinates == new_coordinates

    def test_update_bbox_coordinates_2(self):
        """
        Test case to check updating bounding box coordinates functionality in
        XML file with multiple annotation boxes
        """
        new_coordinates = [[651, 647, 673, 707, 'person'], [673, 651, 696, 703, 'person'],
                           [714, 450, 733, 483, 'person'],
                           [718, 467, 732, 498, 'small_vehicle'], [654, 370, 664, 393, 'person'],
                           [644, 364, 654, 391, 'person'],
                           [645, 365, 654, 382, 'person_occluded_visible'], [653, 354, 664, 385, 'person'],
                           [653, 354, 664, 373, 'person_occluded_visible'], [577, 204, 585, 220, 'person'],
                           [692, 180, 700, 197, 'person'],
                           [699, 127, 705, 139, 'person'], [904, 128, 914, 144, 'person'],
                           [1015, 156, 1024, 176, 'person'],
                           [121, 672, 147, 718, 'person'], [342, 640, 503, 715, 'car'],
                           [428, 629, 556, 695, 'heavy_vehicle'],
                           [450, 566, 585, 643, 'heavy_vehicle'], [582, 581, 671, 692, 'heavy_vehicle'],
                           [604, 483, 661, 569, 'heavy_vehicle'],
                           [611, 443, 692, 500, 'heavy_vehicle'], [607, 390, 660, 444, 'heavy_vehicle'],
                           [469, 404, 518, 477, 'heavy_vehicle'],
                           [422, 310, 489, 348, 'heavy_vehicle'], [723, 282, 756, 324, 'heavy_vehicle'],
                           [740, 388, 787, 449, 'heavy_vehicle'],
                           [988, 464, 1054, 538, 'heavy_vehicle'], [1025, 549, 1101, 637, 'heavy_vehicle'],
                           [1063, 670, 1149, 765, 'heavy_vehicle'], [1136, 437, 1205, 494, 'heavy_vehicle'],
                           [1091, 370, 1162, 433, 'heavy_vehicle'], [1145, 333, 1235, 368, 'heavy_vehicle'],
                           [1122, 307, 1207, 340, 'heavy_vehicle'], [1101, 273, 1145, 310, 'heavy_vehicle'],
                           [895, 273, 929, 310, 'heavy_vehicle'], [871, 240, 909, 269, 'heavy_vehicle'],
                           [865, 184, 921, 209, 'heavy_vehicle'],
                           [950, 168, 1000, 191, 'heavy_vehicle'], [938, 161, 984, 180, 'heavy_vehicle'],
                           [914, 129, 959, 150, 'heavy_vehicle'],
                           [928, 119, 968, 139, 'heavy_vehicle'], [871, 103, 912, 120, 'heavy_vehicle'],
                           [648, 266, 677, 306, 'heavy_vehicle'],
                           [617, 241, 671, 272, 'heavy_vehicle'], [658, 195, 683, 223, 'heavy_vehicle'],
                           [726, 218, 752, 254, 'heavy_vehicle'],
                           [760, 139, 779, 158, 'heavy_vehicle'], [760, 126, 781, 142, 'heavy_vehicle'],
                           [797, 150, 819, 172, 'heavy_vehicle'],
                           [790, 129, 813, 149, 'heavy_vehicle'], [843, 158, 869, 187, 'heavy_vehicle'],
                           [731, 80, 766, 94, 'heavy_vehicle'],
                           [716, 49, 730, 68, 'heavy_vehicle'], [706, 71, 737, 90, 'heavy_vehicle'],
                           [487, 220, 557, 248, 'heavy_vehicle'],
                           [490, 211, 546, 232, 'heavy_vehicle'], [496, 196, 550, 222, 'heavy_vehicle'],
                           [505, 188, 558, 210, 'heavy_vehicle'],
                           [508, 181, 564, 204, 'heavy_vehicle'], [515, 170, 568, 194, 'heavy_vehicle'],
                           [529, 166, 578, 188, 'heavy_vehicle'],
                           [553, 119, 578, 147, 'heavy_vehicle'], [665, 142, 686, 166, 'heavy_vehicle'],
                           [186, 634, 236, 663, 'small_vehicle'],
                           [211, 608, 267, 642, 'small_vehicle'], [206, 561, 244, 606, 'small_vehicle'],
                           [326, 426, 361, 457, 'small_vehicle'],
                           [341, 411, 374, 435, 'small_vehicle'], [351, 386, 394, 412, 'small_vehicle'],
                           [376, 378, 405, 404, 'small_vehicle'],
                           [375, 360, 403, 384, 'small_vehicle'], [389, 350, 421, 368, 'small_vehicle'],
                           [429, 289, 457, 310, 'small_vehicle'],
                           [439, 279, 467, 294, 'small_vehicle'], [1089, 234, 1102, 254, 'small_vehicle'],
                           [375, 299, 386, 332, 'person'],
                           [384, 307, 396, 340, 'person'], [402, 312, 416, 344, 'person'],
                           [481, 98, 487, 112, 'person_sitting'],
                           [864, 244, 874, 268, 'person'], [854, 244, 867, 272, 'person'],
                           [870, 295, 888, 318, 'person'],
                           [725, 124, 733, 138, 'person'], [739, 110, 746, 125, 'person'],
                           [720, 97, 726, 109, 'person'],
                           [750, 111, 756, 124, 'person'], [706, 62, 712, 75, 'person']]

        xml_handler = XmlHandler(self.multiple_objects_xml_file_path)
        xml_handler.update_all_bounding_box_coordinates(new_coordinates)
        bbox_coordinates = xml_handler.get_all_bbox_coordinates_list()
        assert bbox_coordinates == new_coordinates

    def test_remove_class_1(self):
        """
        Test case to check removing classes functionality in XML file
        having single annotation box
        """
        expected_output = []
        xml_handler = XmlHandler(self.single_object_xml_file_path)
        xml_handler.remove_class(["person"])
        bbox_details = xml_handler.get_all_bbox_coordinates_list()
        assert bbox_details == expected_output

    def test_remove_classes_2(self):
        """
        Test case to check removing classes functionality in XML file
        having multiple annotation boxes
        """
        expected_output = [[651, 647, 673, 707, 'person'], [673, 651, 696, 703, 'person'],
                           [714, 450, 733, 483, 'person'],
                           [654, 370, 664, 393, 'person'], [644, 364, 654, 391, 'person'],
                           [645, 365, 654, 382, 'person_occluded_visible'],
                           [653, 354, 664, 385, 'person'], [653, 354, 664, 373, 'person_occluded_visible'],
                           [577, 204, 585, 220, 'person'],
                           [692, 180, 700, 197, 'person'], [699, 127, 705, 139, 'person'],
                           [904, 128, 914, 144, 'person'],
                           [1015, 156, 1024, 176, 'person'], [121, 672, 147, 718, 'person'],
                           [375, 299, 386, 332, 'person'],
                           [384, 307, 396, 340, 'person'], [402, 312, 416, 344, 'person'],
                           [527, 144, 533, 158, 'person'],
                           [864, 244, 874, 268, 'person'], [854, 244, 867, 272, 'person'],
                           [870, 295, 888, 318, 'person'],
                           [725, 124, 733, 138, 'person'], [739, 110, 746, 125, 'person'],
                           [720, 97, 726, 109, 'person'],
                           [750, 111, 756, 124, 'person'], [706, 62, 712, 75, 'person']]
        xml_handler = XmlHandler(self.multiple_objects_xml_file_path)
        xml_handler.remove_class(["small_vehicle", "heavy_vehicle"])
        bbox_coordinates = xml_handler.get_all_bbox_coordinates_list()
        assert bbox_coordinates == expected_output

    def test_save_file(self):
        """
        Test case to check file saving functionality
        """
        xml_file_path = pathlib.Path(
            self.current_file_path / "./res/multiple_annotated_objects.xml")

        output_directory = self.current_file_path / "generated"
        output_directory.mkdir(parents=True, exist_ok=True)
        output_file_path = output_directory / "output.xml"

        xml_handler = XmlHandler(xml_file_path)
        xml_handler.save_xml_file(str(output_file_path))
        assert output_file_path.exists()

        # Cleaning up
        output_file_path.unlink()
        output_directory.rmdir()
