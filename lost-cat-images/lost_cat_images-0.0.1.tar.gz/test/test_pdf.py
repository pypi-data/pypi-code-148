"""A test case for the path utils module"""
import logging
import glob
import os
import sys
import unittest

from lost_cat_images.utils.utils_pdf import make_pdf_images, process_pdf, make_pdf_thumbnail, cv2

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

class TestPDF(unittest.TestCase):
    """A container class for the build path modeule test cases"""

    @classmethod
    def setUpClass(self):
        """ Set up for Trie Unit Tests..."""
        uri = os.path.join("data")
        if not os.path.exists(uri):
            os.makedirs(uri)
            logger.info("Creating %s", uri)
        self.files = []

        uri = os.path.join(uri, "*")
        for f in glob.glob(uri):
            _, ext = os.path.splitext(f)
            if ext.lower() == ".pdf":
                self.files.append(f)

    @classmethod
    def tearDownClass(self):
        """ Tear down for Trie Unit Tests"""
        pass

    def test_thumbnail(self):
        """Will test the thumbnail process"""
        for fidx, f in enumerate(self.files):
            logger.info("File: %s", f)
            imgs = make_pdf_thumbnail(path=f, size=100, first_page=False)
            logger.info("Imgs: %s", len(imgs))
            for iidx, img in enumerate(imgs):
                (w,h,c) = img.shape
                self.assertEqual(first=w, second=100, msg="Image width is incorrect")
                self.assertEqual(first=h, second=100, msg="Image height is incorrect")
                cv2.imwrite(f'data/THM{fidx}.{iidx}.png', img)

    def test_pdfinfo(self):
        """Will test the info in the document"""
        for f in self.files:
            logger.info("File: %s", f)
            data = process_pdf(path=f)
            self.assertIn(member="metadata", container=data, msg="Missing 'metadata' key")
            self.assertIn(member="toc", container=data, msg="Missing 'toc' key")
            self.assertIn(member="texts", container=data, msg="Missing 'texts' key")
            self.assertIn(member="images", container=data, msg="Missing 'images' key")

    def test_pdfimages(self):
        """will test the generation of the pdf"""
        for fidx, f in enumerate(self.files):
            logger.info("File: %s", f)
            imgs = make_pdf_images(path=f, first_page=False)
            logger.info("Imgs: %s", len(imgs))
            for iidx, img in enumerate(imgs):
                (w,h,c) = img.shape
                self.assertGreater(a=w, b=0, msg="Image width is incorrect")
                self.assertGreater(a=h, b=0, msg="Image height is incorrect")
                cv2.imwrite(f'data/PAGE{fidx}.{iidx}.png', img)
