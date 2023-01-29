"""
shellwin
===============================================================================

Implementation of the shell panel.

The shell panel is based on the wxPython 
`Shell <https://wxpython.org/Phoenix/docs/html/wx.py.shell.Shell.html>`_ 
control.
"""
import sys

import wx
from wx.py.shell import Shell as ShellBase

from wbBase.control.textEditControl import MARGIN_SYMBOLS

from .preferences import shellConfig, name

class Shell(ShellBase):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.CLIP_CHILDREN | wx.NO_BORDER,
        introText=None,
        locals=None,
        InterpClass=None,
        startupScript=None,
        execStartupScript=True,
        name=name,
        **kwds,
    ):
        if not introText:
            introText = f"# Python {sys.version}"
        super().__init__(
            parent,
            id,
            pos,
            size,
            style,
            introText,
            locals,
            InterpClass,
            startupScript,
            execStartupScript,
            **kwds,
        )
        shellConfig.load()
        shellConfig.apply(self)
        self.SetMargins(2, 2)
        self.SetMarginWidth(MARGIN_SYMBOLS, 0)  # not used yet - turn off

    def showIntro(self, text:str="") -> None:
        """
        Display introductory text in the shell.
        
        :param text: the text to display
        """
        if text:
            self.write(text)
