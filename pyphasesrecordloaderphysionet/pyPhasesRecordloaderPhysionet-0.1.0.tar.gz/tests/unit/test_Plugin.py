from unittest import TestCase

from pyPhases import Project, pdict

from pyPhasesRecordloaderPhysionet.Plugin import Plugin
from pyPhasesRecordloader import RecordLoader


class TestPlugin(TestCase):

    def setUp(self):
        self.options = {}
        self.project = Project()
        self.project.config = pdict(
            {
                "useLoader": "physionet",
            }
        )
        # self.plugin = Plugin(self.project, self.options)
        self.project.addPlugin("pyPhasesRecordloaderPhysionet")
        self.plugin = self.project.plugins[-1]

    def test_initPlugin(self):

        self.plugin.initPlugin()
        
        self.assertIn("RecordLoaderPhysio", RecordLoader.recordLoaders)
        self.assertIn("physionet", self.project.config["loader"]) 
        self.assertEqual(self.project.config["useLoader"], "physionet") 
        self.assertEqual(self.project.config["loader"]["physionet"]["dataBase"], "PhysioNet2018")
