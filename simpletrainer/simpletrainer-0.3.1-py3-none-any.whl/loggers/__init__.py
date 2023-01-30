from simpletrainer.loggers.base import DeepLearningLogger
from simpletrainer.loggers.mlflow import MlflowLogger
from simpletrainer.loggers.registry import DeepLearningLoggerRegistry
from simpletrainer.loggers.tensorboard import TensorboardLogger
from simpletrainer.loggers.wandb import WandbLogger

__all__ = [
    'DeepLearningLogger',
    'MlflowLogger',
    'TensorboardLogger',
    'WandbLogger',
    'DeepLearningLoggerRegistry',
]
