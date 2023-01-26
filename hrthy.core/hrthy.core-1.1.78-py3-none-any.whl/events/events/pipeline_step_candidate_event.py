from uuid import UUID

from hrthy_core.events.events.base_event import BaseEvent, PipelineBasePayload


class PipelineStepCandidateStartedPayload(PipelineBasePayload):
    candidate_id: UUID


class PipelineStepCandidateFinishedPayload(PipelineBasePayload):
    candidate_id: UUID


class PipelineStepCandidateStartedEvent(BaseEvent):
    type = 'PipelineStepCandidateStartedEvent'
    payload: PipelineStepCandidateStartedPayload


class PipelineStepCandidateFinishedEvent(BaseEvent):
    type = 'PipelineStepCandidateFinishedEvent'
    payload: PipelineStepCandidateFinishedPayload
