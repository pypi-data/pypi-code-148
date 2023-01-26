from uuid import UUID

from hrthy_core.events.events.base_event import BaseEvent, CompanyBasePayload


class PipelineManagerAssignedPayload(CompanyBasePayload):
    user_id: UUID


class PipelineManagerUnassignedPayload(CompanyBasePayload):
    user_id: UUID


class PipelineManagerAssignedEvent(BaseEvent):
    type = 'PipelineManagerAssignedEvent'
    payload: PipelineManagerAssignedPayload


class PipelineManagerUnassignedEvent(BaseEvent):
    type = 'PipelineManagerUnassignedEvent'
    payload: PipelineManagerUnassignedPayload
