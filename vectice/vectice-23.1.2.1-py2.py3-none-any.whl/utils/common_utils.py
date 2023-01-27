from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from git import GitError, Repo

from vectice.api.json.code import CodeInput
from vectice.api.json.code_version import CodeVersionCreateBody
from vectice.api.json.iteration import IterationStatus
from vectice.models.git_version import CodeSource

if TYPE_CHECKING:
    from logging import Logger

    from vectice.api.client import Client
    from vectice.models.iteration import Iteration


def _check_code_source(client: Client, project_id: int, _logger: Logger) -> int | None:
    """Capture source code.

    Naive implementation that uses the commit hash to name the code.

    Only one version of the code is stored in backend.
    This allows to easily reuse versions based on their commits hash.

    Parameters:
        client: The Vectice client, used to communicate with the backend.
        project_id: The id of the current project.

    Returns:
        Either the id of the created/fetched code version, or none if the code could not be captured.
    """
    repository = _look_for_git_repository(_logger)
    if not repository:
        return None
    code = CodeSource(repository)
    git_version = code.git_version
    code_input = CodeInput(name=code.git_version.commitHash)
    try:
        code_output = client.create_code_gql(project_id, code_input)
    except Exception:
        code_output = client.get_code(code.git_version.commitHash, project_id)
        code_version_output = client.get_code_version("Version 1", code_output.id)
        _logger.warning("The code commit exists already.")
        return int(code_version_output.id)
    if code.user_declared_version:
        user_declared_version = code.user_declared_version.__dict__
    else:
        user_declared_version = {}
    code_version_body = CodeVersionCreateBody(
        action="CREATE_GIT_VERSION", gitVersion=git_version.__dict__, userDeclaredVersion=user_declared_version
    )
    code_version_output = client.create_code_version_gql(code_output.id, code_version_body)
    _logger.info("Code captured and will be linked to asset.")
    code_version_id = int(code_version_output.id)
    _capture_local_changed_files(repository, client, _logger, project_id, code_version_id)
    return code_version_id


def _capture_local_changed_files(
    repository: Any, client: Client, _logger: Logger, project_id: int, code_version_id: int
) -> None:
    diff_outputs = []
    changed_files = repository.index.diff(None)
    file_names = []
    for file in changed_files:
        diff_outputs.append(("file", (f"{file.a_path}.diff", (repository.git.diff(file.a_path)))))
        file_names.append(file.a_path)
    if diff_outputs:
        client.create_code_attachments(diff_outputs, code_version_id, project_id)
    if file_names:
        _logger.info(f"Code captured the following changed files; {', '.join(file_names)}")


def _look_for_git_repository(_logger: Logger, repo_path=".") -> Any | None:
    try:
        repo_path = os.path.abspath(repo_path)
    except OSError:
        _logger.warning(f"Code capture failed: the directory '{repo_path}' cannot be accessed by the system")
        return None
    try:
        return Repo(repo_path, search_parent_directories=True)
    except GitError as error:
        error_message = str(error) or repo_path
        _logger.warning(
            f"Code capture failed: {error.__class__.__name__}: {error_message}. "
            "Make sure the current directory is a valid Git repository (non-bare, non worktree) "
            "and its permissions allow the current user to access it."
        )
        return None


def _check_for_code(client: Client, project_id: int, _logger: Logger) -> int | None:
    code_version_id = None
    from vectice import code_capture

    if code_capture:
        code_version_id = _check_code_source(client, project_id, _logger)
    return code_version_id


def _inform_if_git_repo(_logger: Logger):
    with hide_logs(_logger.name):
        repo = _look_for_git_repository(_logger)
    if repo:
        _logger.info("A git repository was found but code capture is disabled.")


@contextmanager
def hide_logs(package: str):
    old_level = logging.getLogger(package).level
    try:
        logging.getLogger(package).setLevel(logging.ERROR)
        yield
    finally:
        logging.getLogger(package).setLevel(old_level)


def _check_read_only(iteration: Iteration):
    """Check if an iteration is completed or canceled.

    Refreshing the iteration is necessary because in a Jupyter notebook
    its status could have changed on the backend.

    Parameters:
        iteration: The iteration to check.

    Raises:
        RuntimeError: When the iteration is read-only (completed or canceled).
    """
    refresh_iteration = iteration._phase.iteration(iteration.index)
    if refresh_iteration._status in {IterationStatus.Completed, IterationStatus.Abandoned}:
        raise RuntimeError(f"The Iteration is {refresh_iteration._status.name} and is read-only!")
