import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class EnsureIdentifiable(object):  # we need such ugly inheritance to guarantee default valued fields follows fields without defaults

    def __post_init__(self):
        if not isinstance(self, Identifiable):
            raise TypeError(f"Fact type should inherit {Identifiable}. Actual mro is {type(self).mro()}")


@dataclass(frozen=True)
class Identifiable(EnsureIdentifiable):
    id: str = field(default_factory=lambda: None)

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', self.generate_id())
        for type_ in type(self).mro():
            if issubclass(type_, Identifiable):
                continue
            if hasattr(type_, '__post_init__'):
                type_.__post_init__(self)

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())
