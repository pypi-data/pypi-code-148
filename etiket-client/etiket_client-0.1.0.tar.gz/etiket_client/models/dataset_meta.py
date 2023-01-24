from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.dataset_meta_meta import DatasetMetaMeta

T = TypeVar("T", bound="DatasetMeta")


@attr.s(auto_attribs=True)
class DatasetMeta:
    """
    Attributes:
        meta (DatasetMetaMeta):
    """

    meta: DatasetMetaMeta
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        meta = self.meta.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "meta": meta,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        meta = DatasetMetaMeta.from_dict(d.pop("meta"))

        dataset_meta = cls(
            meta=meta,
        )

        dataset_meta.additional_properties = d
        return dataset_meta

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
