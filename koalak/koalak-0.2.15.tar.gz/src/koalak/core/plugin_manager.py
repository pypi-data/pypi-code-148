import glob
import inspect
import os
from typing import Dict, List

from koalak.consts import (
    KEY_ATTRIBUTES_CONSTRAINTS,
    KEY_METADATA_MADE_WITH_METHOD,
    KEY_PLUGIN_MANAGER,
    OBJECT_STORAGE_KEY,
)

from .bases import (
    GenericField,
    NamedAndUnnamedContainer,
    abstract,
    field,
    is_abstract,
    is_cls_abstract,
    koalak_object_storage,
)
from .constraints import (
    AbstractMethodConstraint,
    AttributeConstraint,
    BaseConstraint,
    MetadataAttributeConstraint,
    MetadataAttributeIsPresent,
    MetadataAttributeTypeConstraint,
)


def init_subclass_for_baseplugin(subcls, **kwargs):
    """__init_subclass__ method to inject in the baseplugin cls"""

    plugin_manager: PluginManager = koalak_object_storage.get(
        subcls, KEY_PLUGIN_MANAGER
    )

    if plugin_manager is None:
        raise ValueError(
            f"plugin_manager not set in {OBJECT_STORAGE_KEY} attribute for baseplugin"
        )

    # Automatically register subclasses only if 'autoregister' is True
    if plugin_manager.autoregister:
        plugin_manager.register(subcls)


