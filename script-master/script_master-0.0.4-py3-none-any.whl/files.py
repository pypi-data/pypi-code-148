import abc
import difflib as df
import fnmatch

import orjson
import yaml
from aiopath import AsyncPath

from script_master.template import render_template


class FileAbstract(abc.ABC):
    path: AsyncPath = NotImplemented
    name: str = NotImplemented
    fmt: str = NotImplemented

    @abc.abstractmethod
    async def loads(self, kwargs_for_render: dict | None = None):
        ...


class TextFile(FileAbstract):
    __slots__ = ("path", "name", "_text", "kwargs_for_render")
    fmt = "json"

    def __init__(self, path: str | AsyncPath, text=None):
        if isinstance(path, str):
            path = AsyncPath(path)
        self.path = path
        self.name = self.path.name
        self._text = text
        self.kwargs_for_render = {
            "filename": self.name,
            "filepath": str(self.path),
        }

    async def read_text(self, force: bool = False) -> str:
        if force or self._text is None:
            self._text = await self.path.read_text()

        return self._text

    async def write_text(self, text, /, exist_ok: bool = True) -> None:
        if not exist_ok and await self.path.exists():
            raise FileExistsError(f"File already exists: {self.path}")

        await self.check_before_write()
        await self.path.write_text(text)
        self._text = text

    async def loads(self, kwargs_for_render: dict | None = None) -> str:
        dct = self.kwargs_for_render | (kwargs_for_render or {})

        return await render_template(await self.read_text(), **dct)

    async def validate(self) -> tuple[bool, Exception | None, str | None]:
        exception = None
        message = None
        valid = True
        try:
            await self.loads()

        except FileExistsError as exception:
            valid = False
            message = f"File not found: {self.name}"

        except FileNotFoundError as exception:
            valid = False
            message = f"File already exists: {self.name}"

        except Exception as exc:
            valid = False
            exception = str(exc)

        return valid, exception, message

    async def delete(self, missing_ok=True) -> None:
        await self.path.unlink(missing_ok=missing_ok)

    async def move(self, new_path: AsyncPath) -> AsyncPath:
        return await self.path.rename(new_path)

    async def rename(self, new_name: AsyncPath) -> AsyncPath:
        return await self.path.rename(self.path.parent / new_name)

    async def exists(self) -> bool:
        return await self.path.exists()

    async def check_before_write(self) -> None:
        if self._text is None:
            return

        txt1_list = self._text.splitlines()
        try:
            txt2_list = await self.read_text()
        except FileNotFoundError:
            return
        txt2_list = txt2_list.splitlines()

        diff = df.unified_diff(txt1_list, txt2_list, lineterm="")
        diff = "\n".join(diff)

        if diff:
            await self.read_text(force=True)
            raise ValueError(f"File has changed: \n{diff}")

    async def save_text(self):
        if self._text:
            await self.write_text(self._text)
            return

        raise Exception("Not data")


class FileWithDataMixin(TextFile):
    __slots__ = ("_data", "pattern")

    def __init__(self, path: str | AsyncPath, text=None):
        super().__init__(path, text)
        self._data: dict | list | None = None

    async def write_text(self, text, /, exist_ok: bool = True) -> None:
        await super().write_text(text, exist_ok)
        self._data = None


class YAMLFile(FileWithDataMixin):
    fmt = "yaml"
    pattern = "*.y*ml"

    async def loads(self, kwargs_for_render: dict = None) -> dict | list:
        if self._data is not None:
            return self._data
        text = await super().loads(kwargs_for_render)
        # self._data = await tag_loads(yaml_loads(text))
        self._data = yaml.safe_load(text)

        return self._data


class JSONFile(FileWithDataMixin):
    fmt = "json"
    pattern = "*.json"

    async def loads(self, kwargs_for_render: dict = None) -> dict | list:
        if self._data is not None:
            return self._data
        text = await super().loads(kwargs_for_render)
        self._data = orjson.loads(text)
        # self._data = await tag_loads(data)

        return self._data


def init_file(path: str | AsyncPath, *, text=None) -> TextFile | YAMLFile | JSONFile:
    if fnmatch.fnmatch(path, YAMLFile.pattern):
        return YAMLFile(path, text)
    elif fnmatch.fnmatch(path, JSONFile.pattern):
        return JSONFile(path, text)
    else:
        return TextFile(path, text)
