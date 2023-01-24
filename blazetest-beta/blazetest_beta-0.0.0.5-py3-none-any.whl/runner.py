import logging

import click

from blazetest.core.lambda_config import Config
from blazetest.core.license_manager import LicenseManager
from blazetest.core.utils import setup_logging
from blazetest.core.pulumi_manager import PulumiManager

from blazetest.core.tests_runner import TestsRunnerFacade
from blazetest.core.utils import (
    remove_junit_report_path,
    set_aws_credentials,
    create_build_folder,
)
from blazetest import __version__

logger = logging.getLogger(__name__)


@click.command(
    name="pytest-args",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
    help="PyTest Args are passed as a context.",
)
@click.option(
    "--config-path",
    help="Configuration path to the YAML file for the CLI. "
    "If not specified -> searches the project's root folder for the file blazetes.yaml. "
    "If not found -> raises an error.",
)
@click.option(
    "--aws-access-key-id",
    help="AWS Access Key ID which is used to deploy artifacts.",
)
@click.option(
    "--aws-secret-access-key",
    help="AWS Secret Access Key which is used to deploy artifacts.",
)
@click.option(
    "--license-key",
    help="License key for Blazetest CLI. Either --license-key or --license-file should be specified."
    "License key has a higher priority if both are specified.",
)
@click.option(
    "--license-file",
    help="License file for Blazetest CLI. Either --license-key or --license-file should be specified."
    "License file has a lower priority if both are specified.",
)
@click.option(
    "--logs",
    default="enabled",
    type=click.Choice(["enabled", "disabled"]),
    help="Default is enabled. When logs are enabled, they are shown in the console stdout. "
    "When they are set to disabled, the logs are not shown during CLI execution, but saved to blazetest.log, "
    "which will be located in the project's root.",
)
@click.option("--debug", is_flag=True, help="Enables debugging output.")
@click.option("--info", is_flag=True, help="Prints Blazetest CLI version.")
@click.pass_context
def run_tests(
    ctx,
    config_path: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    license_key: str,
    license_file: str,
    logs: str,
    debug: bool,
    info: bool,
):
    """
    Runs tests using the pytest library and parallel Lambda functions.
    It deploys the necessary AWS resources (ECR, Lambda, and S3 bucket) using Pulumi.
    It also accepts any additional arguments passed to the command, which will be passed to pytest as arguments.

    Args:
        ctx (click.core.Context): Pytest Args are passed using context
        config_path (str): Path to the YAML configuration file.
        aws_access_key_id (str): AWS access key id.
        aws_secret_access_key (str): AWS secret access key.
        license_key (str): License key.
        license_file (str): Path to the license file.
        logs (str): Defaults to enabled, possible values: enabled, disabled. If enabled,
            sends logs to Grafana cloud with loki
        debug (bool): flag that enables debugging output if true
        info (bool): prints Blazetest CLI version
    """
    log_to_console = False if logs == "disabled" else True
    setup_logging(debug=debug, stdout_enabled=log_to_console)

    logger.info(f"Blazetest version: {__version__}")

    if info:
        return

    pytest_args = ctx.args
    config = Config.from_yaml(config_path)

    licence_manager = LicenseManager(
        license_key=license_key,
        license_file=license_file,
        config_license_key=config.license_key,
        config_license_file=config.license_file,
    )

    expiration_date = licence_manager.check_license()
    logger.info(f"License expiration date: {expiration_date}")

    # Setting necessary AWS environment variables
    set_aws_credentials(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_region=config.aws_region,
        s3_bucket=config.deploy.s3_bucket,
        ecr_repository_name=config.build.ecr_repository_name,
    )

    # Creating build folder for blazetest files
    create_build_folder()

    # Using Pulumi to do the deployment, create ECR, Lambda and S3 bucket
    pulumi_manager = PulumiManager(
        aws_region=config.aws_region, stack_name=config.deploy.stack_name
    )
    pulumi_manager.deploy()

    # Removing JUnit report path, if present in CLI args
    pytest_args = remove_junit_report_path(pytest_args)

    # Running tests on the Lambda
    tests_runner_facade = TestsRunnerFacade(
        pytest_args=pytest_args,
        config=config,
    )
    tests_runner_facade.run_tests()
