from uuid import UUID

from hrthy_core.events.events.base_event import BaseEvent, CompanyBasePayload


class PipelineCandidateAssignedPayload(CompanyBasePayload):
    candidate_id: UUID


class PipelineCandidateUnassignedPayload(CompanyBasePayload):
    candidate_id: UUID


class PipelineCandidateStartedPayload(CompanyBasePayload):
    candidate_id: UUID
    license_pool_id: UUID


class PipelineCandidateFinishedPayload(CompanyBasePayload):
    candidate_id: UUID


class PipelineCandidateAssignedEvent(BaseEvent):
    type = 'PipelineCandidateAssignedEvent'
    payload: PipelineCandidateAssignedPayload


class PipelineCandidateUnassignedEvent(BaseEvent):
    type = 'PipelineCandidateUnassignedEvent'
    payload: PipelineCandidateUnassignedPayload


class PipelineCandidateStartedEvent(BaseEvent):
    type = 'PipelineCandidateStartedEvent'
    payload: PipelineCandidateStartedPayload


class PipelineCandidateFinishedEvent(BaseEvent):
    type = 'PipelineCandidateFinishedEvent'
    payload: PipelineCandidateFinishedPayload
