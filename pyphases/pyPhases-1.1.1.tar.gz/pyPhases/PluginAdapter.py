from pyPhases import Project
from pyPhases.util.EventBus import EventBus
from pyPhases.util.Optionizable import Optionizable


class PluginAdapter(Optionizable, EventBus):

    def __init__(self, project: Project, options=None):
        super().__init__(options)
        self.project = project

    def getConfig(self, key):
        return self.project.getConfig(key)

    def initPlugin(self):
        self.logDebug("Plugin loaded")
