from abc import ABC, abstractmethod

_object_types = {}
_delta_types = {}

_objects = {}


class UnknownTypeError(Exception):
    pass


class UnknownObjectError(Exception):
    pass


def register_type(name, object_type, delta_type):
    # TODO check object is TickObject and delta is Structure
    _object_types[name] = object_type
    _delta_types[name] = delta_type


def register_object(name, typeID):
    if typeID not in _object_types:
        raise UnknownTypeError
    _objects[name] = typeID


def get_object(name):
    if name not in _objects:
        raise UnknownObjectError
    typ = _objects[name]
    return _object_types[typ], _delta_types[typ]


class TickObject(ABC):

    @abstractmethod
    def to_snapshot(self):
        pass

    @abstractmethod
    def from_snapshot(self):
        pass

    @abstractmethod
    def deltas_to(self, tobject):
        pass

    @abstractmethod
    def process_deltas(self, deltas):
        pass

    @abstractmethod
    def clone(self):
        pass
