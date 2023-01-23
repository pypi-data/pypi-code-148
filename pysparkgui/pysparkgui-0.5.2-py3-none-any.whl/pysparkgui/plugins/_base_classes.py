# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

from pysparkgui.helper import Transformation, Loader, TabViewable
from pysparkgui.plugins import create_plugin_base_class


@create_plugin_base_class
class TransformationPlugin(Transformation):
    """
    Base class for TransformationPlugins. It is used to add custom transformations to pysparkgui.

    Since this is a huge topic, please refer to the documentation at:
    https://github.com/tkrabel/pysparkgui/tree/master/plugins

    You can find examples of TransformationPlugins here:
    https://github.com/tkrabel/pysparkgui/tree/master/plugins/examples/transformations

    """

    name = None  # if user provides no value, it will be set to class.__name__
    description = ""  # can be overridden by user

    def render(self, *args, **kwargs):
        self.set_title(self.name)
        self.set_content()

    def get_description(self, *args, **kwargs):
        return f"<b>{self.name}</b>"


@create_plugin_base_class
class LoaderPlugin(Loader):
    """
    Base class for LoaderPlugins. It is used to add custom loaders to pysparkgui.

    Since this is a huge topic, please refer to the documentation at:
    https://github.com/tkrabel/pysparkgui/tree/master/plugins

    You can find examples of LoaderPlugins here:
    https://github.com/tkrabel/pysparkgui/tree/master/plugins/examples/loaders

    """

    name = None  # if user provides no value, it will be set to class.__name__
    description = ""  # can be overridden by user

    def render(self, *args, **kwargs):
        self.set_title(self.name)
        self.set_content(self.new_df_name_group, self.spacer, self.execute_button)


@create_plugin_base_class
class ViewPlugin(TabViewable):
    """
    Base class for ViewPlugins. It is used to add custom views to pysparkgui.

    Since this is a huge topic, please refer to the documentation at:
    https://github.com/tkrabel/pysparkgui/tree/master/plugins

    You can find examples of ViewPlugins here:
    https://github.com/tkrabel/pysparkgui/tree/master/plugins/examples/views

    """

    name = None  # if user provides no value, it will be set to class.__name__
    description = ""  # can be overridden by user

    def render(self, *args, **kwargs):
        self.set_title(self.name)
        self.set_content()
