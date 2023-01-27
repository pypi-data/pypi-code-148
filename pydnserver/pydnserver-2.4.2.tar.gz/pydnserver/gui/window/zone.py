# encoding: utf-8

from tkinter.constants import NSEW
from uiutil.window.child import ChildWindow
from ..frame.zone import ZoneConfigFrame


class ZoneConfigWindow(ChildWindow):

    def __init__(self,
                 address_list=None,
                 *args,
                 **kwargs):

        self.address_list = address_list

        super(ZoneConfigWindow, self).__init__(*args,
                                               **kwargs)

    def _draw_widgets(self):
        self.title(u"Zone Configuration")

        self.config = ZoneConfigFrame(parent=self._main_frame,
                                      address_list=self.address_list)
        self.config.grid(sticky=NSEW)
