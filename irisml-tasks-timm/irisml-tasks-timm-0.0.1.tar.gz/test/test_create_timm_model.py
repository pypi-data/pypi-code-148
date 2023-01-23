import pickle
import unittest
import torch
from irisml.tasks.create_timm_model import Task


class TestCreateTimmModel(unittest.TestCase):
    def test_simple(self):
        config = Task.Config(name='resnet50', num_classes=256)
        task = Task(config)
        outputs = task.execute(None)
        self.assertIsInstance(outputs.model, torch.nn.Module)

        config = Task.Config(name='resnet50', num_classes=256, task_type='multilabel_classification')
        task = Task(config)
        outputs = task.execute(None)
        self.assertIsInstance(outputs.model, torch.nn.Module)

    def test_pickle(self):
        config = Task.Config(name='resnet50', num_classes=256)
        task = Task(config)
        outputs = task.execute(None)
        model = outputs.model

        serialized = pickle.dumps(model)
        deserialized = pickle.loads(serialized)

        state_dict = model.state_dict()
        state_dict2 = deserialized.state_dict()
        self.assertEqual(set(state_dict.keys()), set(state_dict2.keys()))
        for key in state_dict:
            self.assertTrue(torch.equal(state_dict[key], state_dict2[key]))
