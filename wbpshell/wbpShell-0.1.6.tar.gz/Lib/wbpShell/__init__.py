import wx

from .preferences import ShellPreferences, name, shellConfig
from .shellwin import Shell

__version__ = "0.1.6"


info = wx.aui.AuiPaneInfo()
info.Name(name)
info.Caption(name)
info.MaximizeButton(True)
info.MinimizeButton(True)
info.CloseButton(False)
info.Bottom()
info.Dock()
info.Resizable()
info.FloatingSize(wx.Size(300, 200))
info.BestSize(wx.Size(800, 400))
info.MinSize(wx.Size(300, 200))
info.Icon(wx.ArtProvider.GetBitmap("PYSHELL", wx.ART_FRAME_ICON))
info.IconName = "PYSHELL"

panels = [(Shell, info)]
preferencepages = [ShellPreferences]
