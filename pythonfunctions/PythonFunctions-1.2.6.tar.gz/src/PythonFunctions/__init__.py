from . import Version

if Version.canReadGlobal and Version.LocalSettings():
    Version.Compare()
