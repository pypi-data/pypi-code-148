from aiohttp import web


class Config:
    __REQUIRED_ADDONS = set()
    __PREF = {}

    def __init__(self, **kwargs):
        from jija import apps

        self.__class__.__PREF = kwargs
        apps.Apps.config_init_callback(self.__class__)

    @classmethod
    async def freeze(cls):
        validated_data = await cls.validate(cls.__PREF)
        cls.set_values(validated_data)

    @classmethod
    async def validate(cls, values: dict) -> dict:
        validated_data = {}
        for name, value in values.items():
            name = name.upper()
            field = getattr(cls, name)
            validated_data[name.upper()] = await field.validate(value)

        return validated_data

    @classmethod
    def set_values(cls, validated_data: dict):
        for name, value in validated_data.items():
            setattr(cls, name, value)

    @classmethod
    def base_app_update(cls, aiohttp_app: web.Application) -> web.Application:
        return aiohttp_app

    @classmethod
    def each_app_update(cls, aiohttp_app: web.Application) -> web.Application:
        return aiohttp_app

    @classmethod
    async def preflight(cls):
        pass
