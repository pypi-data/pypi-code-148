"""A test case for the path utils module"""
import logging
import glob
import os
import sys
import unittest

from lost_cat_images.parsers.engimg_parser import EngImgParser
from lost_cat_images.utils.utils_pdf import make_pdf_images, cv2
from lost_cat_images.utils.utils_ocr import classify_contours, Contour

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG
file_handler = logging.FileHandler(f"logs/test_ocr.log")
logger.addHandler(file_handler)

class TestOCR(unittest.TestCase):
    """A container class for the build path modeule test cases"""

    @classmethod
    def setUpClass(cls):
        """ Set up for Trie Unit Tests..."""
        uri = os.path.join("data")
        if not os.path.exists(uri):
            os.makedirs(uri)
            logger.info("Creating %s", uri)
        cls.images = []
        cls.files = []

        uri = os.path.join(uri, "*")
        for f in glob.glob(uri):
            _, ext = os.path.splitext(f)
            if ext.lower() in [".pdf"]:
                cls.files.append(f)
                imgs = make_pdf_images(path=f)
                for img in imgs:
                    cls.images.append(img)
            elif ext.lower() in [ "*.png"]:
                cls.files.append(f)
                img = cv2.imread(uri)
                if img.shape[0] > 100:
                    cls.images.append(img)

    @classmethod
    def tearDownClass(cls):
        """ Tear down for Trie Unit Tests"""
        return

    def test_contours(self):
        """Will load the contours for an image..."""
        return

    def test_extract(self):
        """This will scan the provided pdf and image files and
        extract the text using original flow"""
        for fidx, f in enumerate(self.files):
            logger.info("File: [%s] => %s", fidx, f)
            _, ext = os.path.splitext(f)
            if ext.lower() in [".pdf"]:
                # we have a PDF so now process.
                pdf = EngImgParser(f)
                conf = pdf.get_config()
                if "file" not in conf:
                    conf["file"] = {}
                conf["file"]["id"] = fidx
                pdf.set_config(conf)

                funx = pdf.avail_functions().get("parser")
                data = funx()
                for key, value in data.items():
                    logger.info("\t%s => %s", key, type(value))
