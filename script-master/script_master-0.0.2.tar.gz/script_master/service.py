import asyncio

from script_master_helper import executor
from script_master_helper import workplanner
from script_master_helper.executor.schemas import ProcessCreateSchema
from script_master_helper.workplanner.enums import Statuses
from script_master_helper.workplanner.schemas import WorkplanUpdate, GenerateWorkplans

from script_master.logger import logger
from script_master.notebook import Notebook
from script_master.settings import Settings

workplanner_client = workplanner.client.AsyncClient(
    host=Settings().workplanner_host, port=Settings().workplanner_port
)
executor_client = executor.client.AsyncClient(
    host=Settings().executor_host, port=Settings().executor_port
)
schedule_stop_event = asyncio.Event()


async def generate_workplans_for_notebook():
    logger.info("Generate workplans")

    async for notebook in Notebook.iter_of_valid(include_archived=False):
        workplan_generate_schema = GenerateWorkplans(
            name=notebook.name,
            start_time=notebook.schema.work.schedule._start_datetime,
            interval_in_seconds=notebook.schema.work.schedule._interval_in_seconds,
            keep_sequence=notebook.schema.work.schedule.fill_missing,
            back_restarts=notebook.schema.work.schedule.back_restarts,
            max_retries=notebook.schema.work.max_retries,
            retry_delay=notebook.schema.work.retry_delay,
            extra=GenerateWorkplans.WorkplanExtraData(
                expires_utc=notebook.schema.work.get_expires(),
                data=notebook.schema.script.get_info(),
            ),
        )
        logger.info(
            "[{}] Generate workplan: {}",
            workplan_generate_schema.name,
            workplan_generate_schema,
        )
        try:
            workplans = await workplanner_client.generate_workplans(
                workplan_generate_schema
            )
        except workplanner.client.ApiError as exc:
            logger.exception(exc)
        except Exception as exc:
            logger.exception(exc)
        else:
            for wp in workplans:
                logger.info("[{}, {}] Workplan created: {}", wp.name, wp.id, wp)


async def send_to_executer():
    logger.info("Send to executer")
    async for notebook in Notebook.iter_of_valid(include_archived=False):
        # TODO: надо сделать метод получения воркпланов итерационный.
        try:
            workplans = await workplanner_client.workplans_for_execute(notebook.name)
        except (workplanner.client.ApiError, Exception) as exc:
            logger.exception(exc)
            return

        for workplan in workplans:
            await notebook.render_worktime(workplan.worktime_utc)

            process_create_schema = ProcessCreateSchema(
                workplan_id=workplan.id,
                name=notebook.name,
                command=notebook.schema.script.get_command_line(),
                env=notebook.schema.script.env,
                cwd=notebook.schema.script.cwd,
                time_limit=notebook.schema.work.soft_time_limit,
                expires_utc=notebook.schema.work.time_limit,
                git=notebook.schema.git,
                venv=notebook.schema.venv,
                save_stderr=notebook.schema.work.save_stderr,
                save_stdout=notebook.schema.work.save_stdout,
            )
            workplan_update_schema = WorkplanUpdate(id=workplan.id)
            try:
                process = await executor_client.create_process(process_create_schema)
                if process is False:
                    # No free workers.
                    logger.debug("No free workers")
                    return
            except (executor.client.ApiError, Exception) as exc:
                logger.exception(
                    "[{}, {}] Error creating process {}",
                    workplan.name,
                    workplan.worktime_utc,
                    exc,
                )
                workplan_update_schema.info = str(exc)
                return
            else:
                logger.info("Create {}", process)
                workplan_update_schema.status = Statuses.run
                workplan_update_schema.data = process.dict(exclude_unset=True)

            try:
                await workplanner_client.update_workplan(workplan_update_schema)
            except (workplanner.client.ApiError, Exception) as exc:
                logger.exception(exc)
                return


async def scheduler():
    while not schedule_stop_event.is_set():
        await generate_workplans_for_notebook()
        await send_to_executer()
        await asyncio.sleep(Settings().hearbeat_interval_sec)
