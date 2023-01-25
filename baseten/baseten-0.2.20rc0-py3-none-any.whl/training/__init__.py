import base64
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, List, Optional

from baseten.baseten_deployed_model import BasetenDeployedModel
from baseten.common.api import (deploy_from_training_run, finetune_zoo_model,
                                get_training_dataset)
from baseten.common.api import get_training_run as get_training_run_api
from baseten.common.files import DatasetTrainingType, upload_dataset

logger = logging.getLogger(__name__)


def _bin_transform_str(s: str, transform_fn) -> str:
    return transform_fn(s.encode("utf-8")).decode("utf-8")


class Base64Codec:
    def encode(self, s: str) -> str:
        return _bin_transform_str(s, base64.b64encode)

    def decode(self, s: str) -> str:
        return _bin_transform_str(s, base64.b64decode)


Base64 = Base64Codec()


def encode_base64_json(obj: Any) -> str:
    return Base64.encode(json.dumps(obj))


class DatasetIdentifier(ABC):

    @abstractmethod
    def resolve_dataset_url(self, training_type: DatasetTrainingType) -> str:
        """
        Method that returns a URL from which the training job can download
        a training dataset.
        """


class Dataset(DatasetIdentifier):
    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id

    def resolve_dataset_url(self, training_type: DatasetTrainingType) -> str:
        training_dataset = get_training_dataset(dataset_id=self.dataset_id)
        return training_dataset["presigned_s3_get_url"]


class LocalPath(DatasetIdentifier):
    def __init__(self, path: Path, dataset_name: str):
        self.path = path
        self.dataset_name = dataset_name

    def resolve_dataset_url(self, training_type: DatasetTrainingType) -> str:
        dataset_id = upload_dataset(self.dataset_name, self.path, training_type=training_type)
        training_dataset = get_training_dataset(dataset_id=dataset_id)

        return training_dataset["presigned_s3_get_url"]


class PublicUrl(DatasetIdentifier):
    def __init__(self, url: str):
        self.url = url

    def resolve_dataset_url(self, training_type: DatasetTrainingType) -> str:
        return self.url


class FinetuningConfig(ABC):
    """
    Base abstract class for defining fine tuning configs. Each new fine-tuning
    algorithm that we support must support a subclass of this.

    Each fine-tuning algorithm will have a different set of variables that
    need to be provided.
    """

    @property
    @abstractmethod
    def dataset_training_type(self) -> DatasetTrainingType:
        """
        The dataset training type associated with this config type.
        """

    @property
    @abstractmethod
    def training_truss_name(self) -> str:
        """
        The name of the truss associated with this config.
        """

    @abstractmethod
    def resolve_fine_tuning_variables(self) -> dict:
        """
        Method that must be implemented that returns a variables dictionary
        for this type of FineTuning configuration.
        """


@dataclass
class DreamboothConfig(FinetuningConfig):
    """
    Fine-tuning config for Dreambooth fine-tuning with Stable Diffusion.
    """

    instance_prompt: str
    input_dataset: DatasetIdentifier
    wandb_api_key: str

    pretrained_model_name_or_path: Optional[str] = None
    revision: Optional[str] = None
    tokenizer_name: Optional[str] = None

    class_prompt: Optional[str] = None
    with_prior_preservation: Optional[bool] = None

    prior_loss_weight: Optional[float] = None
    num_class_images: Optional[int] = None
    seed: Optional[int] = None
    resolution: Optional[int] = None
    center_crop: Optional[bool] = None
    train_text_encoder: Optional[bool] = None
    train_batch_size: Optional[int] = None
    sample_batch_size: Optional[int] = None
    num_train_epochs: Optional[int] = None
    max_train_steps: Optional[int] = None
    gradient_accumulation_steps: Optional[int] = None
    learning_rate: Optional[float] = None
    lr_scheduler: Optional[str] = None
    lr_warmup_steps: Optional[int] = None
    adam_beta1: Optional[float] = None
    adam_beta2: Optional[float] = None
    adam_weight_decay: Optional[float] = None
    adam_epsilon: Optional[float] = None
    max_grad_norm: Optional[float] = None
    mixed_precision: Optional[str] = None

    def _resolve_dataset(self) -> str:
        return self.input_dataset.resolve_dataset_url(training_type=self.dataset_training_type)

    def resolve_fine_tuning_variables(self) -> dict:
        """
        Returns fine-tuning variables dict to send when triggering the fine-tuning
        job. The dataset URLs here are resolved to S3 URLs.
        """
        resolved_variables = asdict(self)

        resolved_variables.update({
            "dataset_zip_url": self._resolve_dataset()
        })

        del resolved_variables["input_dataset"]

        return {key: value for key, value in resolved_variables.items() if value is not None}

    @property
    def training_truss_name(self) -> str:
        return "dreambooth"

    @property
    def dataset_training_type(self) -> DatasetTrainingType:
        return DatasetTrainingType.DREAMBOOTH


# Classes to support returning logs
@dataclass
class LogLine:
    """
    Wrapper for log lines.
    """
    timestamp: int
    level: str
    msg: str


class FinetuningRun:
    """
    Class to represent a single finetuning run.
    """

    def __init__(
        self,
        id: str,
    ):
        self.id = id
        self.refresh()

    def logs(self, cursor: Optional[int] = None, limit: Optional[int] = None) -> List[LogLine]:
        """
        Returns logs for the training run, with pagination.
        """

        # TODO: * Write API function for fetching logs
        raise NotImplementedError

    def refresh(self):
        """
        Re-fetch training data from the server.
        """
        training_run_data = get_training_run_api(self.id)

        # TODO (Sid): Handle case of training run not found

        self.status = training_run_data["status"]
        self.created = training_run_data["created"]
        self.trained_model_name = training_run_data["trained_model_name"]

        self.variables = {
            variable["key"]: variable["value"]
            for variable in training_run_data["variables"]
        }


def finetune(trained_model_name: str, fine_tuning_config: FinetuningConfig) -> FinetuningRun:
    """
    Kick off a fine-tuning job.
    """
    variables_dict = fine_tuning_config.resolve_fine_tuning_variables()
    encoded_variables = encode_base64_json(variables_dict)

    logger.info(f"Starting fine-tuning of {fine_tuning_config.training_truss_name}")

    training_run_id = finetune_zoo_model(trained_model_name, fine_tuning_config.training_truss_name, encoded_variables)
    return FinetuningRun(training_run_id)


def get_finetuning_run(id: str) -> FinetuningRun:
    """
    Fetch a Finetuning Run from the server
    """
    return FinetuningRun(id)


def deploy_model_from_finetuning_run(training_run_id: str, idle_time_minutes: int) -> BasetenDeployedModel:
    """
    Deploy a model from a current training run.
    """
    training_run = FinetuningRun(training_run_id)
    model_id, model_version_id = deploy_from_training_run(
        training_run_id=training_run.id,
        name=training_run.trained_model_name,
        idle_time_minutes=idle_time_minutes
    )

    return BasetenDeployedModel(model_id=model_id, model_version_id=model_version_id)
