from typing import Callable

import fitz
from fitz.utils import getColor


class PDFDocument:
    def __init__(
        self,
        fpath: str,
    ) -> None:
        self.fpath = fpath
        self.document = fitz.Document(fpath)

    def highlight_sent(
        self, page: fitz.Page, textpage: fitz.TextPage, sent: str, color: str
    ) -> None:
        quads = textpage.search(sent, quads=True)
        highlight = page.add_highlight_annot(quads)
        highlight.set_colors(stroke=getColor(color))
        highlight.update()

    def run_highlighting(
        self, clf: Callable[[str], str | bool], type2color: dict[str, str]
    ):
        for page in self.document.pages():
            textpage = page.get_textpage()
            sents = [f"{sent}." for sent in textpage.extractText().split(".")]
            for sent in sents:
                sent_type = clf(sent)
                if sent_type is False:
                    continue
                else:
                    assert isinstance(sent_type, str)
                    color = type2color[sent_type]
                    self.highlight_sent(page, textpage, sent, color)

    def save(self, opath) -> None:
        self.document.save(opath)
