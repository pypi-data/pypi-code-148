import abc
import re
from typing import Pattern, Match, Any

from aiopath import AsyncPath

from script_master.settings import Settings


class TagAbstract(abc.ABC):
    regex: Pattern = NotImplemented

    @abc.abstractmethod
    def __call__(self, match: Match):
        ...


class FromTag(TagAbstract):
    regex = re.compile(r"^FROM\((.*)\)$")

    async def __call__(self, match: Match):
        # Переделать под глобальные переменные, из своих файлов можно взять данные через шаблонизатор.
        from script_master.files import init_file

        filename_or_path = AsyncPath(match.groups()[0])
        if filename_or_path.parent == AsyncPath("."):
            filename_or_path = Settings().VARIABLES_DIR / filename_or_path
        file = init_file(filename_or_path)

        return await file.loads()


class CustomTags:
    list = (FromTag(),)

    @classmethod
    async def apply(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = await cls.apply(value)

        elif isinstance(data, (list, tuple)):
            for i, val in enumerate(data):
                data[i] = await cls.apply(val)

        elif isinstance(data, str):
            for tag in cls.list:
                if match := tag.regex.match(data):
                    data = await tag(match)

        return data


async def tag_loads(data: Any) -> Any:
    return await CustomTags.apply(data)
