from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

T = TypeVar("T", bound="DatasetMetaMeta")


@attr.s(auto_attribs=True)
class DatasetMetaMeta:
    """ """

    additional_properties: Dict[str, Union[List[str], str]] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():

            if isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dataset_meta_meta = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Union[List[str], str]:
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_0 = cast(List[str], data)

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                return cast(Union[List[str], str], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        dataset_meta_meta.additional_properties = additional_properties
        return dataset_meta_meta

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union[List[str], str]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union[List[str], str]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
