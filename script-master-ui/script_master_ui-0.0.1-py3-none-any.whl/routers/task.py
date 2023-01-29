from fastapi import APIRouter
from script_master_helper import workplanner
from script_master_helper.workplanner.enums import Statuses
from script_master_helper.workplanner.schemas import WorkplanQuery, FieldFilterGeneric
from starlette.requests import Request
from starlette.responses import RedirectResponse

from script_master_ui.const import templates
from script_master_ui.settings import Settings

router = APIRouter()
workplanner_client = workplanner.client.AsyncClient(
    host=Settings().workplanner_host, port=Settings().workplanner_port
)


@router.get("/tasks")
async def all_tasks(request: Request, page: int = None):
    schema = WorkplanQuery(
        filter=WorkplanQuery.Filter(),
        page=page,
        limit=100,
    )
    workplans = await workplanner_client.workplans(schema=schema)

    return templates.TemplateResponse(
        "/pages/tasks.html",
        context={
            "request": request,
            "tasks": workplans,
        },
    )


@router.get("/notebook/{name}/tasks")
async def notebook_tasks_view(name: str, request: Request, page: int = None):
    schema = WorkplanQuery(
        filter=WorkplanQuery.Filter(name=[FieldFilterGeneric[str](value=name)]),
        page=page,
        limit=100,
    )
    workplans = await workplanner_client.workplans(schema=schema)

    return templates.TemplateResponse(
        "/pages/tasks.html",
        context={
            "request": request,
            "tasks": workplans,
        },
    )


@router.get("/notebook/{name}/error-tasks")
async def error_tasks_view(name: str, request: Request, page: int = None):
    schema = WorkplanQuery(
        filter=WorkplanQuery.Filter(
            name=[FieldFilterGeneric[str](value=name)],
            status=[FieldFilterGeneric[list](value=Statuses.error_statuses)],
        ),
        page=page,
        limit=100,
    )
    workplans = await workplanner_client.workplans(schema=schema)

    return templates.TemplateResponse(
        "/pages/tasks.html",
        context={
            "request": request,
            "tasks": workplans,
        },
    )


@router.get("/notebook/{name}/fatal-error-tasks")
async def fatal_error_tasks_view(name: str, request: Request, page: int = None):
    schema = WorkplanQuery(
        filter=WorkplanQuery.Filter(
            name=[FieldFilterGeneric[str](value=name)],
            status=[FieldFilterGeneric[list](value=Statuses.fatal_error)],
        ),
        page=page,
        limit=100,
    )
    workplans = await workplanner_client.workplans(schema=schema)

    return templates.TemplateResponse(
        "/pages/tasks.html",
        context={
            "request": request,
            "tasks": workplans,
        },
    )


@router.get("/notebook/{name}/task/{id}/replay")
async def replay_task(name: str, id: str):
    await workplanner_client.replay(id)
    return RedirectResponse(f"/notebook/{name}/tasks")
