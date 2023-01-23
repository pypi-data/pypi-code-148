from enum import Enum

class GraphStatus(Enum):
    IDLE='IDLE'
    INITIALIZING='INITIALIZING'
    VALIDATING='VALIDATING'
    ASSEMBLING='ASSEMBLING'
    RUNNING='RUNNING'
    COMPLETE='COMPLETE'
    FAILED='FAILED'