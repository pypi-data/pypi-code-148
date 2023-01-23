"""All sizes and lenghts are in centimeters (will be transformed to  pptx.util.Cm class)"""

from abc import abstractmethod
from dataclasses import dataclass
from typing import Union,Iterable,Iterator

from pptx import Presentation
from pptx.util import Cm, Inches,Emu,Pt

from nf_presentation.builders.slide_builder import SlideBuilder
from nf_presentation.builders.base import Builder
from nf_presentation.logger import logger


@dataclass
class PresentationRatio:
        width:Emu
        height:Emu
        alias:str

class Ratios:
    _16x9=PresentationRatio(width=Emu(12192000),height=Emu(6858000),alias='16:9')
    _4x3=PresentationRatio(width=Emu(9144000),height=Emu(6858000),alias='4:3') # the old broken one

    
    @classmethod
    def list(cls) -> Iterator[PresentationRatio]:
        """returns all ratios as iter"""
        ratios=[]
        for key in cls.__dict__:
            item:PresentationRatio=getattr(cls,key)
            if isinstance(item,PresentationRatio):
                ratios.append(item)
        return iter(ratios)


    @classmethod
    def get_by_alias(cls,alias:str):
        for ratio in cls.list():
            if ratio.alias==alias:
                return ratio
        raise AttributeError(f'Ratio {alias} not found')



    
class PresentationBuilder:
    def __init__(self, ratio : Union[str, PresentationRatio] = Ratios._16x9):
        self.slide_builders:list[Builder]=[]
        self.with_ratio(ratio)

    def with_ratio(self, ratio = Union[str, PresentationRatio]):
        if isinstance(ratio,str):
            self.ratio=Ratios.get_by_alias(ratio)
        else:
            self.ratio=ratio
        return self

    def add_slide(self, slide_builder:SlideBuilder):
        """DEPRECATED"""
        self.slide_builders.append(slide_builder)

    def create_slide(self) -> SlideBuilder:
        slide_builder=SlideBuilder()
        self.slide_builders.append(slide_builder)
        return slide_builder

    def build(self) -> Presentation:
        presentation : Presentation =Presentation()
        presentation.slide_width=self.ratio.width
        presentation.slide_height=self.ratio.height
        for slide_builder in self.slide_builders:
            slide_builder._build(presentation)
        return presentation

    def save(self,to):
        """saves a presentation to a file or a stream
        to: file to save, 
        ex. save(to='sample.pptx')"""
        presentation=self.build()
        presentation.save(to)




