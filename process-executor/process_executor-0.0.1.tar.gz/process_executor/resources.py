from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from script_master_helper.executor.schemas import (
    ProcessCreateSchema,
    ResponseGenericSchema,
    ProcessCreateResponseSchema,
)
from starlette.background import BackgroundTasks

from process_executor import errors
from process_executor.app import logger
from process_executor.executor import processes
from process_executor.service import get_executor_process
from process_executor.settings import Settings

router = APIRouter()


@router.post("/process/create", response_class=ORJSONResponse)
async def process_create_view(
    schema: ProcessCreateSchema, background_tasks: BackgroundTasks
):
    if processes.count_active() >= Settings().max_processes:
        logger.info("MAX_PROCESSES (skip)")
        raise errors.get_max_number_processes_exception(
            f"{processes.count_active()=} >= {Settings().max_processes=}"
        )

    executor_process = get_executor_process(schema)
    processes.add(executor_process)
    background_tasks.add_task(executor_process.run_with_timeout)

    return ResponseGenericSchema(
        data=ProcessCreateResponseSchema(id=executor_process.id)
    )


@router.get("/process/{id}", response_class=ORJSONResponse)
async def process_view(id: str):
    for p in processes.iter_info_processes():
        if p.id == id:
            return ResponseGenericSchema(data=p)

    raise errors.get_404_exception(f"Process id {id}")


@router.delete("/process/{id}", response_class=ORJSONResponse)
async def process_delete_view(id: str):
    process = processes.pop(id)
    if process is None:
        raise errors.get_404_exception(f"Process id {id}")

    return ResponseGenericSchema(data=process.info())


@router.get("/process/all/list", response_class=ORJSONResponse)
async def process_list_view():
    return ResponseGenericSchema(data=list(processes.iter_info_processes()))


@router.get("/process/completed/list", response_class=ORJSONResponse)
async def process_completed_list_view():
    return ResponseGenericSchema(
        data=[p for p in processes.iter_info_processes() if p.is_done]
    )
