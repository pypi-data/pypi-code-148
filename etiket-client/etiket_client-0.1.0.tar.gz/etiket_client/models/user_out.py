import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.scope_out import ScopeOut
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserOut")


@attr.s(auto_attribs=True)
class UserOut:
    """
    Attributes:
        username (str):
        firstname (str):
        lastname (str):
        email (str):
        active (Union[Unset, bool]):  Default: True.
        admin (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        scopes (Union[Unset, List[ScopeOut]]):
    """

    username: str
    firstname: str
    lastname: str
    email: str
    active: Union[Unset, bool] = True
    admin: Union[Unset, bool] = False
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    scopes: Union[Unset, List[ScopeOut]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        firstname = self.firstname
        lastname = self.lastname
        email = self.email
        active = self.active
        admin = self.admin
        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        scopes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = []
            for scopes_item_data in self.scopes:
                scopes_item = scopes_item_data.to_dict()

                scopes.append(scopes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
            }
        )
        if active is not UNSET:
            field_dict["active"] = active
        if admin is not UNSET:
            field_dict["admin"] = admin
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        firstname = d.pop("firstname")

        lastname = d.pop("lastname")

        email = d.pop("email")

        active = d.pop("active", UNSET)

        admin = d.pop("admin", UNSET)

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

        scopes = []
        _scopes = d.pop("scopes", UNSET)
        for scopes_item_data in _scopes or []:
            scopes_item = ScopeOut.from_dict(scopes_item_data)

            scopes.append(scopes_item)

        user_out = cls(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            active=active,
            admin=admin,
            created=created,
            modified=modified,
            scopes=scopes,
        )

        user_out.additional_properties = d
        return user_out

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
