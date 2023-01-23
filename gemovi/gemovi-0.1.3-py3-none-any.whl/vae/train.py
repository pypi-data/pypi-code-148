import copy
import os
import sys
from pathlib import Path

from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import (
    EarlyStopping,
    LearningRateMonitor,
    ModelCheckpoint,
)
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.strategies.ddp import DDPStrategy
from pytorch_lightning.utilities.seed import seed_everything

from gemovi.common.utils import get_config, try_fire_cli, update_config_from_kwargs
from gemovi.vae.dataset import VAEDataset
from gemovi.vae.experiment import VAEXperiment
from gemovi.vae.models import vae_models


def main(config="model_defaults.yaml", model_class=None, **kwargs):
    """
    Generic runner for VAE models.

    Parameters
    ----------
    config
        path to the config file
    model_class
        VAE class to train, must match a key from gemovi.vae.models.vae_models
    kwargs
        additional keyword arguments to override config file
    """
    if isinstance(config, (str, Path)):
        config = get_config(config)
    config = update_config_from_kwargs(config, **kwargs)
    # Some keys get popped from config below, so save a copy for logging first
    to_log = copy.deepcopy(config)
    train_params = config["trainer_params"]

    if model_class is not None:
        train_params["model_name"] = model_class
    name = train_params.pop("model_name")
    fmt_log_dir = train_params.pop("log_dir").format(framework="lightning")
    tb_logger = TensorBoardLogger(name=name, save_dir=fmt_log_dir)
    tb_logger.log_hyperparams(to_log)

    ckpt_path = train_params.pop("ckpt_path")

    # For reproducibility
    seed_everything(config["exp_params"]["manual_seed"], True)

    model = vae_models[name](**config["model_params"][name])
    experiment = VAEXperiment(model, config["exp_params"])

    data = VAEDataset(
        **config["data_params"],
        pin_memory=len(train_params["devices"]) != 0,
    )
    data.setup()

    strat = {}
    if sys.platform != "win32":
        strat["strategy"] = DDPStrategy(find_unused_parameters=False)

    patience = train_params.pop("early_stopping_patience", 5)
    runner = Trainer(
        logger=tb_logger,
        callbacks=[
            LearningRateMonitor(),
            ModelCheckpoint(
                save_top_k=train_params["max_epochs"],
                dirpath=os.path.join(tb_logger.log_dir, "checkpoints"),
                monitor="val_loss",
                save_last=True,
                every_n_epochs=1,
                filename="{val_loss:.3f}-{epoch}-{step}",
            ),
            EarlyStopping(monitor="val_loss", patience=patience),
        ],
        **strat,
        **train_params,
    )

    Path(f"{tb_logger.log_dir}/Samples").mkdir(exist_ok=True, parents=True)
    Path(f"{tb_logger.log_dir}/Reconstructions").mkdir(exist_ok=True, parents=True)

    print(f"======= Training {name} =======")
    runner.fit(experiment, datamodule=data, ckpt_path=ckpt_path)


def main_cli():
    try_fire_cli(main)


if __name__ == "__main__":
    main_cli()
