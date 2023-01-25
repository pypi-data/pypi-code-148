from PyQt5.QtDesigner import QFormBuilder
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, qApp
from PyQt5.QtCore import QSettings, QPoint, QSize, Qt, QFileInfo, QFile
from PyQt5.QtGui import QPixmap
from GUI_mainGrowthTool import Ui_Growth_Tool_main



def settings_value_is_valid(val):
    # https://stackoverflow.com/a/60028282/4988010
    if isinstance(val, QPixmap):
        return not val.isNull()
    return True

def settings_restore(settings):
    # https://stackoverflow.com/a/60028282/4988010
    finfo = QFileInfo(settings.fileName())

    if finfo.exists() and finfo.isFile():
        for w in qApp.allWidgets():
            if w.objectName() and not w.objectName().startswith("qt_"):
                # if w.objectName():
                mo = w.metaObject()
                for i in range(mo.propertyCount()):
                    prop = mo.property(i)
                    name = prop.name()
                    last_value = w.property(name)
                    key = "{}/{}".format(w.objectName(), name)
                    # print(prop, name, last_value, key)
                    if not settings.contains(key):
                        continue
                    val = settings.value(key, type=type(last_value), )
                    if (
                            val != last_value
                            and settings_value_is_valid(val)
                            and prop.isValid()
                            and prop.isWritable()
                    ):
                        w.setProperty(name, val)

def settings_save(settings):
    # https://stackoverflow.com/a/60028282/4988010
    for w in qApp.allWidgets():
        if w.objectName() and not w.objectName().startswith("qt_"):
            # if w.objectName():
            mo = w.metaObject()
            for i in range(mo.propertyCount()):
                prop = mo.property(i)
                name = prop.name()
                key = "{}/{}".format(w.objectName(), name)
                val = w.property(name)
                if settings_value_is_valid(val) and prop.isValid() and prop.isWritable():
                    settings.setValue(key, w.property(name))

class save(QMainWindow):

    def __init__(self):
        super().__init__()

        self.settings = QSettings("dep/gui.ui", QSettings.IniFormat)
        print(self.settings.fileName())

        try:
            self.config_widgets_load_settings()
        except:
            pass

    def closeEvent(self, event):
        self.config_widgets_save_settings()
        event.accept()

    def config_widgets_save_settings(self):
        # Write current state to the settings config file
        settings_save(self.settings)

    def config_widgets_load_settings(self):
        # Load settings config file
        settings_restore(self.settings)

    def config_clear_settings(self):
        # Clear the settings config file
        self.settings.clear()

class GuiApp:
    def __init__(self):
        import sys
        self.app = QApplication(sys.argv)
        self.app.setStyle('Windows')
        # use AA_EnableHighDpiScaling for both high and low res app versions:
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            self.app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            self.app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        self.window = QMainWindow()
        self.ui = Ui_Growth_Tool_main()
        self.ui.setupUi(self.window)
        self.window.showMaximized()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    GuiApp()

