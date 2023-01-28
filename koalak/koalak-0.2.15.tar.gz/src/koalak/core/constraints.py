import abc

from koalak.consts import KEY_METADATA_MADE_WITH_METHOD, KEY_PLUGIN_MANAGER

from .bases import GenericField, is_abstract, koalak_object_storage


class BaseConstraint(abc.ABC):
    """Base class to implement constraints on plugins (having specific attribute, abstract method, etc)"""

    @abc.abstractmethod
    def check(self, obj):
        """Main method to define, this method must raise errors when encountering
            none respected constraints

        Args:
            obj: obj to check against"""
        pass


class AttributeConstraint(BaseConstraint):
    """Check if a specific attribute is present or not on subclass, also check
    - its type
    - choices
    """

    def __init__(self, field: GenericField):
        """
        Args:
            field: description to check (take name, type and choices into account)
        """
        self.field = field

    def check(self, plugin):
        # Check if attribute is present
        if not hasattr(plugin, self.field.name):
            raise AttributeError(
                f"Field {self.field.name!r} not present in plugin {plugin.__name__!r}"
            )

        plugin_attr = getattr(plugin, self.field.name)

        # Check type
        if self.field.type is not None:
            if not self.field.check(plugin_attr):
                raise TypeError(
                    f"class attribute {self.field.name!r} must be of type {self.field.type!r}"
                )

        # Check choices
        if self.field.choices:
            if plugin_attr not in self.field.choices:
                raise ValueError(
                    f"class attribute {self.field.name!r} must be in {self.field.choices!r}"
                )

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.field.name})>"


class AbstractMethodConstraint(BaseConstraint):
    """Check if abstract method is implemented or not"""

    def __init__(self, method_name):
        self.method_name = method_name

    def check(self, plugin):
        method = getattr(plugin, self.method_name)
        if is_abstract(method):
            raise AttributeError(
                f"Plugin {plugin.__name__!r} have an abstract method {self.method_name!r}"
            )

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.method_name})>"


class MetadataAttributeIsPresent(BaseConstraint):
    """Check if metadata attribute is present"""

    def check(self, plugin):
        # Check that metadata attribute is present
        # FIXME: we can check metadata presence / type only one time!
        if not hasattr(plugin, "metadata"):
            raise AttributeError(
                f"metadata attribute not present on plugin {plugin.__name__}"
            )


class MetadataAttributeTypeConstraint(BaseConstraint):
    """Check if metadata type is correct, comes after MetadataAttributeIsPresent"""

    def check(self, plugin):
        # Check metadata is an instance of Metadata
        plugin_manager = koalak_object_storage.get(plugin, KEY_PLUGIN_MANAGER)
        if not isinstance(plugin.metadata, plugin_manager.baseplugin.Metadata):
            raise TypeError(
                f"metadata attribute of Plugin {plugin.__name__!r} is not of type 'Metadata'"
            )


class MetadataAttributeConstraint(BaseConstraint):
    """Check if a specific attribute is present or not on a metadata of cls, also check
    - its type
    - choices
    """

    def __init__(self, field: GenericField):
        """
        Args:
            field: description to check (take name, type and choices into account)
        """
        self.field = field

    def check(self, plugin):
        # Check if attribute is present

        if not hasattr(plugin.metadata, self.field.name):
            raise AttributeError(
                f"Field {self.field.name!r} not present in plugin metadata {plugin.__name__!r}"
            )

        plugin_attr = getattr(plugin.metadata, self.field.name)

        # Check type
        if self.field.type is not None:
            if not self.field.check(plugin_attr):
                raise TypeError(
                    f"metadata attribute {self.field.name!r} must be of type {self.field.type!r}"
                )

        # Check choices
        if self.field.choices:
            if plugin_attr not in self.field.choices:
                raise ValueError(
                    f"metadata attribute {self.field.name!r} must be in {self.field.choices!r}"
                )

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.field.name})>"


# TODO: add specific exceptions?
