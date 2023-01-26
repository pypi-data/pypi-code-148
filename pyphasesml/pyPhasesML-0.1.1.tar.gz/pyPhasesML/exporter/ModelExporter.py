import importlib
from pathlib import Path

from pyPhases.Data import DataNotFound
from pyPhases.exporter.DataExporter import DataExporter
from pyPhases.util.Logger import Logger

from ..Model import Model

if importlib.util.find_spec("torch"):
    import torch
    
    if importlib.util.find_spec("tensorflow"):
        print(u"\033[31;1;4m%s\033[0mTensorflow and PyTorch are installed in the same enviroment, only one model (PyTorch) can be exported/imported")

    class ModelExporter(DataExporter):
        includesStorage = True

        def initialOptions(self):

            return {"basePath": "data/"}

        def getPath(self, dataId):
            return self.getOption("basePath") + dataId

        def checkType(self, expectedType):

            return issubclass(expectedType, torch.nn.Module) or issubclass(expectedType, Model)

        def importData(self, dataId, options={}):
            try:
                deviceName = "cuda" if torch.cuda.is_available() else "cpu"
                return torch.load(self.getPath(dataId), map_location=torch.device(deviceName))
            except FileNotFoundError:
                raise DataNotFound()

        def exportDataId(self, dataId, model):
            torch.save(model.state_dict(), self.getPath(dataId))


elif importlib.util.find_spec("tensorflow"):
    if importlib.util.find_spec("tensorflow.keras"):
        from tensorflow.keras import models
        from tensorflow.python.keras.engine.functional import Functional

    elif importlib.util.find_spec("keras"):
        from keras import models

        Functional = False

    class ModelExporter(DataExporter):
        includesStorage = True

        def initialOptions(self):

            return {"basePath": "data/"}

        def getPath(self, dataId):
            return self.getOption("basePath") + dataId

        def checkType(self, expectedType):
            funcCheck = issubclass(expectedType, Functional) if Functional is not None else False
            return issubclass(expectedType, models.Sequential) or issubclass(expectedType, Model) or funcCheck

        def importData(self, dataId, options={}):
            path = self.getPath(dataId)
            if not Path("%s.index" % path).exists():
                raise DataNotFound()
            return path

        def exportDataId(self, dataId, model):
            model.save_weights(self.getPath(dataId))
else:
    raise Exception("No supported ModelExporter located (Supported: pytorch/tensorflow)")
