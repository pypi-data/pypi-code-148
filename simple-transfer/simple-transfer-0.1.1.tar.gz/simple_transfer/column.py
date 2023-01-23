from typing import NamedTuple, Optional


class Column(NamedTuple):
    name: str
    data_type: str
    is_nullable: bool
    varchar_length: Optional[int]

    def to_dict(self):
        return {
            "name": self.name,
            "data_type": self.data_type,
            "is_nullable": self.is_nullable,
            "varchar_length": self.varchar_length,
        }
