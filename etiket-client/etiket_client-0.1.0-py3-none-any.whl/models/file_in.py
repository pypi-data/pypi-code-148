from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.file_type import FileType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FileIn")


@attr.s(auto_attribs=True)
class FileIn:
    """
    Attributes:
        name (str):
        uid (str):
        dataset_uid (str):
        scope (str):
        creator (Union[Unset, str]):
        etag (Union[Unset, str]):
        size (Union[Unset, int]):
        mimetype (Union[Unset, str]):  Default: 'application/octet-stream'.
        altlocation (Union[Unset, str]):
        rating (Union[Unset, int]):
        immutable (Union[Unset, bool]):  Default: True.
        filetype (Union[Unset, FileType]): An enumeration.
    """

    name: str
    uid: str
    dataset_uid: str
    scope: str
    creator: Union[Unset, str] = UNSET
    etag: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    mimetype: Union[Unset, str] = "application/octet-stream"
    altlocation: Union[Unset, str] = UNSET
    rating: Union[Unset, int] = 0
    immutable: Union[Unset, bool] = True
    filetype: Union[Unset, FileType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        uid = self.uid
        dataset_uid = self.dataset_uid
        scope = self.scope
        creator = self.creator
        etag = self.etag
        size = self.size
        mimetype = self.mimetype
        altlocation = self.altlocation
        rating = self.rating
        immutable = self.immutable
        filetype: Union[Unset, str] = UNSET
        if not isinstance(self.filetype, Unset):
            filetype = self.filetype.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "uid": uid,
                "dataset_uid": dataset_uid,
                "scope": scope,
            }
        )
        if creator is not UNSET:
            field_dict["creator"] = creator
        if etag is not UNSET:
            field_dict["etag"] = etag
        if size is not UNSET:
            field_dict["size"] = size
        if mimetype is not UNSET:
            field_dict["mimetype"] = mimetype
        if altlocation is not UNSET:
            field_dict["altlocation"] = altlocation
        if rating is not UNSET:
            field_dict["rating"] = rating
        if immutable is not UNSET:
            field_dict["immutable"] = immutable
        if filetype is not UNSET:
            field_dict["filetype"] = filetype

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        uid = d.pop("uid")

        dataset_uid = d.pop("dataset_uid")

        scope = d.pop("scope")

        creator = d.pop("creator", UNSET)

        etag = d.pop("etag", UNSET)

        size = d.pop("size", UNSET)

        mimetype = d.pop("mimetype", UNSET)

        altlocation = d.pop("altlocation", UNSET)

        rating = d.pop("rating", UNSET)

        immutable = d.pop("immutable", UNSET)

        _filetype = d.pop("filetype", UNSET)
        filetype: Union[Unset, FileType]
        if isinstance(_filetype, Unset):
            filetype = UNSET
        else:
            filetype = FileType(_filetype)

        file_in = cls(
            name=name,
            uid=uid,
            dataset_uid=dataset_uid,
            scope=scope,
            creator=creator,
            etag=etag,
            size=size,
            mimetype=mimetype,
            altlocation=altlocation,
            rating=rating,
            immutable=immutable,
            filetype=filetype,
        )

        file_in.additional_properties = d
        return file_in

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
