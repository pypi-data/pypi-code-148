from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserUpdate")


@attr.s(auto_attribs=True)
class UserUpdate:
    """
    Attributes:
        username (Union[Unset, str]):
        firstname (Union[Unset, str]):
        lastname (Union[Unset, str]):
        email (Union[Unset, str]):
        active (Union[Unset, str]):
        admin (Union[Unset, bool]):
        hashed_password (Union[Unset, str]):
    """

    username: Union[Unset, str] = UNSET
    firstname: Union[Unset, str] = UNSET
    lastname: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    active: Union[Unset, str] = UNSET
    admin: Union[Unset, bool] = UNSET
    hashed_password: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        firstname = self.firstname
        lastname = self.lastname
        email = self.email
        active = self.active
        admin = self.admin
        hashed_password = self.hashed_password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if firstname is not UNSET:
            field_dict["firstname"] = firstname
        if lastname is not UNSET:
            field_dict["lastname"] = lastname
        if email is not UNSET:
            field_dict["email"] = email
        if active is not UNSET:
            field_dict["active"] = active
        if admin is not UNSET:
            field_dict["admin"] = admin
        if hashed_password is not UNSET:
            field_dict["hashed_password"] = hashed_password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username", UNSET)

        firstname = d.pop("firstname", UNSET)

        lastname = d.pop("lastname", UNSET)

        email = d.pop("email", UNSET)

        active = d.pop("active", UNSET)

        admin = d.pop("admin", UNSET)

        hashed_password = d.pop("hashed_password", UNSET)

        user_update = cls(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            active=active,
            admin=admin,
            hashed_password=hashed_password,
        )

        user_update.additional_properties = d
        return user_update

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