class PluginManager:
    """
    Container for plugins (add, request, specify plugins).

    This is the most important feature of koalak.

    """

    def __init__(
        self,
        name: str = None,
        *,
        autoregister: bool = None,
        autocheck: bool = None,
        homepath: str = None,
    ):
        """

        Args:
            name: name of the plugin manager (can be None)
            autoregister: if True, automatically register plugins when subclassing baseplugin
            autocheck: if True, automatically check if plugins are well constructed
            homepath: path for plugin manager, to load home plugins

        How it works:
            constraints:
        """

        # TODO: add option to disable loading from homepath

        if autoregister is None:
            autoregister = True

        if autocheck is None:
            autocheck = True

        self.name: str = name
        self.baseplugin = None
        self.homepath: str = homepath
        self.autoregister: bool = autoregister  # TODO: implement then test me
        self.autocheck: bool = autocheck  # TODO implement me / test me
        self.plugins: NamedAndUnnamedContainer = NamedAndUnnamedContainer()
        self.abstract_plugins: NamedAndUnnamedContainer = NamedAndUnnamedContainer()
        self._metadata_attributes_constraints: Dict[
            str, MetadataAttributeConstraint
        ] = {}
        self._other_constraints: List[BaseConstraint] = []
        self._initialized: bool = False
        self._metadata_have_at_least_one_required_field = False

    def __contains__(self, item):
        """If plugin or name of plugin is contained, return True"""
        return self.plugins.__contains__(item)

    def __getitem__(self, item: str):
        return self.plugins.__getitem__(item)

    def __iter__(self):
        return self.plugins.__iter__()

    def __len__(self):
        """Return number of plugins (without abstract plugins)"""
        return len(self.plugins)

    def __bool__(self):
        return bool(self.plugins)

    def __repr__(self):
        if self.name:
            return f"<PluginManager [{self.name}]>"
        else:
            return f"<PluginManager>"

    def __str__(self):
        return self.__repr__()

    def __call__(self, **kwargs):
        # TODO: check me / document me
        for plugin in self:
            if not hasattr(plugin, "metadata"):
                continue

            skip_iteration = False
            for key, value in kwargs.items():
                if plugin.metadata.get(key) != value:
                    skip_iteration = True
                    continue
            if skip_iteration:
                continue
            yield plugin

    abstract = staticmethod(abstract)
    field = staticmethod(field)

    def register(self, plugin_cls, check: bool = None):
        """
        Register the plugin and check if it's correctly implemented

        Args:
            plugin_cls: plugin to register
            check: if True check if plugin respect all constraints (default taken from self.autocheck)
        """
        if self.baseplugin is None:
            raise TypeError(
                "Can't register plugin without baseplugin. use mkbaseplugin before"
            )

        if check is None:
            check = self.autocheck

        name = getattr(plugin_cls, "name", None)
        # TODO: check if name already exists

        # If not abstract register
        if not is_cls_abstract(plugin_cls):
            # Create metadata attribute if not present and required
            #  If required and not present, error is thrown before ith MetadataIsPresentConstraint
            if not self._metadata_have_at_least_one_required_field and not hasattr(
                plugin_cls, "metadata"
            ):
                plugin_cls.metadata = self.baseplugin.Metadata()

            # Check constraint before registring
            if check:
                self.check(plugin_cls)

            self.plugins.add(plugin_cls, name=name)
        else:
            # If it's an abstract class (with abstract = True)
            #   add all the contraints to the __koalak__.constraints dict and remove the field attributes
            self._add_constraints_to_cls(plugin_cls)
            self.abstract_plugins.add(plugin_cls, name=name)

    def check(self, plugin):
        """Check if plugin respect all constraints"""
        for contraint in self.iter_constraints(plugin):
            contraint.check(plugin)

    def mkbaseplugin(self, baseplugin):
        """
        - Create empty Metadata cls if not created
        """
        # TODO: add checks that mkbaseplugin is not already set

        self.baseplugin = baseplugin

        # reference plugin manager in the baseplugin
        koalak_object_storage.set(baseplugin, KEY_PLUGIN_MANAGER, self)

        # inject __init_subclass__ to be able to autoregister plugins when subclassing
        baseplugin.__init_subclass__ = classmethod(init_subclass_for_baseplugin)

        # add all the contraints to the __koalak__.constraints dict and remove the field attributes
        self._add_constraints_to_cls(baseplugin)

        # add metadata constraints
        self._add_metadata_constraints(baseplugin)

        # All custom plugins (loaded from home) have _is_home_plugin to True
        # TODO: move _is_home_plugin to __koalak__ attribute
        self.baseplugin._is_home_plugin = False
        return baseplugin

    def metadata(self, **kwargs):
        """Creates metadata for a Plugin"""
        return self.baseplugin.Metadata(**kwargs)

    def init(self, _homepath_initialized: set = None):
        # TODO: read me again
        _homepath_initialized = _homepath_initialized or set()
        if self.homepath is None:
            raise TypeError("You can not init a plugin mananger without homepath")

        if self._initialized:
            raise TypeError("Plugin Already initiated")
        self._initialized = True

        if self.homepath in _homepath_initialized:
            return
        self._init_home()
        self._load_plugins()

    def get_home_plugins(self):
        """Get plugins loaded from home/plugins"""
        for e in self:
            if e._is_home_plugin:
                yield e

    def iter_constraints(self, plugin):
        """Return iterators of all constraints related to a plugin
        attributes, metadata, abstract methods)"""
        yield from koalak_object_storage.getasdict(
            plugin, KEY_ATTRIBUTES_CONSTRAINTS
        ).values()

        yield from self._other_constraints
        yield from self._metadata_attributes_constraints.values()

    def instances(self, *args, **kwargs):
        """Return instances of each plugin after instantiations with args/kwargs"""
        for plugin_cls in self:
            yield plugin_cls(*args, **kwargs)

    def run(self):
        pass

    # ================ #
    # PRIVATES METHODS #
    # ================ #
    def _init_home(self):
        # TODO: read me again
        if not self.homepath:
            return
        if not os.path.exists(self.homepath):
            os.makedirs(self.homepath)
        elif os.path.isfile(self.homepath):
            raise NotADirectoryError("Home path is not a directory")
        # else it's a directory already created

    def _load_plugins(self):
        # TODO: read me again
        """Load home plugins"""
        for python_path in glob.glob(os.path.join(self.homepath, "*.py")):
            with open(python_path) as f:
                data = f.read()
                execution_context = {}
                exec(data, execution_context)
                for object_name, object in execution_context.items():
                    if inspect.isclass(object) and issubclass(object, self.baseplugin):
                        if object is self.baseplugin:
                            continue
                        object._is_home_plugin = True

    def _add_metadata_constraints(self, baseplugin):
        """Add metadata constraints based on 'Metadata' config class (if not create Metadata)"""
        Metadata = getattr(baseplugin, "Metadata", None)

        # if baseplugin don't have metadata do nothing
        if Metadata is None:
            # Create class is not existing
            Metadata = type("Metadata", (object,), {})
            setattr(baseplugin, "Metadata", Metadata)

        # If Metadata is not a class do nothing
        if not inspect.isclass(Metadata):
            raise TypeError("Metadata must be a class")

        # Add constraint for each attribute in metadata
        # ---------------------------------------------
        generic_fields = self._get_and_update_generic_fields(Metadata)
        self._metadata_have_at_least_one_required_field = any(
            generic_field.required for generic_field in generic_fields.values()
        )

        # Add constraint that metadata must be present
        if self._metadata_have_at_least_one_required_field:
            self._other_constraints.append(MetadataAttributeIsPresent())

        # Always check metadata type
        self._other_constraints.append(MetadataAttributeTypeConstraint())

        self._metadata_attributes_constraints = {
            generic_field_name: MetadataAttributeConstraint(generic_field)
            for generic_field_name, generic_field in generic_fields.items()
        }

        setattr(
            baseplugin,
            "Metadata",
            GenericField.build_attrs_dataclass_from_cls(Metadata),
        )

    def _add_constraints_to_cls(self, cls):
        """Transform GenericField() attribute to constraints and removing them from cls
        Used for baseplugin or for abstract plugins

        Add attributes constraints
        Add abstract methods constraints"""

        # Add attribute field constraints #
        # ------------------------------- #
        generic_fields = self._get_and_update_generic_fields(cls)
        for field_name, generic_field in generic_fields.items():
            # Add the constraint check
            constraint = AttributeConstraint(generic_field)

            # Add constraint to the cls
            koalak_object_storage.setindict(
                cls, KEY_ATTRIBUTES_CONSTRAINTS, field_name, constraint
            )

            # Delete attribute
            delattr(cls, field_name)

        # Add 'abstract' methods constraints #
        # ---------------------------------- #
        for attribute_name, attribute in list(cls.__dict__.items()):
            if is_abstract(attribute):
                constraint = AbstractMethodConstraint(attribute_name)

                # Add constraint to the cls
                koalak_object_storage.setindict(
                    cls, KEY_ATTRIBUTES_CONSTRAINTS, attribute_name, constraint
                )

    def _get_and_update_generic_fields(self, cls) -> Dict[str, GenericField]:
        """Return dict of GenericField from cls and update type/annotation of a generic field"""
        generic_fields = {}

        for attribute_name, attribute in list(cls.__dict__.items()):
            if isinstance(attribute, GenericField):
                # set name on the field
                generic_field = attribute
                generic_field.name = attribute_name

                # set annotation on the field
                if generic_field.annotation is None:
                    annotations_dict = getattr(cls, "__annotations__", {})
                    annotation = annotations_dict.get(attribute_name)
                    generic_field.annotation = annotation

                # If annotation is present and not type add default type
                if generic_field.type is None:
                    generic_field.type = generic_field.annotation

                generic_fields[attribute_name] = generic_field

        return generic_fields

    # Utils functions
    def print_table(self):
        metadata_fields = [
            e.field for e in self._metadata_attributes_constraints.values()
        ]
        column_names = [e.name for e in metadata_fields]

        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(title=self.name)
        table.add_column("name")
        for column_name in column_names:
            table.add_column(column_name)

        for plugin in self:
            row = [plugin.name or ""]
            for field_name in column_names:
                cell = getattr(plugin.metadata, field_name)
                if cell is None:
                    cell = ""
                elif isinstance(cell, list):
                    cell = ", ".join(cell)
                else:
                    cell = str(cell)
                row.append(cell)
            table.add_row(*row)
        console.print(table)


mkpluginmanager = PluginManager
