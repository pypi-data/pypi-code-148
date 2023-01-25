from pyPhases import PluginAdapter

from .downloader.Downloader import Downloader
from .RecordLoader import RecordLoader


class Plugin(PluginAdapter):
    def initPlugin(self):
        if "loader" not in self.project.config:
            self.project.config["loader"] = {}

        self.project.config["hasLoader"] = False
        self.loadLoader()
        self.project.once("loadLoader", self.loadLoader)

    def loadLoader(self):
        self.injectLoaderConfig(self.getConfig("useLoader"))

    def injectLoaderConfig(self, loaderId):
        # reload the model everytime the config changed
        self.log("Load loader and all Config: %s" % loaderId)
        if loaderId is not None:
            loaderconfigs = self.getConfig("loader")
            if loaderId not in loaderconfigs:
                raise Exception(
                    "Loader with the id '%s' is not initialized, a specific loader plugin like pyPhasesRecordloaderSHHS needs to be loaded before the generic pyPhasesRecordloader, please reorder your plugins in the config."
                    % loaderId
                )

            loaderconfig = loaderconfigs[loaderId]
            self.project.config.update(loaderconfig)

            self.updateLoaderConfig()

    def updateLoaderConfig(self):
        self.project.config["hasLoader"] = True

        sourceChannels = self.getConfig("sourceChannels")
        self.project.config["sourceChannelNames"] = [
            c["name"] for c in sourceChannels if "generated" not in c or c["generated"] != True
        ]
        self.project.config["sourceChannelTypes"] = [
            c["type"] for c in sourceChannels if "generated" not in c or c["generated"] != True
        ]

        self.project.config["optionalSignals"] = [
            c["name"] for c in sourceChannels if "optional" in c and c["optional"] == True
        ]

        RecordLoader.recordLoader.set(
            name=self.getConfig("dataset.loaderName"),
            options={
                "filePath": self.getConfig("filePath"),
                "targetSignals": self.project.config["sourceChannelNames"],
                "targetSignalTypes": self.project.config["sourceChannelTypes"],
                "optionalSignals": self.project.config["optionalSignals"],
                "combineChannels": self.project.config["combineChannels"],
            },
        )

        downloaderConfig = self.getConfig("dataset")["downloader"]
        Downloader.loadFromConfig(downloaderConfig)

        # self.project.config["dataSetChannelCount"] = self.project.config["addedLabelChannels"] + self.project.config["channelCount"]
