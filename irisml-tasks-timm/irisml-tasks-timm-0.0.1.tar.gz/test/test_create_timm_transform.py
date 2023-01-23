import pickle
import unittest
import PIL.Image
from irisml.tasks.create_timm_transform import Task


class TestCreateTimmTransform(unittest.TestCase):
    def test_simple(self):
        config = Task.Config(input_size=224)
        task = Task(config)
        outputs = task.execute(None)

        self.assertIsNotNone(outputs.train_transform)
        self.assertIsNotNone(outputs.val_transform)

    def test_pickle(self):
        config = Task.Config(input_size=224)
        task = Task(config)
        outputs = task.execute(None)

        serialized = pickle.dumps(outputs.train_transform)
        deserialized = pickle.loads(serialized)

        self.assertIsNotNone(deserialized(PIL.Image.new('RGB', size=(100, 100))))
