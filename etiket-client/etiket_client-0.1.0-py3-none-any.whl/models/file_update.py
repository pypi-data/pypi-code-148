from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.file_type import FileType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FileUpdate")


@attr.s(auto_attribs=True)
class FileUpdate:
    """
    Attributes:
        name (Union[Unset, str]):
        mimetype (Union[Unset, str]):
        filetype (Union[Unset, FileType]): An enumeration.
        rating (Union[Unset, int]):
    """

    name: Union[Unset, str] = UNSET
    mimetype: Union[Unset, str] = UNSET
    filetype: Union[Unset, FileType] = UNSET
    rating: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mimetype = self.mimetype
        filetype: Union[Unset, str] = UNSET
        if not isinstance(self.filetype, Unset):
            filetype = self.filetype.value

        rating = self.rating

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if mimetype is not UNSET:
            field_dict["mimetype"] = mimetype
        if filetype is not UNSET:
            field_dict["filetype"] = filetype
        if rating is not UNSET:
            field_dict["rating"] = rating

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        mimetype = d.pop("mimetype", UNSET)

        _filetype = d.pop("filetype", UNSET)
        filetype: Union[Unset, FileType]
        if isinstance(_filetype, Unset):
            filetype = UNSET
        else:
            filetype = FileType(_filetype)

        rating = d.pop("rating", UNSET)

        file_update = cls(
            name=name,
            mimetype=mimetype,
            filetype=filetype,
            rating=rating,
        )

        file_update.additional_properties = d
        return file_update

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
