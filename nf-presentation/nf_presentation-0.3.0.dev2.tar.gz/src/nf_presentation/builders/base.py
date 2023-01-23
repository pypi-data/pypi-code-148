from abc import abstractmethod

from pptx.slide import Slide
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.dml.color import RGBColor


from nf_presentation.logger import logger

class ElementBuilder:
    def __init__(self):
        self.position=(1,1)

    @property
    def left(self):
        left,_ =self.position
        return left

    @property
    def top(self):
        _,top=self.position
        return top

    def set_position(self,left,top):
        self.position=left,top
        return self

    def at(self, position):
        self.position=position
        return self

    @abstractmethod
    def _build(self, slide: Slide):
        pass

class BoxElementBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self.size=(1,1)
    
    def with_size(self, size:tuple[float,float]):
        self.size=size
        return self

    @property
    def width(self):
        width,height=self.size
        return width

    @property
    def height(self):
        width,height=self.size
        return height

class ColoredBoxBuilder(BoxElementBuilder):
    def __init__(self):
        super().__init__()
        self.background_color=None 
        self.foreground_color=None

    def with_foreground(self, rgb:tuple[int,int,int]):
        if rgb:
            r,g,b=rgb
            self.foreground_color=RGBColor(r,g,b)
        else:
            self.foreground_color=None
        return self

    def with_background(self, rgb:str):
        if rgb:
            r,g,b=rgb
            self.background_color=RGBColor(r,g,b)
        else:
            self.background_color=None
        return self


class ThemeColoredBoxBuilder(BoxElementBuilder):
    def __init__(self):
        super().__init__()
        self.background_color=None 
        self.foreground_color=None

    def with_foreground(self, color:str):
        if color:
            self.foreground_color=MSO_THEME_COLOR.from_xml(color)
        else:
            self.foreground_color=None
        return self

    def with_background(self, color:str):
        if color:
            self.background_color=MSO_THEME_COLOR.from_xml(color)
        else:
            self.background_color=None
        return self


class Builder:
    @abstractmethod
    def _build(self, injection):
        pass