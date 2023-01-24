from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScopeUpdate")


@attr.s(auto_attribs=True)
class ScopeUpdate:
    """
    Attributes:
        description (Union[Unset, str]):
        restricted (Union[Unset, bool]):
        archived (Union[Unset, bool]):
    """

    description: Union[Unset, str] = UNSET
    restricted: Union[Unset, bool] = UNSET
    archived: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        restricted = self.restricted
        archived = self.archived

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if restricted is not UNSET:
            field_dict["restricted"] = restricted
        if archived is not UNSET:
            field_dict["archived"] = archived

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        restricted = d.pop("restricted", UNSET)

        archived = d.pop("archived", UNSET)

        scope_update = cls(
            description=description,
            restricted=restricted,
            archived=archived,
        )

        scope_update.additional_properties = d
        return scope_update

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
