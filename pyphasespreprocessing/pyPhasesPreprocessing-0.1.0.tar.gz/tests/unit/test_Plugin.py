from unittest import TestCase

from pyPhases import ConfigNotFoundException, Project, pdict

from pyPhasesPreprocessing.Plugin import Plugin
from pyPhasesPreprocessing.Preprocessing import Preprocessing


class TestPlugin(TestCase):
    def setUp(self):
        self.options = {}
        self.project = Project()
        self.project.config = pdict(
            {
                "preprocessing": {
                    "targetFrequency": 50,
                    "forceGapBetweenEvents": False,
                    "signals": {
                        "eeg": ["a", "b", "c"]    
                    },
                    "targetChannels": ["a"],
                },
                "dataAugmentationBeforeSegmentation": []
            }
        )
        self.plugin = Plugin(self.project, self.options)

    def test_initPlugin(self):

        self.plugin.initPlugin()
        self.assertEqual(self.plugin.project, self.project)
        
        self.assertIn("RecordNumpyMemmapExporter", self.project.systemExporter)
        
        preprocessing = Preprocessing.instance
        self.assertEqual(preprocessing.targetChannels, ["a"])
        self.assertEqual(preprocessing.stepsByType, {"eeg": ["a", "b", "c"]})
        self.assertEqual(preprocessing.forceGapBetweenEvents, False)
        
        