from pyPhases import PluginAdapter
from pyPhasesML.ModelManager import ModelManager
from .exporter.ModelExporter import ModelExporter

class Plugin(PluginAdapter):
    
    def initPlugin(self):
        # reload the model everytime the config changed
        def updateModel(changedValue):
            ModelManager.loadModel(self.project)
        self.project.on("configChanged", updateModel)
        
        self.project.registerExporter(ModelExporter())
        self.project.systemExporter["ModelExporter"] = "pyPhasesML"
        
    