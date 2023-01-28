from typing import AsyncIterator, Literal

from script_master_helper.executor.client import AsyncApi, ApiError, errors
from script_master_helper.executor.schemas import ProcessCreateSchema, ProcessCreateResponseSchema, ProcessDataSchema


class AsyncClient:
    def __init__(self, host, port, settings: dict = None):
        self.api = AsyncApi(api_root=f"http://{host}:{port}", settings=settings)

    async def process_run_stream(
        self, data: ProcessCreateSchema
    ) -> AsyncIterator[bytes]:

        async for block in self.api.stream_endpoint(
            "POST", "/process/run/stream", json=data.dict(exclude_unset=True)
        ):
            yield block

    async def create_process(
        self, data: ProcessCreateSchema
    ) -> ProcessCreateResponseSchema | Literal[False]:
        try:
            data = await self.api.call_endpoint(
                "POST", "/process/create", json=data.dict(exclude_unset=True)
            )
        except ApiError as exc:
            if exc == errors.max_number_processes_error:
                return False
            raise

        return ProcessCreateResponseSchema(**data)

    async def clear_process_info(self, id: str) -> ProcessDataSchema | None:
        data = await self.api.call_endpoint("DELETE", f"/process/{id}")
        return ProcessDataSchema(**data) if data else None

    async def info_of_process(self, id: str) -> ProcessDataSchema:
        data = await self.api.call_endpoint("GET", f"/process/{id}")
        return ProcessDataSchema(**data)

    async def info_all_processes(self) -> list[ProcessDataSchema]:
        data = await self.api.call_endpoint("GET", "/process/all/list")
        return [ProcessDataSchema(**dct) for dct in data]

    async def info_completed_processes(self) -> list[ProcessDataSchema]:
        data = await self.api.call_endpoint("GET", "/process/completed/list")
        return [ProcessDataSchema(**dct) for dct in data]

    async def delete_process_logs(self, id: str) -> bool:
        return await self.api.call_endpoint("GET", f"/process/{id}/logs/delete")

    async def process_logs(self, id: str) -> bytes:
        return await self.api.call_endpoint("GET", f"/process/{id}/logs")

    async def process_logs_stream(self, id: str) -> AsyncIterator[bytes]:
        async for block in self.api.stream_endpoint("GET", f"/process/{id}/logs/stream"):
            yield block