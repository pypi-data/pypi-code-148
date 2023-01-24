"""Module for the engineering parser class, will extract the text from the provided
files: pdf, image"""
import logging
import os
import imghdr

import cv2
import numpy as np
#import pytesseract
#import re

from PIL import Image

from lost_cat.parsers.base_parser import BaseParser
# change this to use the office library, once created
#from lost_cat_images.parsers.pdf_parser import PDFParser
from lost_cat_office.parsers.pdf_parser import PDFParser
from lost_cat_images.utils.utils_ocr import extract_textareas, extract_artifacts

logger = logging.getLogger(__name__)

class EngImgParser(BaseParser):
    """An image file to extract engineering diagrams parser and converter"""
    def __init__(self, uri: str = None, bytes_io: bytes = None, settings: dict = None) -> None:
        super().__init__(uri=uri, bytes_io=bytes_io, settings=settings)
        self._version = "0.0.1"
        self._name = f"{self.__class__.__name__.lower()} {self._version}"

        if not settings:
            logger.debug("Loading default settings")
            self.settings = EngImgParser.avail_config()

        logger.debug("Name: %s", self._name)
        logger.debug("Settings: %s", self.settings)

        # file
        self._uri = None
        self._file = None
        self.images = []
        self._config = None

        if uri:
            self._uri = uri
            _, _ext = os.path.splitext(self._uri)
            if _ext.lower() in [".pdf"]:
                # pdf
                self._file = PDFParser(uri=self._uri)
                funx = self._file.avail_functions().get("screenshots")
                self.images = funx()

            elif _ext.lower() in [".png", ".tiff", ".jpg", ".jpeg", ".webp"]:
                # image file
                self._file = Image.open(self._uri)
                self.images = [self._file]

        elif bytes_io:
            if bytes_io[:4] == [0x25, 0x50, 0x44, 0x46]:
                # pdf
                self._file = PDFParser(uri=self._uri)
                funx = self._file.avail_functions().get("screenshots")
                self.images = funx()
            else:
                # open the image from a byte arrary
                if imghdr.what(bytes_io) in ["rgb", "tiff", "png", "jpg", "jpeg", "webp"]:
                    # <TODO: add the byte image loader, potentially ise SKImage>
                    self.images= []

    def set_config(self, value: dict):
        "sets the config"
        self._config = value

    def get_config(self):
        """get the config, if not set returns the available
        config"""
        if not getattr(self, "_config"):
            self._config = EngImgParser.avail_config()
        return self._config

    def avail_functions(self) -> dict:
        """Returns a dict prointing to the available functions"""
        return {
            "parser": self.parser,
            "contours": self.contours,
            #"anonimizer": self.set_anonimizer,
            "tags_alias": self.set_alias_tags,
            "tags_metadata": self.set_metadata_tags,
            "tags_groups": self.set_groups_tags,
        }

    @staticmethod
    def avail_config() -> dict:
        """returns default configuration details about the class"""
        return {
            "options":{},
            "uritypes": ["file"],
            "source":[
                {
                    "table": "URIMD",
                    "key": "ext",
                    "values": [".pdf", "*.png"]
                }
            ],
            "parser": {
                "file": {
                    "id": 0,
                },
                "kernel": {
                    "size": 3,
                },
                "operations": {
                    "blur": True,
                    "heal": True,
                },
                "threshold": {
                    "thresh": 75,
                    "maxval": 255,
                    "type": cv2.THRESH_BINARY | cv2.THRESH_OTSU,
                },
                "contours": {
                    "mode": cv2.RETR_TREE,
                    "method": cv2.CHAIN_APPROX_TC89_L1
                }
            }
        }

    def close(self, force: bool = False, block: bool = False, timeout: int = -1):
        """will close the """
        if self._file:
            self._file = None

    def parser(self) -> dict:
        """will parser the open file and retrn the result
        This parser will break out the text blocks ands return them currently
        as a json object, with location on page.
        """
        _data = {}
        for iidx, pil_img in enumerate(self.images):
            # convert and process each image
            img = np.array(pil_img)
            logger.info("IMG: [%s] => %s", iidx, img.shape)
            _resp = extract_textareas(image= img, config=self._config.get("parser"))
            _data[iidx] = {
                "text": _resp.get("text")
            }

        return _data

    def contours(self) -> dict:
        """will parser the open file and retrn the result
        This parser will break out the text blocks ands return them currently
        as a json object, with location on page.
        """
        _data = {}
        for iidx, pil_img in enumerate(self.images):
            # convert and process each image
            img = np.array(pil_img)
            logger.info("IMG: [%s] => %s", iidx, img.shape)
            _data[iidx] = extract_artifacts(image= img, config=self._config.get("parser"))

        return _data

