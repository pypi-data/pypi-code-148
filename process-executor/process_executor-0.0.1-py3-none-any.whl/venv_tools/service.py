"""Manage Python virtual environments."""
import abc
import asyncio
import hashlib
import os
import platform
import shutil
import subprocess
from asyncio import StreamReader
from asyncio.subprocess import Process
from pathlib import Path
from typing import List, Optional, Union

from process_executor.app import logger
from process_executor.settings import Settings


class VenvSpecsAbstract(abc.ABC):
    def __init__(self, version: str | None = None):
        self.version = version or Settings().default_python_version

    @property
    @abc.abstractmethod
    def lib_dir(self):
        ...

    @property
    @abc.abstractmethod
    def bin_dir(self):
        ...

    @property
    @abc.abstractmethod
    def site_packages_dir(self):
        ...

    @property
    @abc.abstractmethod
    def config(self):
        ...

    @property
    @abc.abstractmethod
    def python_file(self):
        ...

    @property
    @abc.abstractmethod
    def executable(self):
        ...


class VenvSpecsPosix(VenvSpecsAbstract):
    lib_dir = "lib"
    bin_dir = "bin"
    python_file = "python"
    config = "pyvenv.cfg"

    @property
    def site_packages_dir(self):
        return os.path.join("lib", f"python{self.version}", "site-packages")

    @property
    def executable(self):
        return f"python{self.version}"


class VenvSpecsNT(VenvSpecsAbstract):
    lib_dir = "Lib"
    bin_dir = "Scripts"
    python_file = "python.exe"
    site_packages_dir = os.path.join("Lib", "site-packages")
    config = "pyvenv.cfg"

    @property
    def executable(self):
        return f"py -{self.version}"


POSIX = VenvSpecsPosix()
NT = VenvSpecsNT()


class VirtualEnv:
    PLATFORM_SPECS = {"Linux": POSIX, "Darwin": POSIX, "Windows": NT}

    def __init__(self, dir: Path, version: str | None = None):
        self.dir = dir
        self.root = dir / "venv"
        self.specs = self.platform_specs(version)
        self.version = version
        self.executable = self.root / self.specs.bin_dir / self.specs.python_file
        self.config = self.root / self.specs.config

    @classmethod
    def platform_specs(cls, version: str | None = None) -> VenvSpecsAbstract:
        system = platform.system()
        try:
            specs = cls.PLATFORM_SPECS[system]
        except KeyError:
            raise Exception(f"Platform {system} not supported.")

        if version:
            specs.version = version

        return specs


class AsyncSubprocessError(Exception):
    """Happens when an async subprocess exits with a resultcode != 0."""

    def __init__(
        self,
        message: str,
        process: Process,
        stderr: Optional[str] = None,
    ):
        """Initialize AsyncSubprocessError."""
        self.process = process
        self._stderr: Union[str, StreamReader, None] = stderr or process.stderr
        super().__init__(message)

    @property
    async def stderr(self) -> Optional[str]:
        """Return the output of the process to stderr."""
        if not self._stderr:
            return None
        elif not isinstance(self._stderr, str):
            stream = await self._stderr.read()
            self._stderr = stream.decode("utf-8")

        return self._stderr


async def exec_async(*args, **kwargs) -> Process:
    """
    Run an executable asyncronously.

    :raises AsyncSubprocessError: if the command fails
    """
    logger.debug("Run command: {}", args)
    run = await asyncio.create_subprocess_exec(
        *args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **kwargs,
    )
    await run.wait()

    if run.returncode != 0:
        raise AsyncSubprocessError("Command failed", run)

    return run


