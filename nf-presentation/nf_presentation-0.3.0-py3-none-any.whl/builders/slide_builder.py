from pptx import Presentation

from nf_presentation.builders.base import Builder,ElementBuilder,BoxElementBuilder,ColoredBoxBuilder
from nf_presentation.builders.text_builder import TextBuilder,TitleBuilder
from nf_presentation.builders.table_builder import RowTableBuilder
from nf_presentation.builders.image_builder import ImageBuilder
from nf_presentation.logger import logger

TITLE_ONLY_LAYOUT=5
BLANK_LAYOUT=6



class SlideBuilder(Builder):
    """A builder for slides
    dont forget to add title
    and use any builder of table or picture to add to slides
    
    table_builder=TableBuilder()
    ...
    add_element(table_builder)"""
    def __init__(self):
        self.shape_builders:list[ElementBuilder]=[]

    def set_title(self, title:str):
        self.title=title
        return self

    def add_element(self,builder:ElementBuilder):
        self.shape_builders.append(builder)
        return builder

    def create_table(self) -> RowTableBuilder:
        return self.add_element(RowTableBuilder())

    def create_image(self,image_file:str) -> ImageBuilder:
        return self.add_element(ImageBuilder(image=image_file))

    def create_text(self, text:str) -> TextBuilder:
        return self.add_element(TextBuilder(text=text))
    
    def create_title(self, text:str) -> TitleBuilder:
        return self.add_element(TitleBuilder(text=text))

    def _build(self,presentation:Presentation):
        blank_slide_layout=presentation.slide_layouts[BLANK_LAYOUT]
        slide= presentation.slides.add_slide(blank_slide_layout)

        for builder in self.shape_builders:
            builder._build(slide)