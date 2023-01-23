from jija.drivers import base


class DatabaseDriver(base.Driver):
    @classmethod
    async def preflight(cls):
        raise NotImplementedError()

    @classmethod
    async def get_connection(cls):
        raise NotImplementedError()


class JijaOrmDriver(DatabaseDriver):
    @classmethod
    async def preflight(cls):
        from jija_orm import config as jija_orm_config
        from jija import config

        await jija_orm_config.JijaORM.async_init(
            project_dir=config.StructureConfig.PROJECT_PATH,
            connection=jija_orm_config.Connection(
                host=config.DatabaseConfig.HOST,
                port=config.DatabaseConfig.PORT,
                user=config.DatabaseConfig.USER,
                database=config.DatabaseConfig.DATABASE,
                password=config.DatabaseConfig.PASSWORD
            ),
            apps=await cls.__get_apps()
        )

    @classmethod
    async def __get_apps(cls):
        from jija_orm import config as jija_orm_config
        from jija.apps import Apps

        apps = []
        for app in Apps.apps.values():
            if app.exist('models.py'):
                path = app.name if app.parent is None else f'apps.{app.name}'
                apps.append(jija_orm_config.App(
                    name=app.name, path=path, migration_dir=app.get_import_path('migrations')))

        return apps

    @classmethod
    async def get_connection(cls):
        pass
