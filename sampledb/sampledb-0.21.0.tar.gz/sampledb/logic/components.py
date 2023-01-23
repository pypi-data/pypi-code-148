# coding: utf-8
"""
"""
import datetime
from uuid import UUID
import dataclasses
import typing
import re
from flask_babel import _
import flask

from .. import db
from ..models import components, objects, component_authentication
from . import errors
from .utils import cache

# component names are limited to this (semi-arbitrary) length
MAX_COMPONENT_NAME_LENGTH = 100
MAX_COMPONENT_ADDRESS_LENGTH = 100


@dataclasses.dataclass(frozen=True)
class Component:
    """
    This class provides an immutable wrapper around models.federation.FederationComponent.
    """
    id: int
    uuid: str
    name: typing.Optional[str]
    address: typing.Optional[str]
    description: typing.Optional[str]
    last_sync_timestamp: typing.Optional[datetime.datetime]
    import_token_available: bool

    @classmethod
    def from_database(cls, component: components.Component) -> 'Component':
        import_token_available = False
        if db.session.query(db.exists().where(component_authentication.OwnComponentAuthentication.component_id == component.id)).scalar():  # type: ignore
            import_token_available = True
        return Component(id=component.id, address=component.address, uuid=component.uuid, name=component.name, description=component.description, last_sync_timestamp=component.last_sync_timestamp, import_token_available=import_token_available)

    def get_name(self) -> str:
        if self.name is None:
            if self.address is not None:
                regex = re.compile(r"https?://(www\.)?")    # should usually be https
                return regex.sub('', self.address).strip().strip('/')
            return _('Database #%(id)s', id=self.id)  # type: ignore
        else:
            return self.name

    def update_last_sync_timestamp(
            self,
            last_sync_timestamp: datetime.datetime
    ) -> None:
        component = components.Component.query.filter_by(id=self.id).first()
        component.last_sync_timestamp = last_sync_timestamp
        db.session.add(component)
        db.session.commit()


