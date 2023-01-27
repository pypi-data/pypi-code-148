import sys
from pathlib import Path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


class CodeViewer(QTextBrowser):
    res_path = Path(__file__).parent.parent / "res"

    def __init__(self):
        super(CodeViewer, self).__init__()
        self.clipboard = QApplication.clipboard()
        self.copy_btn = QPushButton(self)
        self.code = ""

        self.set_up()

    def set_up(self):
        self.set_window_attr()
        self.set_object_name()
        self.set_style_sheet()
        self.set_widget()
        self.set_signal()
        self.set_layout()

    def set_window_attr(self):
        self.setMinimumSize(700, 500)

    def set_object_name(self):
        self.setObjectName("codeViewer")
        self.copy_btn.setObjectName("copyBtn")

    def set_style_sheet(self):
        with open(self.res_path / "qss/viewer.qss") as f:
            self.setStyleSheet(f.read())

    def set_widget(self):
        self.copy_btn.setToolTip("点击复制代码")
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.setIcon(QIcon(str(self.res_path / "images/copy.png")))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def set_signal(self):
        self.copy_btn.clicked.connect(self.copy)
        self.clipboard.dataChanged.connect(self.on_clipboard_changed)

    def set_layout(self):
        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout(self)
        h_layout.addStretch()
        h_layout.addWidget(self.copy_btn)
        v_layout.addLayout(h_layout)
        v_layout.addStretch()

    def set_code(self, code):
        self.code = code
        formatter = HtmlFormatter(linenos=True, style="paraiso-dark")
        html = highlight(self.code, lexer=PythonLexer(), formatter=formatter)
        css = formatter.get_style_defs('.highlight').replace("#2f1e2e", "#2b2b2b").replace("#4f424c", "#2b2b2b")
        css = "<style>"+css+"</style>"
        self.setHtml(css+html)
        self.horizontalScrollBar().move(0, 0)

    def copy(self):
        self.clipboard.setText(self.code)

    def on_clipboard_changed(self):
        data = self.clipboard.mimeData()
        if data.text() == self.code:
            self.copy_btn.setIcon(QIcon(str(self.res_path / "images/check.png")))
            self.copy_btn.setToolTip("已复制")
        else:
            self.copy_btn.setIcon(QIcon(str(self.res_path / "images/copy.png")))
            self.copy_btn.setToolTip("点击复制代码")

    def contextMenuEvent(self, event):
        pass


if __name__ == "__main__":
    app = QApplication([])
    viewer = CodeViewer()
    viewer.show()
    sys.exit(app.exec())
