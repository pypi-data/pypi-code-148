import enum
from uuid import UUID

from hrthy_core.events.events.base_event import BaseEvent, PipelineBasePayload
from hrthy_core.models.constants import (
    PIPELINE_STEP_TYPE_ASSESSMENT,
    PIPELINE_STEP_TYPE_INFO,
    PIPELINE_STEP_TYPE_INTERVIEW,
    PIPELINE_STEP_TYPE_PERSONALITY,
)


class PipelineStepType(enum.Enum):
    INFO = PIPELINE_STEP_TYPE_INFO
    ASSESSMENT = PIPELINE_STEP_TYPE_ASSESSMENT
    PERSONALITY = PIPELINE_STEP_TYPE_PERSONALITY
    INTERVIEW = PIPELINE_STEP_TYPE_INTERVIEW


class PipelineStepCreatedPayload(PipelineBasePayload):
    step_type: PipelineStepType


class PipelineStepDeletedPayload(PipelineStepCreatedPayload):
    pass


class PipelineStepCandidateStartedPayload(PipelineBasePayload):
    pipeline_step_id: UUID
    candidate_id: UUID


class PipelineStepCandidateFinishedPayload(PipelineStepCandidateStartedPayload):
    pass


class PipelineStepCreatedEvent(BaseEvent):
    type = 'PipelineStepCreatedEvent'
    payload: PipelineStepCreatedPayload


class PipelineStepDeletedEvent(BaseEvent):
    type = 'PipelineStepDeletedEvent'
    payload: PipelineStepDeletedPayload


class PipelineStepCandidateStartedEvent(BaseEvent):
    type = 'PipelineStepCandidateStartedEvent'
    payload: PipelineStepCandidateStartedPayload


class PipelineStepCandidateFinishedEvent(BaseEvent):
    type = 'PipelineStepCandidateFinishedEvent'
    payload: PipelineStepCandidateFinishedPayload
