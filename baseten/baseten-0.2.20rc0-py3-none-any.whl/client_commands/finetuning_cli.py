import json
import os
from json import JSONDecodeError
from typing import Optional

import click

from baseten.training import (Dataset, DatasetIdentifier, DreamboothConfig,
                              LocalPath, PublicUrl,
                              deploy_model_from_finetuning_run)
from baseten.training import finetune as finetune_api


def _finetune_interactive(finetuning_type: str):
    raise NotImplementedError


def _validate_input_options(input_: Optional[str], input_file: Optional[str]) -> bool:

    if input_ and input_file:
        click.echo("Please provide exactly one of input|input_file")
        return False

    if input_ is None and input_file is None:
        click.echo("Please provide exactly one of input|input_file")
        return False

    if input_file is not None and (not os.path.exists(input_file) or os.path.isdir(input_file)):
        click.echo(f"{input_file} is not a valid file.")
        return False

    return True


def _parse_input_data(params: dict) -> Optional[DatasetIdentifier]:
    if "input_dataset" in params:
        raw_input_data = params["input_dataset"]
    else:
        return None

    if "public_url" in raw_input_data:
        return PublicUrl(raw_input_data["public_url"])

    if "baseten_dataset_id" in raw_input_data:
        return Dataset(raw_input_data["baseten_dataset_id"])

    if "local_path" in raw_input_data:
        if "dataset_name" in raw_input_data:
            return LocalPath(raw_input_data["local_path"], raw_input_data["dataset_name"])
        else:
            click.echo("If using local_path, please also provide a `dataset_name`.")
            return None

    return None


def _finetune_dreambooth(trained_model_name: str, params: dict):
    parsed_input_dataset = _parse_input_data(params)

    if parsed_input_dataset:
        params.update({
            "input_dataset": parsed_input_dataset
        })
        config = DreamboothConfig(**params)
        return finetune_api(trained_model_name, config)
    else:
        click.echo("No valid `input_dataset` provided.")
        return None


@click.command()
@click.option("--interactive/--no-interactive", default=True)
@click.option("--finetuning-type", type=click.Choice(['DREAMBOOTH', 'CLASSIC_STABLE_DIFFUSION']), required=True)
@click.option("--trained-model-name", required=True)
@click.option("--input-file", required=False)
@click.option("--input", "input_", required=False)
def finetune(interactive: bool, finetuning_type: str, trained_model_name: str, input_file: str, input_: str):
    """
    CLI for triggering fine-tunng jobs.
    """
    if interactive:
        click.echo("Starting interactive finetuning flow.")
        _finetune_interactive(finetuning_type)
    else:
        if _validate_input_options(input_, input_file):
            # TODO: Take input or input file, parse it into a dict. Handle the input_data piece, and
            # construct a Dreambooth config object.
            if input_file:
                input_ = open(input_file, "r").read()

            try:
                parsed_json = json.loads(input_)
            except JSONDecodeError as error:
                click.echo("Could not parse JSON.")
                click.echo(str(error))
                return

            if finetuning_type == 'DREAMBOOTH':
                training_run = _finetune_dreambooth(trained_model_name, parsed_json)
                if training_run:
                    click.echo(f"Started training run: {training_run.id}")


@click.command()
@click.option("--training-run-id", required=True)
@click.option("--idle-time-minutes", required=True)
def deploy_from_finetuning_run(training_run_id, idle_time_minutes):
    """
    """
    deployed_model = deploy_model_from_finetuning_run(training_run_id, idle_time_minutes)
    # TODO (Sid): replace ID with link
    click.echo(f"Deploying trained model: {deployed_model.id}...")
