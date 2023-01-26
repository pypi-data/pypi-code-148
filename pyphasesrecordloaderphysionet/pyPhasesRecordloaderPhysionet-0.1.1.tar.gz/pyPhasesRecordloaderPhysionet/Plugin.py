from pyPhases import PluginAdapter
from pyPhasesRecordloader import RecordLoader


class Plugin(PluginAdapter):
    
    def initPlugin(self):   
        RecordLoader.registerRecordLoader("RecordLoaderPhysio", "pyPhasesRecordloaderPhysionet.recordLoaders")