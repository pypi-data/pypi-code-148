from typing import Any, Dict, List

import attrs
import typeguard
from koalak.consts import OBJECT_STORAGE_KEY


def _attr_nothing_factory():
    """Since attr already use attr.NOTHING for no default args,
    we use the hack as factory so that we can use nothing as default"""
    return attrs.NOTHING


class GenericField:
    """Generic Field class to be used to describe: attribute, columns, collections, etc."""

    def __init__(
        self,
        name: str = None,
        *,
        # Attributes related to arguments/parameters
        kw_only: bool = None,
        default=attrs.NOTHING,
        annotation=None,
        factory=None,
        # Attributes related to type checking
        type=None,
        choices: List = None,
        # Attributes related to documentation
        description: str = None,
        examples: List = None,
        # Attributes related to database
        unique: bool = None,
        indexed: bool = None,
        # additional attributes
        metadata: Dict = None,
    ):
        # check mutual exclusif arguments
        # -------------------------------
        if default is not attrs.NOTHING and factory is not None:
            raise ValueError(f"'default' and 'factory' are mutually exclusive")

        if type is not None and annotation is not None:
            raise ValueError(f"'type' and 'annotation' are mutually exclusive")

        # check parameters based on others
        # --------------------------------
        if type is not None:
            annotation = type

        # Set default arguments
        if kw_only is None:
            kw_only = False

        if indexed is None:
            indexed = False

        if unique is None:
            unique = False

        self.name = name
        self.kw_only = kw_only
        self.default = default
        self.factory = factory
        self.choices = choices
        self.annotation = annotation
        self.description = description
        self.examples = examples
        self.indexed = indexed
        self.unique = unique

    # default = attrs.field(factory=_attr_nothing_factory, kw_only=True)

    # type related
    # ------------
    # raw annotation
    # ref: bool = attrs.field(default=False)
    # many: bool = attrs.field(default=False)
    # in_filter_query: bool = attrs.field(default=False, kw_only=True)

    def get_default(self):
        if self.factory is None:
            return self.default
        return self.factory()

    def build_attrs_field(self):
        return attrs.field(
            default=self.default, factory=self.factory, kw_only=self.kw_only
        )

    def check(self, value):
        """Verify"""
        try:
            typeguard.check_type("varname", value, self.annotation)
            return True
        except TypeError:
            return False

    @property
    def required(self):
        return self.default is attrs.NOTHING and self.factory is None

    @property
    def type(self):
        return self.annotation

    @type.setter
    def type(self, value):
        self.annotation = value

    def __repr__(self):
        return f"GenericField({self.name})"

    # Class methods
    @classmethod
    def build_attrs_dataclass_from_cls(cls, cls_object):
        attributes = {}
        for attr_name, attr in cls_object.__dict__.items():
            if not isinstance(attr, GenericField):
                continue
            attributes[attr_name] = attr.build_attrs_field()

        AttrClass = type(cls_object.__name__, (object,), attributes)
        return attrs.define(AttrClass)


field = GenericField


class ObjectStorage:
    """Class to help storing key, value information inside objects
    mainly used to add fields in objects in the __koalak__ namespace

    Act like setattr and getattr in the chosen key:
        - Will check the base classes to retrieve information
        - etc.
    """

    def __init__(self, key: str):
        self.key = key

    def set(self, obj: Any, name: str, value: Any):
        """Set an attribute in the __dict__ of the object
        Act like setattr on the self.key namespace"""
        if self.key not in obj.__dict__:
            setattr(obj, self.key, {})
        storage = getattr(obj, self.key)
        storage[name] = value

    def getfromobject(self, obj: Any, name: str, default=None):
        """Get the attribute from the object only (using __dict__)
        Without checking cls/bases"""
        # If object don't have __dict__ (like slots or class.__delattr__ do nothing
        if not hasattr(obj, "__dict__"):
            return default

        storage = obj.__dict__.get(self.key, {})
        return storage.get(name, default)

    def get(self, obj: Any, name: str, default=None):
        """Get the attribute by checking the object and its cls/bases"""
        # If object don't have __dict__ (like slots or class.__delattr__ do nothing
        if not hasattr(obj, "__dict__"):
            return default

        objects_to_fetch = self._get_objects_to_fetch(obj)
        for object_to_fetch in objects_to_fetch:
            # get the __dict__ of current object
            storage = object_to_fetch.__dict__.get(self.key)
            # If __koalak__ not in object, check next object
            if storage is None:
                continue

            # If key not in __koalak__ dict, check next object
            if name not in storage:
                continue

            # Object found
            return storage[name]

        return default
        # TODO: what if we store None and default is not the same?

    def setindict(self, obj: Any, dictname: str, name: str, value: Any):
        """Similar to set, but key/value are inside a nested dict"""
        if self.key not in obj.__dict__:
            setattr(obj, self.key, {})

        storage = getattr(obj, self.key)
        if dictname not in storage:
            storage[dictname] = {}

        dict_storage = storage[dictname]
        dict_storage[name] = value

    def getasdict(self, obj: Any, dictname: str) -> Dict:
        """Works with 'setindict' get key, value from object by building a dict through
        its cls/bases"""

        final_dict = {}
        objects_to_fetch = self._get_objects_to_fetch(obj)
        for object_to_fetch in reversed(objects_to_fetch):
            # get the __dict__ of current object
            storage = object_to_fetch.__dict__.get(self.key)

            # If __koalak__ not in object, check next object
            if storage is None:
                continue

            # If key not in __koalak__ dict, check next object
            if dictname not in storage:
                continue

            final_dict.update(storage[dictname])

        return final_dict

    def _get_objects_to_fetch(self, obj):
        """Private method used to get the order of fetching object if it's a cls or an instance"""
        # If they have __mro__ it means it's a class
        if hasattr(obj, "__mro__"):
            # Fetch the class and its bases in the mro order
            return obj.__mro__
        # Else: it's an object
        else:
            # Fetch the object, then it base classes
            return [obj, *obj.__class__.__mro__]


# Instance of object storage with __koalak__ key
koalak_object_storage = ObjectStorage(OBJECT_STORAGE_KEY)


class NamedAndUnnamedContainer:
    """Container to hold named and unnamed objects.
    Can be seen as a List with some elements accessible through string.

    This class is mainly used for koalak containers (framework, plugin managers, hooks)
    Warning:
        This class is not meant for general use, it has unexpected behaviours
        when storing "strings" element and when dealing with 'in' operator'

    TODO: implement removing elements
    """

    def __init__(self):
        self._data = []
        self._index = {}

    def add(self, o: Any, *, name: str = None):
        self._data.append((name, o))
        if name is not None:
            self._index[name] = o

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._index
        return item in (e[1] for e in self._data)

    def __getitem__(self, item):
        return self._index[item]

    def __iter__(self):
        for name, item in self._data:
            yield item

    def __len__(self):
        return len(self._data)

    def __bool__(self):
        return bool(self._data)


def set_abstract(obj):
    koalak_object_storage.set(obj, "abstract", True)


def is_abstract(obj) -> bool:
    return koalak_object_storage.getfromobject(obj, "abstract", False)


def is_cls_abstract(cls):
    return cls.__dict__.get("abstract", False)


def abstract(obj):
    set_abstract(obj)
    return obj
