from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyRefreshToken")


@attr.s(auto_attribs=True)
class BodyRefreshToken:
    """
    Attributes:
        grant_type (str):
        refresh_token (str):
    """

    grant_type: str
    refresh_token: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        grant_type = self.grant_type
        refresh_token = self.refresh_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "grant_type": grant_type,
                "refresh_token": refresh_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        grant_type = d.pop("grant_type")

        refresh_token = d.pop("refresh_token")

        body_refresh_token = cls(
            grant_type=grant_type,
            refresh_token=refresh_token,
        )

        body_refresh_token.additional_properties = d
        return body_refresh_token

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
