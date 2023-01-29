import asyncio
import datetime as dt
import os
import uuid
from typing import Optional, TYPE_CHECKING

from script_master_helper.executor.schemas import ProcessDataSchema, ProcessCreateSchema

from process_executor.app import logger
from process_executor.settings import Settings

if TYPE_CHECKING:
    from asyncio.subprocess import Process


class Processes:
    def __init__(self):
        self._processes: dict[str, "ProcessExecutor"] = {}

    def __getitem__(self, name) -> Optional["ProcessExecutor"]:
        return self._processes.get(name)

    def __len__(self) -> int:
        return len(self._processes)

    def count_active(self) -> int:
        return sum(1 for p in self._processes.values() if not p.is_done)

    def iter_info_processes(self):
        return (p.info() for p in self._processes.values())

    def add(self, process: "ProcessExecutor") -> None:
        self._processes[process.id] = process

    def pop(self, process_id) -> Optional["ProcessExecutor"]:
        process = self._processes.pop(process_id, None)

        return process


processes = Processes()


class ProcessExecutor:
    def __init__(self, schema: ProcessCreateSchema):
        self.schema: ProcessCreateSchema = schema

        self.id: str = uuid.uuid4().hex
        self.pid: int | None = None
        self.is_done: bool = False
        self.has_error: bool = False
        self.error_message: str = ""
        self.started_utc: dt.datetime | None = None
        self.finished_utc: dt.datetime | None = None
        self.subprocess: Optional["Process"] = None

    def info(self) -> ProcessDataSchema:
        return ProcessDataSchema(
            id=self.id,
            pid=self.pid,
            is_done=self.is_done,
            has_error=self.has_error,
            error_message=self.error_message,
            started_utc=self.started_utc,
            finished_utc=self.finished_utc,
            **self.schema.dict(exclude_unset=True),
        )

    def terminate(self):
        if self.subprocess:
            logger.info(f"Terminate {self!r}")
            self.subprocess.terminate()

    def _done(self, *, error_message: str = None) -> None:
        self.is_done = True
        self.has_error = bool(error_message)
        self.error_message = error_message
        self.finished_utc = dt.datetime.utcnow()
        if error_message:
            logger.error(f"Error {self!r}, {error_message}")

        logger.info(f"End {self!s}")

    async def _read_std(self):
        is_save = self.schema.save_stdout or self.schema.save_stderr
        try:
            if is_save:
                file = open(Settings().process_log_dir / f"{self.id}.log", "wb")

            while self.schema.save_stdout:
                line = await self.subprocess.stdout.readline()
                if line:
                    file.write(line)
                    logger.debug(f"{self!r}, line=[{line.decode()}]")
                else:
                    break

            while self.schema.save_stderr:
                line_err = await self.subprocess.stderr.readline()
                if line_err:
                    file.write(line_err)
                    logger.error(f"{self!r}, error=[{line_err.decode()}]")
                else:
                    break
        finally:
            if is_save:
                file.close()

    async def run(self):
        self.started_utc = dt.datetime.utcnow()
        logger.debug("Run process {}", self.info())
        try:
            self.subprocess = await asyncio.create_subprocess_exec(
                *self.schema.command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.schema.cwd,
                env={**os.environ.copy(), **self.schema.env}
                if self.schema.env
                else None,
                **self.schema.subprocess_kwargs,
            )
        except Exception as exc:
            logger.error("Error creating process {}", self.info())
            self._done(error_message=str(exc))

        else:
            self.pid = self.subprocess.pid

            logger.info(f"Create process {self!r}, command={self.schema.command}")

            await self._read_std()

            error = await self.subprocess.wait()
            self._done(error_message="UnknownError" if error else None)

    async def run_with_timeout(self) -> None:
        try:
            timeout = self.schema.get_timeout()
            if timeout <= 0:
                raise asyncio.TimeoutError()
            await asyncio.wait_for(self.run(), timeout=timeout)

        except asyncio.TimeoutError:
            self._done(error_message="ExpiredError")
            self.terminate()

    def __repr__(self):
        return f"Process id=[{self.id}], pid=[{self.pid}]"

    def __str__(self):
        text = f"{self!r}, is_done={self.is_done}, has_error={self.has_error}, started={self.started_utc}"

        if self.finished_utc and self.started_utc:
            duration_in_minutes = round(
                (self.finished_utc - self.started_utc).total_seconds() / 60, 1
            )
            text += f", finished={self.finished_utc}, {duration_in_minutes=}"

        return text
