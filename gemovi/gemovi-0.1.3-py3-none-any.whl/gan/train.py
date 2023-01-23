import copy
import os
from pathlib import Path

import pytorch_lightning as pl
from pytorch_lightning.callbacks import (
    EarlyStopping,
    LearningRateMonitor,
    ModelCheckpoint,
)
from pytorch_lightning.loggers import TensorBoardLogger

from gemovi.common.dataset import LitGMVLoader
from gemovi.common.utils import get_config, try_fire_cli, update_config_from_kwargs
from gemovi.gan.trainer import GANTrainerState


def main(
    config="model_defaults.yaml",
    # TODO: Once other GANs are implemented, this should be ``None`` by default
    model_class="DCGAN",
    **kwargs,
):
    """
    Generic runner for GAN models.

    Parameters
    ----------
    config
        path to the config file
    model_class
        GAN class to train; currently only DCGAN is supported
    kwargs
        additional keyword arguments to override config file
    """
    if isinstance(config, (str, Path)):
        config = get_config(config)
    config = update_config_from_kwargs(config, **kwargs)

    # Seed everything for reproducibility
    pl.seed_everything(config["exp_params"]["manual_seed"], True)

    trainer_params = config["trainer_params"]
    data_params = config["data_params"]
    if model_class is not None:
        trainer_params["model_name"] = model_class
    to_log = copy.deepcopy(config)

    name = trainer_params.pop("model_name", model_class)
    ckpt_path = trainer_params.pop("ckpt_path", None)

    log_dir = config["trainer_params"].pop("log_dir").format(framework="lightning")
    tb_logger = TensorBoardLogger(save_dir=log_dir, name=name)
    tb_logger.log_hyperparams(to_log)

    # TODO: This needs modification once multiple forms of GANs are implemented
    model_state = GANTrainerState(**config["model_params"][name])

    patience = trainer_params.pop("early_stopping_patience", 10)
    trainer_engine = pl.Trainer(
        logger=tb_logger,
        log_every_n_steps=2,
        callbacks=[
            LearningRateMonitor(),
            ModelCheckpoint(
                save_top_k=trainer_params["max_epochs"],
                dirpath=os.path.join(tb_logger.log_dir, "checkpoints"),
                monitor="val_loss",
                save_last=True,
                every_n_epochs=1,
                filename="{val_loss:.4f}-{epoch}-{step}",
            ),
            EarlyStopping(monitor="val_loss", patience=patience),
        ],
        **trainer_params,
    )

    loader = LitGMVLoader(**data_params, pin_memory=len(trainer_params["devices"]) != 0)
    Path(f"{tb_logger.log_dir}/Samples").mkdir(exist_ok=True, parents=True)

    print(f"======= Training {name} =======")
    trainer_engine.fit(model_state, loader, ckpt_path=ckpt_path)


def main_cli():
    try_fire_cli(main)


if __name__ == "__main__":
    main_cli()
