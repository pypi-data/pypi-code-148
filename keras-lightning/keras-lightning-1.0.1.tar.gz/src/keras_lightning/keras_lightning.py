import torch
import pytorch_lightning as pl
from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.callbacks import LearningRateMonitor
from pytorch_lightning.callbacks.progress import TQDMProgressBar
from pytorch_lightning.loggers import CSVLogger
from torch.utils.data import DataLoader, TensorDataset
from torchmetrics import Accuracy, Metric, MetricCollection
import copy
import logging

class KLModel(LightningModule):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def compile(self, optimizer, loss, metrics=None, scheduler=None):
        self.koptimizer = optimizer
        self.loss = loss
        self.metrics = torch.nn.ModuleDict({i: MetricCollection(copy.deepcopy(metrics)) for i in ('train_set', 'val_set', 'test_set')})
        self.kscheduler = scheduler
    
    def configure_optimizers(self):
        # if self.kscheduler:
        #     return [self.koptimizer], [{"scheduler": self.kscheduler, "interval": "epoch"}]
        # else:
        return self.koptimizer

    def forward(self, x):
        with torch.no_grad():
            for parameter in self.parameters():
                if parameter.requires_grad:
                    parameter.clamp_(-1, 1)
        return self.model(x)
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        output = self(x)
        loss = self.loss(output, y)

        with torch.no_grad():
            for metric_name, metric in self.metrics['train_set'].items():
                metric.update(output, y)
                self.log(metric_name, metric.compute(), prog_bar=True)
            if self.kscheduler:
                self.log('lr', self.kscheduler.get_lr()[0], prog_bar=True)

        return loss

    def training_epoch_end(self, training_step_outputs):
        for metric_name, metric in self.metrics['train_set'].items():
            metric.reset()
        if self.kscheduler:
            self.kscheduler.step()

    def validation_step(self, batch, batch_idx):
        x, y = batch
        output = self(x)
        loss = self.loss(output, y)
        self.log("val_loss", loss, prog_bar=True)

        for metric_name, metric in self.metrics['val_set'].items():
            metric.update(output, y)
            self.log(f"val_{metric_name}", metric.compute(), prog_bar=True)

    def validation_epoch_end(self, validation_step_outputs):
        for metric_name, metric in self.metrics['val_set'].items():
            metric.reset()
        # print()

    def test_step(self, batch, batch_idx):
        x, y = batch
        output = self(x)
        loss = self.loss(output, y)
        self.log("test_loss", loss, prog_bar=True)

        for metric_name, metric in self.metrics['test_set'].items():
            metric.update(output, y)
            self.log(f"test_{metric_name}", metric.compute(), prog_bar=True)

    def fit(self, x_train=None, y_train=None, x_val=None, y_val=None, x_test=None, y_test=None,
            batch_size=32, epochs=1, dataset_train=None, dataset_val=None, dataset_test=None, 
            shuffle=True, verbose=True, **kwargs):


        if x_train is not None and y_train is not None:
            self.dataset_train = TensorDataset(torch.tensor(x_train), torch.tensor(y_train))
        elif dataset_train is not None:
            self.dataset_train = dataset_train
        else:
            raise "No training set provided."

        if x_val is not None and y_val is not None:
            self.dataset_val = TensorDataset(torch.tensor(x_val), torch.tensor(y_val))
        elif dataset_val is not None:
            self.dataset_val = dataset_val
        else:
            self.dataset_val = None

        if x_test is not None and y_test is not None:
            self.dataset_test = TensorDataset(torch.tensor(x_test), torch.tensor(y_test))
        elif dataset_test is not None:
            self.dataset_test = dataset_test
        else:
            self.dataset_test = None

        self.batch_size = batch_size

        if verbose:
            logging.getLogger("pytorch_lightning").setLevel(logging.NOTSET)
        else:
            logging.getLogger("pytorch_lightning").setLevel(100)

        trainer = Trainer(
            accelerator = kwargs.pop('enable_checkpointing', 'auto'),
            devices = kwargs.pop('devices', torch.cuda.device_count()) if torch.cuda.is_available() else None,
            max_epochs = epochs,
            callbacks = kwargs.pop('callbacks', [
               TQDMProgressBar(refresh_rate=20),
               pl.callbacks.ModelSummary(max_depth=2),
            ]) if verbose else None,
            enable_checkpointing = kwargs.pop('enable_checkpointing', False),
            logger = kwargs.pop('logger', False),
            enable_model_summary = True if verbose else False,
            enable_progress_bar=True if verbose else False,
            **kwargs,
        )

        if self.dataset_val is not None:
            trainer.fit(self, DataLoader(self.dataset_train, batch_size=batch_size, shuffle=shuffle), DataLoader(self.dataset_val, batch_size=batch_size))
        else:
            trainer.fit(self, DataLoader(self.dataset_train, batch_size=batch_size))

        results = None

        if self.dataset_test is not None:
            results = trainer.test(self, dataloaders=DataLoader(self.dataset_test, batch_size=batch_size), verbose=verbose)[0]

        return results


class SparseCategoricalAccuracy(Metric):
    def __init__(self):
        super().__init__()
        self.add_state("correct", default=torch.tensor(0), dist_reduce_fx="sum")
        self.add_state("total", default=torch.tensor(0), dist_reduce_fx="sum")

    def update(self, output: torch.Tensor, target: torch.Tensor):
        preds = torch.argmax(output, dim=1)
        assert preds.shape == target.shape

        self.correct += torch.sum(preds == target)
        self.total += target.numel()

    def compute(self):
        return self.correct.float() / self.total
