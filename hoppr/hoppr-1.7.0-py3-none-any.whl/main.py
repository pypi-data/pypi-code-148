"""
Framework for manipulating bundles for airgapped transfers.
"""
import logging
import sys

from pathlib import Path
from typing import List, Optional

from typer import Exit, echo, prompt

from hoppr import __version__
from hoppr.configs.credentials import Credentials
from hoppr.configs.manifest import Manifest
from hoppr.configs.transfer import Transfer
from hoppr.in_toto import generate_in_toto_layout
from hoppr.processor import HopprProcessor


def bundle(  # pylint: disable=too-many-arguments,too-many-locals
    manifest_file: Path,
    credentials_file: Path,
    transfer_file: Path,
    log_file: Path,
    verbose: bool = False,
    strict_repos: bool = True,
    create_attestations: bool = False,
    functionary_key_path: Optional[Path] = None,
    functionary_key_prompt: bool = False,
    functionary_key_password: Optional[str] = None,
):
    """
    Run the stages specified in the transfer config
    file on the content specified in the manifest
    """

    metadata_files = [manifest_file, transfer_file]

    if credentials_file is not None:
        Credentials.load_file(file=credentials_file)
        metadata_files.append(credentials_file)

    manifest = Manifest.load_file(file=manifest_file)
    transfer = Transfer.load_file(file=transfer_file)
    log_level = logging.DEBUG if verbose else logging.INFO

    if create_attestations and functionary_key_path is None:
        echo("To create attestations both the `--attest` option and a functionary private key need to be provided.")
        raise Exit(code=1)

    if functionary_key_prompt:
        functionary_key_password = prompt(f"Enter password for {str(functionary_key_path)}", hide_input=True)

    processor = HopprProcessor(
        transfer=transfer,
        manifest=manifest,
        create_attestations=create_attestations,
        functionary_key_path=functionary_key_path,
        functionary_key_password=functionary_key_password,
        log_level=log_level,
    )
    processor.metadata_files = metadata_files

    result = processor.run(log_file=log_file, strict_repos=strict_repos)

    if result.is_fail():
        sys.exit(1)


def generate_layout(
    transfer_file: Path,
    project_owner_key_path: Path,
    functionary_key_path: Path,
    project_owner_key_prompt: bool,
    project_owner_key_password: str,
):
    """
    Create in-toto layout based on transfer file.
    """

    if project_owner_key_prompt:
        project_owner_key_password = prompt(f"Enter password for {str(project_owner_key_path)}", hide_input=True)

    transfer = Transfer.load_file(file=transfer_file)
    generate_in_toto_layout(transfer, project_owner_key_path, functionary_key_path, project_owner_key_password)


def validate(
    input_files: List[Path],
    credentials_file: Path,
    transfer_file: Path,
):
    """
    Validate multiple manifest files for schema errors.
    """

    cred_config = None
    transfer_config = None  # pylint: disable=unused-variable
    manifests = []  # pylint: disable=unused-variable

    if credentials_file is not None:
        cred_config = Credentials.load_file(credentials_file)
    if transfer_file is not None:
        transfer_config = Transfer.load_file(transfer_file)

    manifests = [Manifest.load_file(file, cred_config) for file in input_files]