class VenvService:
    def __init__(self, name: str, version: str | None = None):
        """
        Manage isolated virtual environments.

        The methods in this class are not threadsafe.
        """
        self.name = name
        self.venv = VirtualEnv(dir=Settings().scripts_dir / name, version=version)
        self.fingerprint_path = self.venv.root / ".venv_fingerprint"

    async def install(self, *pip_urls: str, clean: bool = False) -> None:
        """
        Configure a virtual environment and install the given `pip_urls` packages in it.

        This will try to use an existing virtual environment if one exists unless commanded
        to `clean`.

        :raises: SubprocessError: if any of the commands fail.
        """
        pip_urls = [pip_url for arg in pip_urls for pip_url in arg.split(" ")]

        if not clean and self._requires_clean_install(pip_urls):
            logger.info(
                f"Packages for '{self.venv.dir}' have changed so performing a clean install."
            )
            clean = True

        if clean:
            await self._clean_install(pip_urls)
        else:
            await self._upgrade_install(pip_urls)
        self._write_fingerprint(pip_urls)

    @staticmethod
    def _fingerprint(pip_urls: List[str]) -> str:
        """Return a unique string for the given pip urls."""
        key = " ".join(sorted(pip_urls))
        return hashlib.sha256(bytes(key, "utf-8")).hexdigest()

    def _read_fingerprint(self) -> Optional[str]:
        """Return the fingerprint of the existing virtual environment, if any."""
        if not self.fingerprint_path.exists():
            return None
        with open(self.fingerprint_path, "rt") as fingerprint_file:
            return fingerprint_file.read()

    def _requires_clean_install(self, pip_urls: List[str]) -> bool:
        """Return `True` if the virtual environment doesn't exist or can't be reused."""
        existing_fingerprint = self._read_fingerprint()
        if not existing_fingerprint:
            return True
        return existing_fingerprint != self._fingerprint(pip_urls)

    def clean(self) -> None:
        """Destroy the virtual environment, if it exists."""
        try:
            shutil.rmtree(self.venv.root)
            logger.info(
                "Removed old virtual environment for '{}'",  # noqa: WPS323
                self.venv.dir,
            )
        except FileNotFoundError:
            # If the VirtualEnv has never been created before do nothing
            logger.debug("No old virtual environment to remove")
            pass

    async def create(self) -> Process:
        """
        Create a new virtual environment.

        :raises: SubprocessError: if the command fails.
        """
        logger.info(f"Creating virtual environment for '{self.venv.dir}'")

        Settings().scripts_dir.mkdir(exist_ok=True)
        self.venv.dir.mkdir(exist_ok=True)
        self.venv.root.mkdir(exist_ok=True)
        try:
            return await exec_async(
                *self.venv.specs.executable.split(" "),
                "-m",
                "venv",
                str(self.venv.root),
            )
        except AsyncSubprocessError as err:
            raise AsyncSubprocessError(
                f"Could not create the virtualenv for '{self.venv.dir}'",
                err.process,
            )

    async def upgrade_pip(self) -> Process:
        """
        Upgrade the `pip` package to the latest version in the virtual environment.

        :raises: SubprocessError: if the command fails.
        """
        logger.info(f"Upgrading pip for '{self.venv.dir}'")

        try:
            return await self._pip_install(
                *Settings().default_pip_packages, upgrade=True
            )

        except AsyncSubprocessError as err:
            raise AsyncSubprocessError(
                "Failed to upgrade pip to the latest version.", err.process
            )

    def _write_fingerprint(self, pip_urls: List[str]):
        """Save the fingerprint for this installation."""
        with open(self.fingerprint_path, "wt") as fingerprint_file:
            fingerprint_file.write(self._fingerprint(pip_urls))

    async def _clean_install(self, pip_urls: List[str]) -> None:
        self.clean()
        await self.create()
        await self.upgrade_pip()

        logger.info(
            f"Installing '{' '.join(pip_urls)}' into virtual environment for '{self.venv.dir}'"  # noqa: WPS221
        )
        await self._pip_install(*pip_urls)

    async def _upgrade_install(self, pip_urls: List[str]) -> None:
        logger.info(
            f"Upgrading '{' '.join(pip_urls)}' in existing virtual environment for '{self.venv.dir}'"  # noqa: WPS221
        )
        await self._pip_install(
            *Settings().default_pip_packages, *pip_urls, upgrade=True
        )

    async def _pip_install(self, *pip_urls: str, upgrade: bool = False) -> Process:
        """
        Install a package using `pip` in the proper virtual environment.

        :raises: AsyncSubprocessError: if the command fails.
        """
        args = [
            str(self.venv.executable),
            "-m",
            "pip",
            "install",
        ]
        if upgrade:
            args += ["--upgrade"]
        args += pip_urls

        try:
            return await exec_async(*args)
        except AsyncSubprocessError as err:
            raise AsyncSubprocessError(
                f"Failed to install virtual environment '{self.name}'.", err.process
            )


if __name__ == "__main__":

    async def create_venv_and_install_reqiurements(
        name: str, pip_urls: list[str], version: str | None = None
    ) -> None:
        vs = VenvService(name=name, version=version)
        await vs.create()
        await vs.install(*pip_urls)

    asyncio.run(
        create_venv_and_install_reqiurements("test_venv2", ["pendulum", "pytz"])
    )
