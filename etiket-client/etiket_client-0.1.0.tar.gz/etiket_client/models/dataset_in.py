import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.dataset_in_meta import DatasetInMeta
from ..models.file_dataset_in import FileDatasetIn
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetIn")


@attr.s(auto_attribs=True)
class DatasetIn:
    """
    Attributes:
        name (str):
        uid (str):
        scope (str):
        creator (Union[Unset, str]):
        description (Union[Unset, str]):
        meta (Union[Unset, DatasetInMeta]):
        started (Union[Unset, datetime.datetime]):
        duration (Union[Unset, float]):
        ranking (Union[Unset, int]):
        files (Union[Unset, List[FileDatasetIn]]):
    """

    name: str
    uid: str
    scope: str
    creator: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    meta: Union[Unset, DatasetInMeta] = UNSET
    started: Union[Unset, datetime.datetime] = UNSET
    duration: Union[Unset, float] = UNSET
    ranking: Union[Unset, int] = 0
    files: Union[Unset, List[FileDatasetIn]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        uid = self.uid
        scope = self.scope
        creator = self.creator
        description = self.description
        meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            #meta = self.meta.to_dict()
            meta = self.meta

        started: Union[Unset, str] = UNSET
        if not isinstance(self.started, Unset):
            #started = self.started.isoformat()
            started = self.started

        duration = self.duration
        ranking = self.ranking
        files: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "uid": uid,
                "scope": scope,
            }
        )
        if creator is not UNSET:
            field_dict["creator"] = creator
        if description is not UNSET:
            field_dict["description"] = description
        if meta is not UNSET:
            field_dict["meta"] = meta
        if started is not UNSET:
            field_dict["started"] = started
        if duration is not UNSET:
            field_dict["duration"] = duration
        if ranking is not UNSET:
            field_dict["ranking"] = ranking
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        uid = d.pop("uid")

        scope = d.pop("scope")

        creator = d.pop("creator", UNSET)

        description = d.pop("description", UNSET)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, DatasetInMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = DatasetInMeta.from_dict(_meta)

        _started = d.pop("started", UNSET)
        started: Union[Unset, datetime.datetime]
        if isinstance(_started, Unset):
            started = UNSET
        else:
            started = isoparse(_started)

        duration = d.pop("duration", UNSET)

        ranking = d.pop("ranking", UNSET)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = FileDatasetIn.from_dict(files_item_data)

            files.append(files_item)

        dataset_in = cls(
            name=name,
            uid=uid,
            scope=scope,
            creator=creator,
            description=description,
            meta=meta,
            started=started,
            duration=duration,
            ranking=ranking,
            files=files,
        )

        dataset_in.additional_properties = d
        return dataset_in

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
