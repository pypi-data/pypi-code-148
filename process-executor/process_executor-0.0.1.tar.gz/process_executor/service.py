import asyncio
import datetime as dt
from concurrent.futures import ThreadPoolExecutor

from script_master_helper.executor.schemas import ProcessCreateSchema
from script_master_helper.workplanner import client
from script_master_helper.workplanner.client import ApiError, errors
from script_master_helper.workplanner.enums import Statuses
from script_master_helper.workplanner.schemas import WorkplanUpdate

from process_executor.app import logger
from process_executor.executor import processes, ProcessExecutor
from process_executor.git_tools.servise import Repo
from process_executor.settings import Settings
from process_executor.venv_tools.service import VenvService

workplanner_client = client.AsyncClient(
    host=Settings().workplanner_host,
    port=Settings().workplanner_port,
)


async def check_process_status():
    for process_info in list(processes.iter_info_processes()):
        if process_info.is_done:
            logger.debug(
                "Updating data in the workplanner for %s", process_info.workplan_id
            )

            update_schema = WorkplanUpdate(id=process_info.workplan_id)
            update_schema.started_utc = process_info.started_utc
            update_schema.finished_utc = process_info.finished_utc
            update_schema.info = process_info.error_message

            if process_info.has_error:
                update_schema.status = Statuses.error
            else:
                update_schema.status = Statuses.success

            try:
                await workplanner_client.update_workplan(schema=update_schema)
            except ApiError as exc:
                if exc == errors.not_found_error:
                    logger.info(str(exc))
                else:
                    logger.exception(str(exc))

            processes.pop(process_info.id)


async def cycle_check_process_status():
    while True:
        await check_process_status()
        await asyncio.sleep(Settings().hearbeat_interval_sec)


async def processes_to_fail():
    workplans_schemas = []
    for process_info in processes.iter_info_processes():
        workplans_schemas.append(
            WorkplanUpdate(
                id=process_info.workplan_id,
                status=Statuses.error,
                info="StopError: The result is unknown due to the stop of the executor",
                finished_utc=dt.datetime.utcnow() if process_info.started_utc else None,
            )
        )
    try:
        await workplanner_client.update_workplans(workplans_schemas)
    except ApiError as exc:
        logger.exception(str(exc))


async def download_script(schema: ProcessCreateSchema) -> Repo:
    repo = Repo(schema.git)
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(
        max_workers=1, thread_name_prefix="download_script_thread"
    ) as executor:
        await loop.run_in_executor(executor, repo.clone_or_pull)

    return repo


async def create_venv(schema: ProcessCreateSchema, repo: Repo) -> None:
    service = VenvService(name=repo.name, version=schema.venv.version)
    await service.create()
    await service.install(*schema.venv.requirements)
    schema.command = [
        part.format(executable=service.venv.executable) for part in schema.command
    ]


def get_executor_process(schema: ProcessCreateSchema) -> ProcessExecutor:
    def decorator(func):
        async def wrap():
            repo = await download_script(schema)
            schema.cwd = str(repo.path)

            await create_venv(schema, repo)

            return await func()

        return wrap

    executor_process = ProcessExecutor(schema)
    executor_process.run = decorator(executor_process.run)

    return executor_process
