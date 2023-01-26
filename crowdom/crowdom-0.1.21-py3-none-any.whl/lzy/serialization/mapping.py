from dataclasses import dataclass
from typing import List

from pure_protobuf.dataclasses_ import field, message

from ... import mapping
from .base import OptionalObject
from .common import ProtobufSerializer


@message
@dataclass
class Objects(ProtobufSerializer[mapping.Objects]):
    objects: List[OptionalObject] = field(1, default_factory=list)

    @staticmethod
    def serialize(obj: mapping.Objects) -> 'Objects':
        return Objects(objects=[OptionalObject.serialize(o) for o in obj])

    def deserialize(self) -> mapping.Objects:
        return tuple([o.deserialize() for o in self.objects])


@message
@dataclass
class TaskSingleSolution(ProtobufSerializer[mapping.TaskSingleSolution]):
    task: Objects = field(1)
    solution: Objects = field(2)

    @staticmethod
    def serialize(obj: mapping.TaskSingleSolution) -> 'TaskSingleSolution':
        task, solution = obj
        return TaskSingleSolution(task=Objects.serialize(task), solution=Objects.serialize(solution))

    def deserialize(self) -> mapping.TaskSingleSolution:
        return self.task.deserialize(), self.solution.deserialize()


@message
@dataclass
class ObjectsList(ProtobufSerializer[List[mapping.Objects]]):
    list: List[Objects] = field(1, default_factory=list)

    @staticmethod
    def serialize(obj: List[mapping.Objects]) -> 'ObjectsList':
        return ObjectsList(list=[Objects.serialize(objects) for objects in obj])

    def deserialize(self) -> List[mapping.Objects]:
        return [objects.deserialize() for objects in self.list]


@message
@dataclass
class TaskSingleSolutionList(ProtobufSerializer[List[mapping.TaskSingleSolution]]):
    list: List[TaskSingleSolution] = field(1, default_factory=list)

    @staticmethod
    def serialize(obj: List[mapping.TaskSingleSolution]) -> 'TaskSingleSolutionList':
        return TaskSingleSolutionList(list=[TaskSingleSolution.serialize(ts) for ts in obj])

    def deserialize(self) -> List[mapping.TaskSingleSolution]:
        return [ts.deserialize() for ts in self.list]
