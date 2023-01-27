from dataclasses import dataclass
from typing import Union, Iterator

from pptx import Presentation
from pptx.util import Emu

from nf_presentation.builders.slide_builder import SlideBuilder
from nf_presentation.builders.base import Builder
from nf_presentation.logger import logger


@dataclass
class PresentationRatio:
    """a class representing a presentation ratio,

    basically it sets each slide width and height"""
    width: Emu
    height: Emu
    alias: str


class Ratios:
    """An enumeration of avialable presentation ratios"""

    _16x9 = PresentationRatio(
        width=Emu(12192000),
        height=Emu(6858000),
        alias='16:9')

    _4x3 = PresentationRatio(
        width=Emu(9144000),
        height=Emu(6858000),
        alias='4:3')  # the old broken one

    @classmethod
    def list(cls) -> Iterator[PresentationRatio]:
        """returns an iterator with all ratios
        returns all ratios available in current package"""
        ratios = []
        for key in cls.__dict__:
            item: PresentationRatio = getattr(cls, key)
            if isinstance(item, PresentationRatio):
                ratios.append(item)
        return iter(ratios)

    @classmethod
    def get_by_alias(cls, alias: str):
        """returns a PresentationRatio object with asked alias
        searches this enumeration class for available items"""
        for ratio in cls.list():
            if ratio.alias == alias:
                return ratio
        raise AttributeError(f'Ratio {alias} not found')


class PresentationBuilder:
    """A class for building a presentation
    a root element, all global settings are set here
    and slides are made out of here

    eg.

    p = PresentationBuilder().with_ratio('16x9')
    slide = p.create_slide()
    ...
    p.save(to='out.pptx')"""

    def __init__(self, ratio: Union[str, PresentationRatio] = Ratios._16x9):
        self.slide_builders: list[Builder] = []
        self.with_ratio(ratio)

    def with_ratio(self, ratio=Union[str, PresentationRatio]):
        """sets the ratio of the presentation
        
            ratio: str| Presentation ratio
                a ratio for presentation may be a string or object
        p=PresentationBuilder().with_ratio("16x9")"""

        if isinstance(ratio, str):
            self.ratio = Ratios.get_by_alias(ratio)
        else:
            self.ratio = ratio
        return self

    def create_slide(self) -> SlideBuilder:
        """Creates a new slide
        and returns a new SlideBuilder object"""
        slide_builder = SlideBuilder()
        self.slide_builders.append(slide_builder)
        return slide_builder

    def build(self) -> Presentation:
        """Returns a pptx.Presentation object
        with a constructed presentation"""

        presentation: Presentation = Presentation()
        presentation.slide_width = self.ratio.width
        presentation.slide_height = self.ratio.height
        for slide_builder in self.slide_builders:
            slide_builder._build(presentation)
        return presentation

    def save(self, to):
        """saves a presentation to a file or a stream
        to: file to save,
        ex. save(to='sample.pptx')"""
        presentation = self.build()
        presentation.save(to)
