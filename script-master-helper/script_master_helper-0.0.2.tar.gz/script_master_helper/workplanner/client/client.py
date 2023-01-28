from script_master_helper.workplanner.client import AsyncApi
from script_master_helper.workplanner.enums import Statuses
from script_master_helper.workplanner.schemas import (
    WorkplanQuery, Workplan, WorkplanListGeneric, GenerateWorkplans, WorkplanUpdate, Affected
)


class AsyncClient:
    def __init__(self, host, port=None, settings: dict = None):
        if port:
            api_root = f"http://{host}:{port}"
        else:
            api_root = f"http://{host}"

        self.api = AsyncApi(api_root=api_root, settings=settings)

    async def workplans(self, schema: WorkplanQuery) -> list[Workplan]:
        data = await self.api.call_endpoint(
            f"/workplan/list",
            "POST",
            json=schema.dict(exclude_unset=True),
        )
        return [Workplan(**dct) for dct in data]

    async def generate_workplans(self, schema: GenerateWorkplans) -> list[Workplan]:
        data = await self.api.call_endpoint(
            "/workplan/generate/list",
            "POST",
            json=schema.dict(exclude_none=True),
        )
        return [Workplan(**dct) for dct in data]

    async def workplans_for_execute(self, name: str) -> list[Workplan]:
        data = await self.api.call_endpoint(f"/workplan/execute/{name}/list", "GET")
        return [Workplan(**dct) for dct in data]

    async def change_status(
            self, name, worktime_utc, status: Statuses.LiteralT
    ) -> Workplan:
        schema = WorkplanUpdate(name=name, worktime_utc=worktime_utc, status=status)
        data = await self.api.call_endpoint(
            f"/workplan/update",
            "POST",
            json=schema.dict(exclude_unset=True),
        )
        return Workplan(**data)

    async def update_workplans(self, schemas: list[WorkplanUpdate]) -> Affected:
        data = await self.api.call_endpoint(
            f"/workplan/update/list",
            "POST",
            json=[schema.dict(exclude_unset=True) for schema in schemas],
        )
        return Affected(**data)

    async def update_workplan(self, schema: WorkplanUpdate) -> Workplan:
        data = await self.api.call_endpoint(
            f"/workplan/update",
            "POST",
            json=schema.dict(exclude_unset=True),
        )
        return Workplan(**data)

    async def replay(self, id: str) -> Workplan:
        data = await self.api.call_endpoint(f"/workplan/{id}/replay", "GET")
        return Workplan(**data)
