import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetUpdate")


@attr.s(auto_attribs=True)
class DatasetUpdate:
    """
    Attributes:
        name (Union[Unset, str]):
        started (Union[Unset, datetime.datetime]):
        duration (Union[Unset, float]):
        description (Union[Unset, str]):
        creator (Union[Unset, str]):
        ranking (Union[Unset, int]):
    """

    name: Union[Unset, str] = UNSET
    started: Union[Unset, datetime.datetime] = UNSET
    duration: Union[Unset, float] = UNSET
    description: Union[Unset, str] = UNSET
    creator: Union[Unset, str] = UNSET
    ranking: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        started: Union[Unset, str] = UNSET
        if not isinstance(self.started, Unset):
            started = self.started.isoformat()

        duration = self.duration
        description = self.description
        creator = self.creator
        ranking = self.ranking

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if started is not UNSET:
            field_dict["started"] = started
        if duration is not UNSET:
            field_dict["duration"] = duration
        if description is not UNSET:
            field_dict["description"] = description
        if creator is not UNSET:
            field_dict["creator"] = creator
        if ranking is not UNSET:
            field_dict["ranking"] = ranking

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _started = d.pop("started", UNSET)
        started: Union[Unset, datetime.datetime]
        if isinstance(_started, Unset):
            started = UNSET
        else:
            started = isoparse(_started)

        duration = d.pop("duration", UNSET)

        description = d.pop("description", UNSET)

        creator = d.pop("creator", UNSET)

        ranking = d.pop("ranking", UNSET)

        dataset_update = cls(
            name=name,
            started=started,
            duration=duration,
            description=description,
            creator=creator,
            ranking=ranking,
        )

        dataset_update.additional_properties = d
        return dataset_update

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
