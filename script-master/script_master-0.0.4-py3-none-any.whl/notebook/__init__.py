import pendulum
from aiopath import AsyncPath
from pydantic import ValidationError
from yaml._yaml import YAMLError

from script_master.files import YAMLFile, init_file
from script_master.notebook.schemas import NotebookSchema
from script_master.notebook.service import get_notebook_name_from_filename
from script_master.settings import Settings
from script_master.template import get_variables_map


class Notebook:
    model = NotebookSchema
    patterns = (YAMLFile.pattern,)

    def __init__(self, file: YAMLFile):
        self.file = file
        self.name = get_notebook_name_from_filename(self.file.name)

        self._schema = None
        self._valid = None
        self._exception = None

    def __hash__(self):
        if self.valid is None:
            raise AttributeError("Not validated")
        return hash(self.schema.dict())

    @property
    def schema(self) -> NotebookSchema:
        if self.valid is None:
            raise AttributeError("Not validated")
        elif self.valid is False:
            raise self._exception

        return self._schema

    @property
    def valid(self) -> bool:
        if self._valid is None:
            raise AttributeError("Not validated")
        return self._valid

    @property
    def exception(self) -> Exception | None:
        if self._valid is None:
            raise ValueError("Not validated")
        return self._exception

    @classmethod
    async def from_path(cls, path: AsyncPath) -> "Notebook":
        return cls(init_file(path))

    async def validate(self) -> tuple[bool, Exception | None]:
        try:
            data = await self.file.loads(
                kwargs_for_render=dict(
                    notebook_name=self.name, variables=await get_variables_map()
                )
            )
            self._schema = self.model(**data)
        except Exception as exc:
            self._valid, self._exception = False, exc
        else:
            self._valid = True

        return self._valid, self._exception

    async def render_with(self, **kwargs_for_render):
        try:
            data = await self.file.loads(
                kwargs_for_render=dict(notebook_name=self.name, **kwargs_for_render)
            )
            self._schema = self.model(**data)
        except (YAMLError, ValidationError, FileNotFoundError) as exc:
            self._valid, self._exception = False, exc
        else:
            self._valid = True

        return self._valid, self._exception

    async def render_worktime(self, worktime: pendulum.DateTime):
        worktime.__str__ = lambda self: self.format("YYYY-MM-DD HH:mm:ss")
        workdate = worktime.date()
        workdate.__str__ = lambda self: self.format("YYYY-MM-DD")

        return await self.render_with(worktime=worktime, workdate=workdate)

    @classmethod
    async def create(cls, name: str, yaml_text) -> "Notebook":
        filepath = Settings().ARCHIVE_NOTEBOOK_DIR / f"{name}.{YAMLFile.fmt}"
        notebook = cls(YAMLFile(filepath, yaml_text))
        valid, exception = await notebook.validate()
        if valid:
            await notebook.file.save_text()

        return notebook

    async def replace(self, yaml_text, /) -> tuple[bool, Exception | None]:
        temp_file = YAMLFile(self.file.path.with_name("temp"), yaml_text)
        temp_notebook = Notebook(temp_file)
        valid, exception = await temp_notebook.validate()
        if valid:
            await temp_file.save_text()
            self._valid, self._exception = valid, exception

        return valid, exception

    async def delete(self) -> bool:
        if await self.file.path.exists():
            await self.file.delete()
            return True
        return False

    async def archive(self) -> None:
        await self.file.move(Settings().ARCHIVE_NOTEBOOK_DIR / self.file.path.name)

    async def unarchive(self) -> None:
        await self.file.move(Settings().NOTEBOOK_DIR / self.file.path.name)

    def is_archive(self) -> bool:
        return Settings().ARCHIVE_NOTEBOOK_DIR == self.file.path.parent

    @classmethod
    async def iter(cls, *, include_archived: bool = True):
        for pattern in Notebook.patterns:
            async for path in Settings().NOTEBOOK_DIR.rglob(pattern):
                if path.parent != Settings().ARCHIVE_NOTEBOOK_DIR:
                    yield await cls.from_path(path)

            if include_archived:
                async for path in Settings().ARCHIVE_NOTEBOOK_DIR.glob(pattern):
                    yield await cls.from_path(path)

    @classmethod
    async def iter_of_valid(cls, *, include_archived: bool = True):
        async for notebook in cls.iter(include_archived=include_archived):
            await notebook.validate()
            if notebook.valid:
                yield notebook

    @classmethod
    async def get_by_name(cls, name: str) -> "Notebook":
        async for notebook in cls.iter(include_archived=True):
            if get_notebook_name_from_filename(notebook.name) == name:
                return notebook
