from fastapi import APIRouter
from fastapi import Form
from script_master.files import init_file
from script_master.settings import Settings
from starlette.requests import Request
from starlette.responses import RedirectResponse

from script_master_ui.const import templates
from script_master_ui.exceptions import throw, NotFoundException
from script_master_ui.utils import editor_form_errors

route_prefix = "variable"
router = APIRouter(prefix=f"/{route_prefix}", tags=[f"{route_prefix}"])


@router.get("/list")
async def variables(request: Request):
    variables_data = []

    async for path in Settings().VARIABLES_DIR.rglob("*"):
        if await path.is_file():
            file = init_file(path)
            await file.loads()
            variables_data.append(
                {
                    "name": file.name,
                }
            )

    return templates.TemplateResponse(
        "/pages/variables.html",
        context={
            "request": request,
            "route_prefix": route_prefix,
            "variables": variables_data,
        },
    )


@router.get("/create/{fmt}")
async def create_variable(request: Request, fmt: str):
    return templates.TemplateResponse(
        "/pages/create-variable.html", context={"request": request, "fmt": fmt}
    )


@router.post("/create/{fmt}")
async def create_variable_post(
    request: Request, fmt: str, name: str = Form(...), text: str = Form(...)
):
    path = Settings().VARIABLES_DIR / f"{name}.{fmt}"
    file = init_file(path, text=text)
    await file.exists() or throw(NotFoundException)
    valid, exception, message = await file.validate()
    if valid:
        await file.save_text()
        return RedirectResponse(f"/{route_prefix}/{file.name}/detailed")

    return templates.TemplateResponse(
        "/pages/create-variable.html",
        context={
            "request": request,
            "fmt": fmt,
            "form_data": {"name": name, "text": text},
            "form_errors": editor_form_errors(exception, message),
        },
    )


@router.get("/{name}/detailed")
@router.post("/{name}/detailed")
async def variable_detailed(name: str, request: Request, render: bool = False):
    file = init_file(Settings().VARIABLES_DIR / name)
    await file.exists() or throw(NotFoundException)
    valid, exception, message = await file.validate()
    text = await file.read_text()

    if render:
        if valid:
            text = await file.loads()
        else:
            render = False

    return templates.TemplateResponse(
        "/pages/wrapper-detailed.html",
        context={
            "request": request,
            "render": render,
            "object": route_prefix,
            "form_data": {"name": name, "text": text},
            "form_errors": editor_form_errors(exception, message),
            "filepath": str(file.path),
        },
    )


@router.get("/{name}/edit")
async def edit_notebook_get(name: str, request: Request):
    file = init_file(Settings().VARIABLES_DIR / name)
    await file.exists() or throw(NotFoundException)
    valid, exception, message = await file.validate()

    return templates.TemplateResponse(
        "/pages/create-variable.html",
        context={
            "request": request,
            "fmt": file.fmt,
            "form_data": {
                "name": name.split(".", 1)[0],
                "text": await file.read_text(),
            },
            "form_errors": editor_form_errors(exception, message),
        },
    )


@router.post("/{name}/edit")
async def edit_variable_post(request: Request, name: str, text: str = Form(...)):
    file = init_file(Settings().VARIABLES_DIR / name, text=text)
    await file.exists() or throw(NotFoundException)
    valid, exception, message = await file.validate()

    if valid:
        await file.save_text()
        return RedirectResponse(f"/{route_prefix}/{file.name}/detailed")

    return templates.TemplateResponse(
        "/pages/create-variable.html",
        context={
            "request": request,
            "fmt": file.fmt,
            "form_data": {
                "name": name.split(".", 1)[0],
                "text": await file.read_text(),
            },
            "form_errors": editor_form_errors(exception, message),
        },
    )


@router.get("/{name}/delete")
@router.post("/{name}/delete")
async def delete_notebook(name: str):
    file = init_file(Settings().VARIABLES_DIR / name)
    await file.delete()

    return RedirectResponse(f"/{route_prefix}/list")
