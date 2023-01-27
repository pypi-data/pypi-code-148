import sys
import webbrowser
from pathlib import Path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qtbox.utils.viewer import CodeViewer
from qtbox.pushbutton.func.button1 import FuncButton1
from qtbox.pushbutton.style.button1 import StyleButton1
from qtbox.pushbutton.style.button2 import StyleButton2
from qtbox.pushbutton.style.button3 import StyleButton3


class Window(QWidget):
    res_path = Path(__file__).parent / "res"

    def __init__(self):
        super(Window, self).__init__()
        self.btn_list_widget = QListWidget()
        self.btn_list = [QPushButton(txt) for txt in ["QPushButton", "QLabel", "QSlider", "1", "2", "3", "4", "5", "6", "7", "8"]]

        self.func_widget = QWidget()
        self.style_widget = QWidget()
        self.func_tab = QScrollArea()
        self.style_tab = QScrollArea()
        self.tab_widget = QTabWidget()

        self.doc_btn = QPushButton()
        self.about_btn = QPushButton()
        self.settings_btn = QPushButton()

        self.code_viewer = CodeViewer()

        self.grid_layout_children = []
        self.grid_layout = QGridLayout()

        self.pushbutton_dict = {
            "func": [FuncButton1, FuncButton1, FuncButton1, FuncButton1],
            "style": [StyleButton1, StyleButton2, StyleButton3, StyleButton1,
                    StyleButton1, StyleButton1, StyleButton1, StyleButton1,
                    StyleButton1, StyleButton2, StyleButton1, StyleButton1,
                    StyleButton1, StyleButton2, StyleButton1, StyleButton1,
                    StyleButton1, StyleButton2, StyleButton1, StyleButton1,
                    StyleButton1, StyleButton2, StyleButton1, StyleButton1,
                    StyleButton1, StyleButton2, StyleButton1, StyleButton1,
                    StyleButton1, StyleButton2, StyleButton1, StyleButton1,
                    StyleButton1, StyleButton2, StyleButton1, StyleButton1,
                    StyleButton1, StyleButton2, StyleButton1, StyleButton1,
                    StyleButton1, StyleButton2, StyleButton1, StyleButton1,
                    StyleButton1, StyleButton2, StyleButton1, StyleButton1]
        }

        self.set_up()

    def set_up(self):
        self.set_window_attr()
        self.set_object_name()
        self.set_style_sheet()
        self.set_widget()
        self.set_signal()
        self.set_layout()

        self.btn_list[0].setCheckable(True)
        self.btn_list[0].setChecked(True)
        self.set_tab_content("QPushButton")

    def set_window_attr(self):
        self.resize(1000, 600)
        self.setWindowTitle("Qt Box")
        self.setWindowIcon(QIcon(str(self.res_path / "images/icon.png")))

    def set_object_name(self):
        self.setObjectName("window")
        self.btn_list_widget.setObjectName("btnList")

        for btn in self.btn_list:
            btn.setObjectName("listBtn")

        self.doc_btn.setObjectName("docBtn")
        self.about_btn.setObjectName("aboutBtn")
        self.settings_btn.setObjectName("settingsBtn")

        self.tab_widget.setObjectName("tabWidget")
        self.func_tab.setObjectName("funcScroll")
        self.style_tab.setObjectName("styleScroll")
        self.func_widget.setObjectName("funcWidget")
        self.style_widget.setObjectName("styleWidget")

    def set_style_sheet(self):
        with open(self.res_path / "qss/window.qss") as f:
            self.setStyleSheet(f.read())

    def set_widget(self):
        self.btn_list_widget.setMaximumWidth(300)
        self.btn_list_widget.setMinimumWidth(150)

        self.func_tab.setWidgetResizable(True)
        self.style_tab.setWidgetResizable(True)
        self.func_tab.setWidget(self.func_widget)
        self.style_tab.setWidget(self.style_widget)
        self.func_tab.setAlignment(Qt.AlignCenter)
        self.style_tab.setAlignment(Qt.AlignCenter)
        self.tab_widget.addTab(self.style_tab, "样式")
        self.tab_widget.addTab(self.func_tab, "功能")

        self.doc_btn.setCursor(Qt.PointingHandCursor)
        self.about_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.doc_btn.setIcon(QIcon(str(self.res_path / "images/doc.png")))
        self.about_btn.setIcon(QIcon(str(self.res_path / "images/about.png")))
        self.settings_btn.setIcon(QIcon(str(self.res_path / "images/settings.png")))

        self.code_viewer.hide()

    def set_signal(self):
        for btn in self.btn_list:
            btn.clicked.connect(self.change_widget)

        self.doc_btn.clicked.connect(self.open_doc)
        self.about_btn.clicked.connect(self.show_info)
        self.settings_btn.clicked.connect(self.show_settings)
        self.tab_widget.currentChanged.connect(self.change_tab)

    def set_layout(self):
        v_layout1 = QVBoxLayout()
        h_layout1 = QHBoxLayout()
        h_layout2 = QHBoxLayout()
        v_layout1.setContentsMargins(0, 0, 0, 0)
        h_layout1.setContentsMargins(0, 0, 0, 0)

        for btn in self.btn_list:
            item = QListWidgetItem()
            item.setSizeHint(QSize(150, 50))
            self.btn_list_widget.addItem(item)
            self.btn_list_widget.setItemWidget(item, btn)

        h_layout1.addWidget(self.doc_btn)
        h_layout1.addWidget(self.about_btn)
        h_layout1.addWidget(self.settings_btn)

        v_layout1.addLayout(h_layout1)
        v_layout1.addWidget(self.btn_list_widget)
        h_layout2.addLayout(v_layout1)
        h_layout2.addWidget(self.tab_widget)
        self.setLayout(h_layout2)

        self.grid_layout.setVerticalSpacing(30)
        self.grid_layout.setHorizontalSpacing(60)

    def change_widget(self):
        self.update_btn_style()
        self.clear_grid_layout()
        self.set_tab_content(self.sender().text())

    def change_tab(self):
        self.clear_grid_layout()

        for btn in self.btn_list:
            if btn.isChecked():
                self.set_tab_content(btn.text())
                break

    def update_btn_style(self):
        for btn in self.btn_list:
            if btn.text() == self.sender().text():
                btn.setCheckable(True)
                btn.setChecked(True)
            else:
                btn.setCheckable(False)
                btn.setChecked(False)
        self.btn_list_widget.update()

    def clear_grid_layout(self):
        for widget in self.grid_layout_children:
            widget.deleteLater()
        self.grid_layout_children = []

    def set_tab_content(self, btn_txt):
        widget_list = []
        tab_index = self.tab_widget.currentIndex()

        if btn_txt == "QLabel":
            if tab_index == 0:
                ...
            else:
                ...
        elif btn_txt == "QPushButton":
            if tab_index == 0:
                widget_list = self.pushbutton_dict["style"]
            else:
                widget_list = self.pushbutton_dict["func"]

        if self.tab_widget.currentIndex() == 0:
            self.set_style_tab_content(widget_list)
        else:
            self.set_func_tab_content(widget_list)

    def set_style_tab_content(self, widget_list):
        self.add_widget_list_to_grid_layout(widget_list)
        self.style_widget.setLayout(self.grid_layout)

    def set_func_tab_content(self, widget_list):
        self.add_widget_list_to_grid_layout(widget_list)
        self.func_widget.setLayout(self.grid_layout)

    def add_widget_list_to_grid_layout(self, widget_list):
        row, column = 0, 0
        for widget in widget_list:
            if column != 0 and column % 3 == 0:
                row += 1
                column = 0

            widget = widget()
            widget.view_code_signal.connect(self.view_code)
            widget.download_code_signal.connect(self.download_code)
            self.grid_layout.addWidget(widget, row, column, 1, 1, Qt.AlignCenter)
            self.grid_layout_children.append(widget)
            column += 1

    def view_code(self, code_file_path):
        code = self.get_code_content(code_file_path)
        self.code_viewer.set_code(code)
        self.code_viewer.show()

    def download_code(self, code_file_path):
        path, _ = QFileDialog.getSaveFileName(self, '保存文件', './', '文件类型 (*.py)')
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.get_code_content(code_file_path))

    @staticmethod
    def get_code_content(code_file_path):
        code = ""
        with open(code_file_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if "pathlib" not in line and "Base" not in line:
                    code += line
            return code.replace("str(Path(__file__))", "")

    @staticmethod
    def open_doc():
        webbrowser.open("https://baidu.com")

    def show_info(self):
        QMessageBox.about(self, "Qt Box", "123")

    def show_settings(self):
        ...


def main():
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()