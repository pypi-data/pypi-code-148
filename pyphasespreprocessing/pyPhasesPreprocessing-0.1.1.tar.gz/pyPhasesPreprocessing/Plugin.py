from pyPhases import PluginAdapter

from .Preprocessing import Preprocessing
from .exporter.RecordNumpyMemmapExporter import RecordNumpyMemmapExporter

class Plugin(PluginAdapter):
    
    def __init__(self, project, options=...):
        super().__init__(project, options)
        self.project.systemExporter["RecordNumpyMemmapExporter"] = "pyPhasesPreprocessing"
        
    
    def initPlugin(self):
        Preprocessing.setup(self.project.config)