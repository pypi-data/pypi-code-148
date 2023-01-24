"""A test case for the path utils module"""
import logging
import unittest

from lost_cat_images.utils.utils_shapes import Rectangle, ShapeGrouper, intersect, merge, contains

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG
file_handler = logging.FileHandler("logs/test_shapes.log")
logger.addHandler(file_handler)

class TestShapes(unittest.TestCase):
    """A container class for the build path modeule test cases"""

    def test_rect_interset(self):
        """test the intersection"""
        rect1 = Rectangle(1,1,2,2)  # 3,3
        rect2 = Rectangle(2,2,2,2)  # 4,4
        rect3 = Rectangle(4,4,2,2)  # 6,6

        self.assertTrue(intersect(rect1, rect2), msg="Rectangle do overlap!")
        self.assertFalse(intersect(rect1,rect3), msg="Rectangle don't overlap!")

    def test_vars(self):
        """test that the data call works"""
        rect1 = Rectangle(1,1,1,1)
        tags = {
            "id": 0,
            "contours": [[1,2],[3,4]]
        }
        rect1.add_tags(**tags)

        data = rect1.data()
        for key,value in data.items():
            logger.info("\t%s: %s", key ,value)

    def test_rect_merge(self):
        """Test merging rectangles"""
        rect1 = Rectangle(1,1,2,2)  # 3,3
        rect2 = Rectangle(2,2,2,2)  # 4,4

        rect3 = merge(rect1, rect2)
        self.assertTrue(rect3.x == 1 and rect3.y == 1 and \
                rect3.w == 3 and rect3.h == 3, msg="Merge failed!")

    def test_rect_interset_border(self):
        """Test the intersect with a border set"""
        rect1 = Rectangle(1,1,2,2)  # 3,3
        rect2 = Rectangle(5,5,2,2)  # 6,6

        self.assertFalse(intersect(rect1,rect2), msg="Rectangle don't overlap!")
        self.assertFalse(intersect(rect1,rect2, 1), msg="Rectangle don't overlap!")
        self.assertTrue(intersect(rect1, rect2, 2), msg="Rectangle do overlap!")

    def test_shapes(self):
        """Test the shape heirarchy, currently contains only"""
        rect1 = Rectangle(1,1,15,15)
        rect2 = Rectangle(2,2,4,4)
        rect3 = Rectangle(14,14,3,3)

        self.assertTrue(contains(rect1, rect2), msg=f"{rect1} should contain {rect2}")
        self.assertFalse(contains(rect1, rect3), msg=f"{rect1} should not contain {rect3}")

        shpg = ShapeGrouper()
        shpg.add_rectangle(rect1)
        shpg.add_rectangle(rect2)
        shpg.add_rectangle(rect3)

        logger.info(shpg.shapes)
