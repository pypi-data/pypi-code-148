from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="DatasetMetaKeys")


@attr.s(auto_attribs=True)
class DatasetMetaKeys:
    """
    Attributes:
        keys (List[str]):
    """

    keys: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        keys = self.keys

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "keys": keys,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        keys = cast(List[str], d.pop("keys"))

        dataset_meta_keys = cls(
            keys=keys,
        )

        dataset_meta_keys.additional_properties = d
        return dataset_meta_keys

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
