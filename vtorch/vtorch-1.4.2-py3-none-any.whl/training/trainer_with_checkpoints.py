import logging
import os
import pickle
import random
import shutil
from copy import deepcopy
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
import torch
from clearml import Task
from fastprogress import master_bar
from torch.cuda.amp import GradScaler
from torch.optim.lr_scheduler import _LRScheduler

from vtorch.common.checks import ConfigurationError
from vtorch.common.utils import set_seed
from vtorch.data.iterators.base import InstanceFeatureVectors
from vtorch.data.iterators.interruptable import InterruptableDataIterator
from vtorch.metrics import Metric
from vtorch.models.model import IModel
from vtorch.nn import utils as nn_util

from . import Trainer

logger = logging.getLogger(__name__)


class RandomStateManager:
    def __init__(self, seed: int, n_gpu: int) -> None:
        self.seed = seed
        self.n_gpu = n_gpu
        self.python_random_state: Optional[Tuple[int, Tuple[int, ...], Optional[float]]] = None
        self.numpy_random_state: Optional[Tuple[Tuple[str, np.ndarray, int, int, float], Dict[str, Any]]] = None
        self.torch_random_state: Optional[torch.Tensor] = None
        self.torch_cuda_all_random_state: Optional[List[torch.Tensor]] = None

    def state_dict(self) -> Dict[str, Any]:
        self.python_random_state = random.getstate()  # type: ignore
        self.numpy_random_state = np.random.get_state()
        self.torch_random_state = torch.random.get_rng_state()
        self.torch_cuda_all_random_state = torch.cuda.get_rng_state_all()
        return self.__dict__

    def set_state(self) -> None:
        if any(v is None for v in self.__dict__.values()):
            set_seed(self.seed, self.n_gpu)
        else:
            random.setstate(self.python_random_state)
            np.random.set_state(self.numpy_random_state)
            torch.random.set_rng_state(self.torch_random_state)
            torch.cuda.set_rng_state_all(self.torch_cuda_all_random_state)

    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        for key, val in state_dict.items():
            self.__setattr__(key, val)


