import yaml
from fastapi import Form, APIRouter
from script_master.notebook import Notebook
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from script_master_ui.const import templates
from script_master_ui.exceptions import throw, NotFoundException

route_prefix = "notebook"
router = APIRouter(prefix=f"/{route_prefix}", tags=[f"{route_prefix}"])


@router.get("/")
async def notebooks(request: Request):
    # TODO: Add pagination
    notebooks_data = []

    async for notebook in Notebook.iter():
        await notebook.validate()
        notebooks_data.append(
            {
                "name": notebook.name,
                "is_archive": notebook.is_archive(),
                "validate": notebook.valid,
            }
        )

    return templates.TemplateResponse(
        "/pages/notebooks.html",
        context={"request": request, "notebooks": notebooks_data},
    )


@router.get("/create")
async def create_get(request: Request):
    return templates.TemplateResponse(
        "/pages/create.html", context={"request": request}
    )


@router.post("/create")
async def create_post(request: Request, name: str = Form(...), text: str = Form(...)):
    notebook = await Notebook.create(name, yaml_text=text)
    if notebook.valid:
        return RedirectResponse(f"/{route_prefix}/{notebook.name}/detailed")

    name_error = ""
    if isinstance(notebook.exception, FileExistsError):
        name_error = notebook.file.name

    return templates.TemplateResponse(
        "/pages/create.html",
        context={
            "request": request,
            "name": name,
            "yaml_text": text,
            "name_error": name_error,
            "yaml_text_error": str(notebook.exception),
        },
    )


@router.get("/{name}/detailed")
@router.post("/{name}/detailed")
async def detailed(name: str, request: Request, render: bool = False):
    notebook = await Notebook.get_by_name(name) or throw(NotFoundException)
    valid, exception = await notebook.validate()
    text = await notebook.file.read_text()

    if render:
        try:
            text = yaml.safe_dump(notebook.schema.dict())
        except ValueError as exception:
            pass

    return templates.TemplateResponse(
        "/pages/detailed.html",
        context={
            "request": request,
            "name": name,
            "valid": valid,
            "yaml_text": text,
            "yaml_text_error": str(exception or ""),
            "filepath": str(notebook.file.path),
            "render": render,
        },
    )


@router.get("/{name}/edit")
async def edit_get(name: str, request: Request):
    notebook = await Notebook.get_by_name(name) or throw(NotFoundException)
    await notebook.validate()

    return templates.TemplateResponse(
        "/pages/edit.html",
        context={
            "request": request,
            "filename": notebook.file.name,
            "yaml_text": await notebook.file.read_text(),
            "yaml_text_error": str(notebook.exception or ""),
        },
    )


@router.post("/{name}/edit")
async def edit_post(request: Request, name: str, text: str = Form(...)):
    notebook = await Notebook.get_by_name(name) or throw(NotFoundException)

    valid, exception = await notebook.replace(text)
    if valid:
        return RedirectResponse(
            f"/{route_prefix}/{name}/detailed", status_code=status.HTTP_302_FOUND
        )

    return templates.TemplateResponse(
        "/pages/edit.html",
        context={
            "request": request,
            "filename": notebook.file.name,
            "yaml_text": text,
            "yaml_text_error": str(exception or ""),
        },
    )


@router.get("/{name}/delete")
@router.post("/{name}/delete")
async def delete(name: str):
    notebook = await Notebook.get_by_name(name) or throw(NotFoundException)
    await notebook.delete()

    return RedirectResponse(f"/{route_prefix}")


@router.get("/{name}/unarchive")
async def unarchive(name: str):
    notebook = await Notebook.get_by_name(name) or throw(NotFoundException)
    await notebook.unarchive()

    return RedirectResponse(f"/{route_prefix}")


@router.get("/{name}/archive")
async def archive(name: str):
    notebook = await Notebook.get_by_name(name) or throw(NotFoundException)
    await notebook.archive()

    return RedirectResponse(f"/{route_prefix}")