def validate_address(
        address: str,
        max_length: int = 100,
        allow_http: bool = False
) -> str:
    if not 1 <= len(address) <= max_length:
        raise errors.InvalidComponentAddressError()
    if address[:8] != 'https://' and address[:7] != 'http://':
        address = 'https://' + address

    regex = re.compile(
        r'^(?:http)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, address) is None:
        raise errors.InvalidComponentAddressError()

    if not allow_http and address[:7] == 'http://':
        raise errors.InsecureComponentAddressError()

    return address


def get_components() -> typing.List[Component]:
    """
    Returns a list of all existing components.

    :return: the list of components
    """
    return [Component.from_database(component) for component in components.Component.query.order_by(db.asc(components.Component.name)).all()]


def add_component(
        uuid: str,
        name: typing.Optional[str] = None,
        address: typing.Optional[str] = None,
        description: typing.Optional[str] = ''
) -> Component:
    """
    Adds a new component with the given address, name and description.

    :param uuid: the uuid of the component
    :param name: a (possibly empty) name for the component
    :param address: the address of the component
    :param description: a (possibly empty) description for the component
    :return: the newly added component
    :raise errors.InvalidComponentNameError: when the component name is more
        than MAX_COMPONENT_NAME_LENGTH characters long
    :raise errors.InvalidComponentAddressError: when the component address is empty or more
        than MAX_COMPONENT_ADDRESS_LENGTH characters long
    :raise errors.InvalidComponentUUIDError: when the component uuid does not match the UUID format
    :raise errors.ComponentAlreadyExistsError: when another component with the given
        name already exists
    """
    if name is not None and not 1 <= len(name) <= MAX_COMPONENT_NAME_LENGTH:
        raise errors.InvalidComponentNameError()
    if address is not None:
        address = validate_address(address, max_length=MAX_COMPONENT_ADDRESS_LENGTH, allow_http=flask.current_app.config['ALLOW_HTTP'])
    try:
        uuid_obj = UUID(uuid)
        uuid = str(uuid_obj)
    except ValueError:
        raise errors.InvalidComponentUUIDError()
    except TypeError:
        raise errors.InvalidComponentUUIDError()

    if name is not None:
        existing_component = components.Component.query.filter_by(name=name).first()
        if existing_component is not None:
            raise errors.ComponentAlreadyExistsError()
    existing_component = components.Component.query.filter_by(uuid=uuid).first()
    if existing_component is not None:
        raise errors.ComponentAlreadyExistsError()

    component = components.Component(uuid=uuid, name=name, description=description, address=address)
    db.session.add(component)
    db.session.commit()

    return Component.from_database(component)


@cache
def check_component_exists(
        component_id: int
) -> None:
    """
    Check whether a component with the given component ID exists.

    :param component_id: the ID of an existing component
    :raise errors.ComponentDoesNotExistError: when no component with the given
        component ID exists
    """
    if not db.session.query(db.exists().where(components.Component.id == component_id)).scalar():  # type: ignore
        raise errors.ComponentDoesNotExistError()


def get_component(
        component_id: int
) -> Component:
    """
    Returns the federation component with the given ID.

    :param component_id: the ID of an existing component
    :return: the component
    :raise errors.ComponentDoesNotExistError: when no component with the given
        component ID exists
    """
    component = components.Component.query.filter_by(id=component_id).first()
    if component is None:
        raise errors.ComponentDoesNotExistError()
    return Component.from_database(component)


def get_component_or_none(
        component_id: typing.Optional[int]
) -> typing.Optional[Component]:
    if component_id is None:
        return None
    try:
        return get_component(component_id)
    except errors.ComponentDoesNotExistError:
        return None


def get_component_by_uuid(
        component_uuid: str
) -> Component:
    try:
        uuid_obj = UUID(component_uuid)
        component_uuid = str(uuid_obj)
    except ValueError:
        raise errors.InvalidComponentUUIDError()
    except TypeError:
        raise errors.InvalidComponentUUIDError()
    component = components.Component.query.filter_by(uuid=component_uuid).first()
    if component is None:
        raise errors.ComponentDoesNotExistError
    return Component.from_database(component)


def get_component_id_by_uuid(
        component_uuid: typing.Optional[str]
) -> typing.Optional[int]:
    """
    Get the component ID for a given UUID.

    :param component_uuid: a UUID, or None
    :return: the matching component ID, or None
    """
    if component_uuid is None:
        return None
    # component_uuid is not validated as no exceptions should be raised from
    # this function, so an invalid UUID returns None just as an unknown one.
    component = components.Component.query.filter_by(uuid=component_uuid).first()
    if component is None:
        return None
    return typing.cast(int, component.id)


def update_component(component_id: int, name: typing.Optional[str] = None, address: typing.Optional[str] = None, description: typing.Optional[str] = '') -> None:
    """
    Updates the component's address, name and description.

    :param component_id: the ID of an existing component
    :param name: the new unique component name
    :param address: the address of the component
    :param description: the new component description
    :param name: the new component address
    :raise errors.InvalidComponentNameError: when the component name is more
        than MAX_COMPONENT_NAME_LENGTH characters long
    :raise errors.InvalidComponentAddressError: when the component address is empty or more
        than MAX_COMPONENT_ADDRESS_LENGTH characters long
    :raise errors.ComponentDoesNotExistError: when no component with the given
        component ID exists
    :raise errors.ComponentAlreadyExistsError: when another component with the given
        name or uuid already exists
    """
    if name is not None and not 1 <= len(name) <= MAX_COMPONENT_NAME_LENGTH:
        raise errors.InvalidComponentNameError()
    if address is not None:
        address = validate_address(address, max_length=MAX_COMPONENT_ADDRESS_LENGTH, allow_http=flask.current_app.config['ALLOW_HTTP'])

    component = components.Component.query.filter_by(id=component_id).first()
    if component is None:
        raise errors.ComponentDoesNotExistError()
    if component.name != name and name is not None:
        existing_component = components.Component.query.filter_by(name=name).first()
        if existing_component is not None:
            raise errors.ComponentAlreadyExistsError()

    component.address = address
    component.name = name
    component.description = description
    db.session.add(component)
    db.session.commit()


def get_object_ids_for_component_id(
        component_id: int
) -> typing.Set[int]:
    """
    Get the set of object IDs for all objects imported from a given component.

    :param component_id: the ID of an existing component
    :return: the set of object IDs
    :raise errors.ComponentDoesNotExistError: when no component with the given
        component ID exists
    """
    object_ids = db.session.query(  # type: ignore
        objects.Objects._current_table.c.object_id
    ).filter(
        objects.Objects._current_table.c.component_id == component_id
    ).all()
    if not object_ids:
        # ensure component exists
        check_component_exists(component_id)
    return {
        row[0]
        for row in object_ids
    }


def get_object_ids_for_components() -> typing.Set[int]:
    """
    Get the set of object IDs for all objects imported from a component.

    :return: the set of object IDs
    """
    object_ids = db.session.query(  # type: ignore
        objects.Objects._current_table.c.object_id
    ).filter(
        db.not_(objects.Objects._current_table.c.component_id.is_(db.null()))
    ).all()
    return {
        row[0]
        for row in object_ids
    }


def get_local_object_ids() -> typing.Set[int]:
    """
    Get the set of object IDs for all objects not imported from any component.

    :return: the set of object IDs
    """
    object_ids = db.session.query(  # type: ignore
        objects.Objects._current_table.c.object_id
    ).filter(
        objects.Objects._current_table.c.component_id.is_(db.null())
    ).all()
    return {
        row[0]
        for row in object_ids
    }
