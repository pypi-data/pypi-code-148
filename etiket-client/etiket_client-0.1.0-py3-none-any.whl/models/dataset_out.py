import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.collection_dataset_out import CollectionDatasetOut
from ..models.dataset_out_meta import DatasetOutMeta
from ..models.file_dataset_out import FileDatasetOut
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetOut")


@attr.s(auto_attribs=True)
class DatasetOut:
    """
    Attributes:
        name (str):
        uid (str):
        scope (str):
        collections (List[CollectionDatasetOut]):
        creator (Union[Unset, str]):
        description (Union[Unset, str]):
        meta (Union[Unset, DatasetOutMeta]):
        started (Union[Unset, datetime.datetime]):
        duration (Union[Unset, float]):
        ranking (Union[Unset, int]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        files (Union[Unset, List[FileDatasetOut]]):
    """

    name: str
    uid: str
    scope: str
    collections: List[CollectionDatasetOut]
    creator: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    meta: Union[Unset, DatasetOutMeta] = UNSET
    started: Union[Unset, datetime.datetime] = UNSET
    duration: Union[Unset, float] = UNSET
    ranking: Union[Unset, int] = 0
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    files: Union[Unset, List[FileDatasetOut]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        uid = self.uid
        scope = self.scope
        collections = []
        for collections_item_data in self.collections:
            collections_item = collections_item_data.to_dict()

            collections.append(collections_item)

        creator = self.creator
        description = self.description
        meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        started: Union[Unset, str] = UNSET
        if not isinstance(self.started, Unset):
            started = self.started.isoformat()

        duration = self.duration
        ranking = self.ranking
        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

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
                "collections": collections,
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
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        uid = d.pop("uid")

        scope = d.pop("scope")

        collections = []
        _collections = d.pop("collections")
        for collections_item_data in _collections:
            collections_item = CollectionDatasetOut.from_dict(collections_item_data)

            collections.append(collections_item)

        creator = d.pop("creator", UNSET)

        description = d.pop("description", UNSET)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, DatasetOutMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            #meta = DatasetOutMeta.from_dict(_meta)
            meta = _meta

        _started = d.pop("started", UNSET)
        started: Union[Unset, datetime.datetime]
        if isinstance(_started, Unset):
            started = UNSET
        else:
            started = isoparse(_started) if _started else None

        duration = d.pop("duration", UNSET)

        ranking = d.pop("ranking", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = FileDatasetOut.from_dict(files_item_data)

            files.append(files_item)

        dataset_out = cls(
            name=name,
            uid=uid,
            scope=scope,
            collections=collections,
            creator=creator,
            description=description,
            meta=meta,
            started=started,
            duration=duration,
            ranking=ranking,
            created=created,
            modified=modified,
            files=files,
        )

        dataset_out.additional_properties = d
        return dataset_out

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
