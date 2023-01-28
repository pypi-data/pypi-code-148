import pendulum
from jinja2 import Template

from script_master.settings import Settings


class DateTimeFunc:
    __slots__ = ("method",)

    def __init__(self, method: str = "now"):
        self.method = method

    def __call__(self, tzname=None):
        return getattr(pendulum, self.method)(tzname)

    def __str__(self):
        return self().format("YYYY-MM-DD HH:mm:ss")


class DateFunc:
    __slots__ = ("method",)

    def __init__(self, method: str = "today"):
        self.method = method

    def __call__(self, tzname=None):
        dt: pendulum.DateTime = getattr(pendulum, self.method)(tzname)
        return pendulum.datetime(dt.year, dt.month, dt.day)

    def __str__(self):
        return self().format("YYYY-MM-DD")


default_kwargs_for_render = dict(
    now=DateTimeFunc(),
    today=DateFunc(),
    tomorrow=DateFunc("tomorrow"),
    yesterday=DateFunc("yesterday"),
    filename=None,
    filepath=None,
    notebook_name=None,
    worktime=None,
    workdate=None,
)


async def get_variables_map(**kwargs) -> dict:
    from script_master.notebook import init_file

    dct = {**default_kwargs_for_render, **kwargs}
    data = {}
    async for path in Settings().VARIABLES_DIR.rglob("*"):
        if await path.is_file():
            file = init_file(path)
            data[file.name] = await file.loads(dct)

    return data


async def render_template(text: str, **kwargs) -> str:
    template = Template(text, enable_async=True)
    dct = {**default_kwargs_for_render, **kwargs}

    return await template.render_async(**dct)


async def render_template_with_variables(text: str, **kwargs):
    variables_map = await get_variables_map(**kwargs)
    return await render_template(text, **variables_map)
