import logging
from typing import Dict, Iterable, List, Optional, Tuple, Union

import torch
from clearml import Task
from fastprogress import master_bar
from torch.cuda.amp import GradScaler
from torch.optim.lr_scheduler import _LRScheduler

from vtorch.data.entity import InstanceFeatureVectors
from vtorch.data.iterators import DataIterator
from vtorch.metrics import Metric
from vtorch.models.model import IModel
from vtorch.training import Trainer

logger = logging.getLogger(__name__)


class TrainerWithSeparateValidations(Trainer):

    validation_dataset: Optional[Dict[str, List[InstanceFeatureVectors]]]

    def __init__(
        self,
        model: IModel,
        optimizer: torch.optim.Optimizer,  # type: ignore
        metrics: Dict[str, Metric],
        label_keys: Tuple[str, Union[str, List[str]]],
        iterator: DataIterator,
        train_dataset: Iterable[InstanceFeatureVectors],
        num_epochs: int,
        shuffle: bool = True,
        validation_dataset: Optional[Dict[str, List[InstanceFeatureVectors]]] = None,
        validation_iterator: Optional[DataIterator] = None,
        early_stopping: bool = False,
        patience: Optional[int] = None,
        early_stopping_metric_name: str = "loss",
        early_stopping_metric_should_decrease: bool = True,
        accumulation_steps: int = 1,
        cuda_device: Union[int, List[int]] = -1,
        grad_norm: Optional[float] = 1.0,
        lr_scheduler: Optional[_LRScheduler] = None,
        scaler: Optional[GradScaler] = None,
        gradual_unfreezing_steps: Optional[List[List[str]]] = None,
        run_validation_each_global_steps: Optional[int] = None,
        clearml_task: Optional[Task] = None,
        seed: int = 12,
    ) -> None:
        super().__init__(
            model=model,
            optimizer=optimizer,
            metrics=metrics,
            label_keys=label_keys,
            iterator=iterator,
            train_dataset=train_dataset,
            num_epochs=num_epochs,
            shuffle=shuffle,
            validation_dataset=validation_dataset,  # type: ignore
            validation_iterator=validation_iterator,
            early_stopping=early_stopping,
            patience=patience,
            early_stopping_metric_name=early_stopping_metric_name,
            early_stopping_metric_should_decrease=early_stopping_metric_should_decrease,
            accumulation_steps=accumulation_steps,
            cuda_device=cuda_device,
            grad_norm=grad_norm,
            lr_scheduler=lr_scheduler,
            scaler=scaler,
            gradual_unfreezing_steps=gradual_unfreezing_steps,
            run_validation_each_global_steps=run_validation_each_global_steps,
            clearml_task=clearml_task,
            seed=seed,
        )

    def _validation_run(self, master_bar_logger: master_bar, global_steps: int = 0) -> Optional[Dict[str, float]]:
        """
        Computes the validation metrics. Returns it and the number of batches.
        """
        if self.validation_data is None:
            return None

        logger.info("Validating")

        with torch.no_grad():
            self._eval_mode()

            for validation_name, validation_data in self.validation_data.items():  # type: ignore

                batches_this_epoch = 0
                val_loss = 0
                for batch_group in self._configure_batch_iterator(
                    iterator=self.validation_iterator,
                    data=validation_data,
                    master_bar_logger=master_bar_logger,
                    shuffle=False,
                ):
                    outputs, loss = self._batch_outputs_and_loss(batch_group)
                    self._calculate_metrics(outputs=outputs, batch_group=batch_group)
                    batches_this_epoch += 1
                    val_loss += loss.cpu().numpy()

                val_metrics: Dict[str, float] = self._form_metric_dict(
                    total_loss=val_loss, num_batches=batches_this_epoch, reset=True
                )

                for metric_name, metric_value in val_metrics.items():
                    metric_name = f"{validation_name}_{metric_name}"
                    self.callbacks.clearml_report_scalar(
                        title="Validation", series=metric_name, value=metric_value, iteration=global_steps
                    )

        return val_metrics  # just last validation will be taken into account
