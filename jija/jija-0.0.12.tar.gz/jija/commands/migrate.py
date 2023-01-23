from jija.command import Command


class Migrate(Command):
    async def handle(self):
        from jija_orm.migrator import migrator

        migrator_instance = migrator.Migrator()
        await migrator_instance.migrate()

