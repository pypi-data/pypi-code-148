from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScopeIn")


@attr.s(auto_attribs=True)
class ScopeIn:
    """
    Attributes:
        name (str):
        description (str):
        restricted (Union[Unset, bool]):
        archived (Union[Unset, bool]):
    """

    name: str
    description: str
    restricted: Union[Unset, bool] = False
    archived: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        restricted = self.restricted
        archived = self.archived

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
            }
        )
        if restricted is not UNSET:
            field_dict["restricted"] = restricted
        if archived is not UNSET:
            field_dict["archived"] = archived

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        restricted = d.pop("restricted", UNSET)

        archived = d.pop("archived", UNSET)

        scope_in = cls(
            name=name,
            description=description,
            restricted=restricted,
            archived=archived,
        )

        scope_in.additional_properties = d
        return scope_in

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
