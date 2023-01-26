import enum

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


class PipelineStepDeletedPayload(PipelineBasePayload):
    step_type: PipelineStepType


class PipelineStepCreatedEvent(BaseEvent):
    type = 'PipelineStepCreatedEvent'
    payload: PipelineStepCreatedPayload


class PipelineStepDeletedEvent(BaseEvent):
    type = 'PipelineStepDeletedEvent'
    payload: PipelineStepDeletedPayload
