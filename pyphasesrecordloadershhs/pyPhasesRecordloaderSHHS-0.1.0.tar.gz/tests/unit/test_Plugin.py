from unittest import TestCase

from pyPhases import ConfigNotFoundException, Project, pdict

from pyPhasesRecordloaderSHHS.Plugin import Plugin
from pyPhasesRecordloader import RecordLoader


class TestPlugin(TestCase):
    def test_loaderMisconfigured(self):
        project = Project()
        project.config = pdict({})
        plugin = Plugin(project)

        # useLoader not specified
        self.assertRaises(ConfigNotFoundException, plugin.initPlugin)
        self.project.config = pdict({"useLoader": "shhs"})
        plugin = Plugin(self.project)
        self.assertRaises(ConfigNotFoundException, plugin.initPlugin)

    def setUp(self):
        self.options = {}
        self.project = Project()
        self.project.addPlugin("pyPhasesRecordloaderSHHS", self.options)
        self.plugin = self.project.plugins[-1]
        self.project.config.update({"useLoader": "shhs", "shhs-path": "./data"})

    def test_initPlugin(self):

        self.plugin.initPlugin()

        self.assertIn("RecordLoaderSHHS", RecordLoader.recordLoaders)
        self.assertIn("SHHSAnnotationLoader", RecordLoader.recordLoaders)
        self.assertIn("shhs", self.project.config["loader"])
        self.assertIn("shhs2", self.project.config["loader"])

        self.assertEqual(self.project.config["loader"]["shhs"]["dataBase"], "SHHS1")
        self.assertEqual(self.project.config["loader"]["shhs2"]["dataBase"], "SHHS2")
        self.assertEqual(
            self.project.config["loader"]["shhs"]["dataset"]["downloader"]["basePath"], "./data/polysomnography/edfs/shhs1"
        )
        self.assertEqual(
            self.project.config["loader"]["shhs2"]["dataset"]["downloader"]["basePath"], "./data/polysomnography/edfs/shhs2"
        )
