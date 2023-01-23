
from abc import abstractmethod
from dataclasses import dataclass
from typing import Union,Iterable,Iterator

from pptx import Presentation
from pptx.slide import Slide
from pptx.util import Cm, Inches,Emu,Pt

from nf_presentation.builders.base import Builder,ElementBuilder,BoxElementBuilder,ColoredBoxBuilder
from nf_presentation.logger import logger

class ImageBuilder(BoxElementBuilder):
    """a class for adding images to a slide,
    automaticly scales for height or width
    so can use set_size(width,None) to scale image to width and same for height(leave width None)"""
    def __init__(self, image):
        super().__init__()
        self.image=image
        self.href=None

    def set_size(self,width=None,height=None):
        """DEPRECATED"""
        self.size=width,height
        return self

    def with_href(self, href:str):
        """adds a hyperlink to this shape, ex. builder.with_href('https://nanofootball.com')"""
        self.href=href
        return self

    @property
    def width(self):
        width,height=self.size
        return width
    @property
    def height(self):
        width,height=self.size
        return height

    def _build(self, slide: Slide):
        shape=slide.shapes.add_picture(
            image_file=self.image,
            left= Cm(self.left),
            top= Cm(self.top),
            width=Cm(self.width) if self.width else None,
            height=Cm(self.height) if self.height else None)
        if self.href:
            shape.click_action.hyperlink.address=self.href
    