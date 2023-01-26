from abc import abstractmethod
from pptx.text.text import _Paragraph,_Run

from nf_presentation.builders.base import Builder



class TextItem:
    def __init__(self):
        self.font_family=None
        self.font_size=None
    @abstractmethod
    def _make_run(self, run:_Run):
        pass

class PlainText(TextItem):
    def __init__(self,text:str):
        super().__init__()
        self.text=text
    def _make_run(self, run:_Run):
        super()._make_run(run)
        run.text=self.text

class HyperLink(TextItem):
    def __init__(self,link_text:str,href:str):
        super().__init__()
        self.link_text=link_text
        self.href=href
    def _make_run(self, run:_Run):
        super()._make_run(run)
        run.text=self.link_text
        run.hyperlink.address=self.href
        

class ParagraphBuilder(Builder):
    def __init__(self):
        self._items:list[TextItem]=[]
    def append_text(self,text:str,):
        self._items.append(PlainText(text=text))
    def append_link(self,link_text:str,href:str):
        self._items.append(HyperLink(link_text=link_text,href=href))
    def _build(self, paragraph:_Paragraph):
        for item in self._items:
            run=paragraph.add_run()
            item._make_run(run=run)