class TrainerWithCheckpoints(Trainer):

    FIELDS_TO_SAVE = [
        "best_model",
        "callbacks",
        "model",
        "optimizer",
        "iterator",
        "scaler",
        "lr_scheduler",
        "current_epoch",
        "global_steps",
        "random_state_manager",
        # "validation_iterator",  # This is excluded due to validation iterators most likely being static anyway
    ]

    def __init__(
        self,
        model: IModel,
        optimizer: torch.optim.Optimizer,  # type: ignore
        metrics: Dict[str, Metric],
        label_keys: Tuple[str, Union[str, List[str]]],
        iterator: InterruptableDataIterator,
        train_dataset: Iterable[InstanceFeatureVectors],
        num_epochs: int,
        shuffle: bool = True,
        validation_dataset: Optional[Iterable[InstanceFeatureVectors]] = None,
        validation_iterator: Optional[InterruptableDataIterator] = None,
        early_stopping: bool = False,
        patience: Optional[int] = None,
        early_stopping_metric_name: str = "loss",
        early_stopping_metric_should_decrease: bool = True,
        accumulation_steps: int = 1,
        cuda_device: Union[int, List[int]] = -1,
        grad_norm: Optional[float] = 1.0,
        lr_scheduler: Optional[_LRScheduler] = None,  # type: ignore
        scaler: Optional[GradScaler] = None,
        gradual_unfreezing_steps: Optional[List[List[str]]] = None,
        clearml_task: Optional[Task] = None,
        seed: int = 12,
        n_checkpoints_to_keep: int = 2,
        n_global_steps_per_checkpoint: int = 10000,
        checkpoint_folder_path: Optional[str] = None,
    ) -> None:
        """
        A trainer for doing supervised learning. It just takes a labeled dataset
        and a ``DataIterator``, and uses the supplied ``Optimizer`` to learn the weights
        for your model over some fixed number of epochs. You can also pass in a validation
        dataset and enable early stopping. There are many other bells and whistles as well.

        Parameters
        ----------
        model : ``Model``, required.
            An Vtorch model to be optimized. Pytorch Modules can also be optimized if
            their ``forward`` method returns a dictionary with a "loss" key, containing a
            scalar tensor representing the loss function to be optimized.
            If you are training your model using GPUs, your model should already be
            on the correct device.
        optimizer : ``torch.nn.Optimizer``, required.
            An instance of a Pytorch Optimizer, instantiated with the parameters of the
            model to be optimized.
        iterator : ``DataIterator``, required.
            A method for iterating over a ``Dataset``, yielding padded indexed batches.
        train_dataset : ``Dataset``, required.
            A ``Dataset`` to train on. The dataset should have already been indexed.
        validation_dataset : ``Dataset``, optional, (default = None).
            A ``Dataset`` to evaluate on. The dataset should have already been indexed.
        patience : Optional[int] > 0, optional (default=None)
            Number of epochs to be patient before early stopping: the training is stopped
            after ``patience`` epochs with no improvement. If given, it must be ``> 0``.
            If None, early stopping is disabled.
        validation_iterator : ``DataIterator``, optional (default=None)
            An iterator to use for the validation set.  If ``None``, then
            use the training `iterator`.
        shuffle : ``bool``, optional (default=True)
            Whether to shuffle the instances in the iterator or not.
        num_epochs : int, optional (default = 20)
            Number of training epochs.
        accumulation_steps : int, optional (default = 0)
            Number of training steps to accumulate gradients
        cuda_device : ``Union[int, List[int]]``, optional (default = -1)
            An integer or list of integers specifying the CUDA device(s) to use. If -1, the CPU is used.
        grad_norm : ``float``, optional, (default = None).
            If provided, gradient norms will be rescaled to have a maximum of this value.
        clearml_task: ``Task``, optional  (default = None)
        """
        if isinstance(cuda_device, list) and len(cuda_device) > 1:
            raise NotImplementedError("Distributed training is not supported")

        if patience is not None and (not isinstance(patience, int) or patience <= 0):
            raise ConfigurationError(
                f'{patience} is an invalid value for "patience": it must be a positive integer '
                "or None (if you want to disable early stopping)"
            )

        super().__init__(
            model=model,
            optimizer=optimizer,
            metrics=metrics,
            label_keys=label_keys,
            iterator=iterator,
            train_dataset=train_dataset,
            num_epochs=num_epochs,
            shuffle=shuffle,
            validation_dataset=validation_dataset,
            validation_iterator=validation_iterator or deepcopy(iterator),
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
            run_validation_each_global_steps=None,
            clearml_task=clearml_task,
            seed=seed,
        )

        self.n_checkpoints_to_keep = n_checkpoints_to_keep
        self.n_global_steps_per_checkpoint = n_global_steps_per_checkpoint
        self._checkpoint_folder_path = checkpoint_folder_path

        self.best_model: IModel = model
        self.current_epoch: int = 0
        self.global_steps: int = 0
        self.random_state_manager = RandomStateManager(self.seed, len(self._cuda_devices))

        self.__try_recovery()

    @property
    def checkpoint_folder_path(self) -> Optional[str]:
        return self._checkpoint_folder_path

    @checkpoint_folder_path.setter
    def checkpoint_folder_path(self, checkpoints_folder_path: str) -> None:
        self._checkpoint_folder_path = checkpoints_folder_path
        self.__try_recovery()

    def __get_sorted_checkpoint_names(self) -> List[str]:
        return list(
            sorted(
                [folder for folder in os.listdir(self.checkpoint_folder_path) if "checkpoint" in folder],
                key=lambda x: int(x.replace("checkpoint_", "")),
            )
        )

    def __load_checkpoint(self, full_checkpoint_folder_path: str) -> bool:
        field = None
        recovered_field_state_dicts: Dict[str, Any] = {}
        try:
            for field in self.FIELDS_TO_SAVE:
                with open(os.path.join(full_checkpoint_folder_path, f"{field}_state_dict.p"), "rb") as f:
                    recovered_field_state_dicts[field] = pickle.load(f)

            for field, data in recovered_field_state_dicts.items():
                if hasattr(self.__dict__[field], "load_state_dict"):
                    self.__dict__[field].load_state_dict(data)
                    self.__dict__[field] = nn_util.move_to_device(self.__dict__[field], self._cuda_devices[0])
                else:
                    self.__dict__[field] = data
        except Exception:
            logger.exception(
                f"There was an error with recovering {field} for checkpoint {full_checkpoint_folder_path}"
            )
            return False
        return True

    def __try_recovery(self) -> None:
        """
        Will look for a last completed checkpoint and try to recover from it.
        """
        if self.checkpoint_folder_path is None or not os.path.exists(self.checkpoint_folder_path):
            return
        if os.path.exists(os.path.join(self.checkpoint_folder_path, "completed.txt")):
            logger.info("The training has already been finished.")
            exit(0)
        checkpoints = self.__get_sorted_checkpoint_names()
        if len(checkpoints) == 0:
            logger.info("The checkpoints folder exists, but it's empty. Starting a new training run")
            return

        for checkpoint in reversed(checkpoints):
            last_checkpoint_folder = os.path.join(self.checkpoint_folder_path, checkpoint)
            if self.__load_checkpoint(last_checkpoint_folder):
                logger.info(f"The Trainer has been successfully recovered from {checkpoint}")
                return
        logger.error(f"All of the checkpoints in {self.checkpoint_folder_path} are invalid. Not be able to recover.")

    def __write_checkpoint(self) -> None:
        """
        Will save the current state to a checkpoint folder.
        """
        if self.checkpoint_folder_path is None:
            return
        if not os.path.exists(self.checkpoint_folder_path):
            os.makedirs(self.checkpoint_folder_path)
        checkpoints = self.__get_sorted_checkpoint_names()
        if not checkpoints:
            new_checkpoint_folder = os.path.join(self.checkpoint_folder_path, "checkpoint_0")
        else:
            last_checkpoint_n = int(checkpoints[-1].replace("checkpoint_", ""))
            new_checkpoint_folder = os.path.join(self.checkpoint_folder_path, f"checkpoint_{last_checkpoint_n+1}")
        os.makedirs(new_checkpoint_folder)
        for field in self.FIELDS_TO_SAVE:
            with open(os.path.join(new_checkpoint_folder, f"{field}_state_dict.p"), "wb") as f:
                if hasattr(self.__dict__[field], "state_dict"):
                    data_to_save = self.__dict__[field].state_dict()
                else:
                    data_to_save = self.__dict__[field]
                pickle.dump(data_to_save, f)

        if len(checkpoints) >= self.n_checkpoints_to_keep:
            shutil.rmtree(os.path.join(self.checkpoint_folder_path, checkpoints[0]))

    def __write_final(self) -> None:
        """
        Will indicate that the training process is finished and this needs to no longer be loaded
        """
        if self.checkpoint_folder_path is None:
            return
        with open(os.path.join(self.checkpoint_folder_path, "completed.txt"), "w") as f:
            f.write("True")

    def _train_epoch(self, master_bar_logger: master_bar) -> Dict[str, float]:  # type: ignore
        """
        Trains one epoch and returns metrics.
        """
        train_loss = 0.0
        # Set the model to "train" mode.
        self._train_mode()

        batches_this_epoch = 0

        for batch_group in self._configure_batch_iterator(
            iterator=self.iterator, data=self.train_data, master_bar_logger=master_bar_logger
        ):
            batches_this_epoch += 1

            outputs, loss = self._batch_outputs_and_loss(batch_group)
            self._calculate_metrics(outputs=outputs, batch_group=batch_group)

            if torch.isnan(loss):
                raise ValueError("nan loss encountered")

            self._backward(loss)

            train_loss += loss.item()
            if batches_this_epoch % self.accumulation_steps == 0:
                self._step()
                self.model.zero_grad()

                self.callbacks.clearml_report_scalar(
                    title="Training", series="loss", value=loss.item(), iteration=self.global_steps
                )

            self.global_steps += 1

            if (
                self.n_global_steps_per_checkpoint is not None
                and self.global_steps % self.n_global_steps_per_checkpoint == 0
            ):
                self._validation_run(master_bar_logger=master_bar_logger, global_steps=self.global_steps)
                self.__write_checkpoint()
                self._train_mode()

            master_bar_logger.child.comment = "loss: {:.4f}".format(train_loss / batches_this_epoch)

        return self._form_metric_dict(total_loss=train_loss, num_batches=batches_this_epoch, reset=True)

    def train(self) -> IModel:
        """
        Trains the supplied model with the supplied parameters.
        """
        logger.info("Beginning training.")
        mb = master_bar(range(self.current_epoch, self.num_epochs))
        mb.first_bar.comment = f"{self.model.__class__.__name__} training"
        mb_elements = ["epoch"] + [f"train_{metrics_name}" for metrics_name in self.validation_metric_names]
        if self.validation_data is not None:
            mb_elements.extend([f"val_{metrics_name}" for metrics_name in self.validation_metric_names])

        mb.write(mb_elements, table=True)
        self.random_state_manager.set_state()

        self.best_model = self.model
        for epoch in mb:
            self.current_epoch = epoch
            mb_results = [str(epoch)]
            self._gradual_unfreezing(epoch)

            train_metrics = self._train_epoch(mb)
            mb_results.extend(["{:.4f}".format(train_metrics[metric]) for metric in self.validation_metric_names])
            for metric_name, metric_value in train_metrics.items():
                self.callbacks.clearml_report_scalar(
                    title="Training", series=metric_name, value=metric_value, iteration=self.global_steps
                )

            val_metrics = self._validation_run(mb, global_steps=self.global_steps)
            if val_metrics is not None:
                self.callbacks.add_metric(val_metrics)
                mb_results.extend(["{:.4f}".format(val_metrics[metric]) for metric in self.validation_metric_names])

            mb.write(mb_results, table=True)
            self.current_epoch += 1
            self.__write_checkpoint()

            if self.callbacks.should_stop_early():
                break
            elif self.callbacks.is_best_so_far():
                self.best_model = deepcopy(self.model).cpu()  # TODO: This creates a copy on GPU and then moves to RAM
                #  Thus, GPU memory must hold two copies of a single model at once (before dumping to RAM)
                #  Can we copy directly to RAM?
                # https://discuss.pytorch.org/t/copy-best-model-from-gpu-to-cpu/38683

        self.__write_final()
        return self.best_model
