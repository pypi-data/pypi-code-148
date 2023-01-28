import colorlog
import logging
import boto3  # currently only supports S3
import os
import time
import uuid
import warnings
import lightgbm as lgb
import xgboost as xgb

from abc import ABC, abstractmethod
from catboost import CatBoostRanker
from urllib.parse import urlparse
from .version import __version__

DATE_FMT = "%Y-%m-%d"

_DEFAULT_LOG_FMT = "%(log_color)s[%(levelname)s %(asctime)s.%(msecs)03d %(name)s]:%(reset)s %(message)s"
_DEFAULT_LOG_DATE_FMT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str, fmt: str = None, dt_fmt: str = None) -> logging.Logger:
    if fmt is None:
        fmt = _DEFAULT_LOG_FMT
    if dt_fmt is None:
        dt_fmt = _DEFAULT_LOG_DATE_FMT

    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(fmt, dt_fmt))
    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)
    logger.propogate = False
    return logger


logger = get_logger("bst-wrapper")


class BoosterWrapper(ABC):
    def __init__(
        self,
        model_path: str,
    ):
        self.model_path = model_path
        self.booster = self.load_model(model_path)

    def __getstate__(self):
        return self.model_path

    def _get_bucket_and_prefix(self, s3_path: str):
        parsed = urlparse(s3_path)
        return parsed.netloc, parsed.path[1:]

    def __setstate__(self, model_path: str):
        self.model_path = model_path
        self.booster = self.load_model(model_path)

    def _download_and_return_path(self, model_path: str) -> str:
        model_path = model_path.rstrip("/")
        suffix = os.path.basename(model_path).split(".")[-1]
        local_model_path = f"/tmp/bst-model-{uuid.uuid4().hex}.{suffix}"
        logger.warning("Downloading model file@%s to: %s", model_path, local_model_path)
        bucket, prefix = self._get_bucket_and_prefix(model_path)
        client = boto3.client("s3")
        client.download_file(bucket, prefix, local_model_path)
        return local_model_path

    @abstractmethod
    def load_model(self, model_path: str):
        pass


class LGBWrapper(BoosterWrapper):
    def load_model(self, model_path: str) -> lgb.Booster:
        model_path = self._download_and_return_path(model_path)
        logger.warning("Loading model file@%s", model_path)
        return lgb.Booster(model_file=model_path)


class CatBoostWrapper(BoosterWrapper):
    def load_model(self, model_path: str) -> CatBoostRanker:
        model_path = self._download_and_return_path(model_path)
        logger.warning("Loading model file@%s", model_path)
        model = CatBoostRanker()
        model.load_model(model_path, "json")
        return model


class XGBoostWrapper(BoosterWrapper):
    def load_model(self, model_path: str) -> xgb.Booster:
        model_path = self._download_and_return_path(model_path)
        logger.warning("Loading model file@%s", model_path)
        bst = xgb.Booster()
        bst.load_model(model_path)
        return bst
