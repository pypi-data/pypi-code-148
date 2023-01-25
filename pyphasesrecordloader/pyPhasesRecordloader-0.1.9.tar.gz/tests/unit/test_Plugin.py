from unittest import TestCase

from pyPhases import ConfigNotFoundException, Project, pdict

from pyPhasesRecordloader.downloader.Downloader import Downloader
from pyPhasesRecordloader.downloader.FolderDownloader import FolderDownloader
from pyPhasesRecordloader.Plugin import Plugin
from pyPhasesRecordloader.RecordLoader import RecordLoader


class TestPlugin(TestCase):
    def test_loaderMisconfigured(self):
        project = Project()
        project.config = pdict({})
        plugin = Plugin(project)

        # useLoader not specified
        self.assertRaises(ConfigNotFoundException, plugin.initPlugin)
        self.project.config = pdict({"useLoader": "myLoader"})
        plugin = Plugin(self.project)

        # loader config is not specified
        self.assertRaises(Exception, plugin.initPlugin)

        self.project.config = pdict({"useLoader": "myLoader"})
        plugin = Plugin(self.project)
        self.assertRaises(Exception, plugin.initPlugin)

    def setUp(self):
        self.options = {}
        self.project = Project()
        self.project.config = pdict(
            {
                "useLoader": "myLoader",
                "loader": {
                    "myLoader": {
                        "sourceChannels": [],
                        "dataset": {
                            "loaderName": "MyRecordLoader",
                            "downloader": {
                                "type": "allFromFolder",
                                "basePath": ".",
                            },
                        },
                        "filePath": ".",
                        "combineChannels": [],
                    },
                },
            }
        )
        self.plugin = Plugin(self.project, self.options)

    def test_initPlugin(self):

        self.plugin.initPlugin()
        self.assertEqual(self.plugin.project, self.project)
        self.assertEqual(self.project.config["sourceChannels"], [])
        self.assertEqual(
            self.project.config["dataset"],
            {
                "loaderName": "MyRecordLoader",
                "downloader": {
                    "type": "allFromFolder",
                    "basePath": ".",
                },
            },
        )

        # process channels
        self.assertIn("sourceChannelNames", self.project.config)
        self.assertIn("sourceChannelTypes", self.project.config)
        self.assertIn("optionalSignals", self.project.config)

        # set recordloader
        self.assertEqual(RecordLoader.recordLoader.moduleName, "MyRecordLoader")

        # set downloader
        self.assertIsInstance(Downloader.instance, Downloader)
        self.assertIsInstance(Downloader.instance, FolderDownloader)
