from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserIn")


@attr.s(auto_attribs=True)
class UserIn:
    """
    Attributes:
        username (str):
        firstname (str):
        lastname (str):
        email (str):
        hashed_password (str):
        active (Union[Unset, bool]):  Default: True.
        admin (Union[Unset, bool]):
    """

    username: str
    firstname: str
    lastname: str
    email: str
    hashed_password: str
    active: Union[Unset, bool] = True
    admin: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        firstname = self.firstname
        lastname = self.lastname
        email = self.email
        hashed_password = self.hashed_password
        active = self.active
        admin = self.admin

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "hashed_password": hashed_password,
            }
        )
        if active is not UNSET:
            field_dict["active"] = active
        if admin is not UNSET:
            field_dict["admin"] = admin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        firstname = d.pop("firstname")

        lastname = d.pop("lastname")

        email = d.pop("email")

        hashed_password = d.pop("hashed_password")

        active = d.pop("active", UNSET)

        admin = d.pop("admin", UNSET)

        user_in = cls(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            hashed_password=hashed_password,
            active=active,
            admin=admin,
        )

        user_in.additional_properties = d
        return user_in

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
