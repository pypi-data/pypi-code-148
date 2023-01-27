# encoding: utf-8

from tkinter.constants import NSEW
from uiutil.window.child import ChildWindow
from ..frame.forwarder import AddEditForwarderFrame


class AddEditForwarderWindow(ChildWindow):

    def __init__(self,
                 selected_record=None,
                 edit=False,
                 *args,
                 **kwargs):

        self.selected_record = selected_record
        self.edit = edit

        super(AddEditForwarderWindow, self).__init__(*args,
                                                     **kwargs)

    def _draw_widgets(self):
        self.title(u"Add/Edit Forwarder")

        self.config = AddEditForwarderFrame(parent=self._main_frame,
                                            selected_record=self.selected_record,
                                            edit=self.edit)
        self.config.grid(sticky=NSEW)
