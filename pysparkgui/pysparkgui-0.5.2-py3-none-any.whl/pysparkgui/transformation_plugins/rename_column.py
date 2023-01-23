# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import string_to_code
from pysparkgui.plugins import TransformationPlugin, Text

from pysparkgui.transformations.base_components import (
    SelectorGroupMixin,
    SelectorMixin,
    SingleColumnSelector,
)


class RenameEntry(SelectorMixin, widgets.HBox):
    """Manages a (<old_column_name>, <new_column_name>) pair."""

    def __init__(self, column_options, **kwargs):
        super().__init__(**kwargs)

        self.column_dropdown = SingleColumnSelector(
            options=column_options,
            set_soft_value=True,
            focus_after_init=True,
            width="sm",
        )

        self.new_name = Text(
            value=self.column_dropdown.value, execute=self.selector_group.transformation
        )

        def adjust_new_name(dropdown):
            self.new_name.value = dropdown.value

        self.column_dropdown.on_change(adjust_new_name)

        self.children = [
            self.column_dropdown,
            widgets.HTML("&nbsp;to&nbsp;"),
            self.new_name,
            self.delete_selector_button,
        ]

    def test_set_rename(self, old_column_name, new_column_name):
        self.column_dropdown.value = old_column_name
        self.new_name.value = new_column_name


class RenameSection(SelectorGroupMixin, widgets.VBox):
    """Manages a group of `RenameEntry`s."""

    def __init__(self, transformation, df):
        super().__init__()
        self.df = df
        self.transformation = transformation

        self.init_selector_group("add column")

        self.children = [self.selector_group, self.add_selector_button]

    def create_selector(self, show_delete_button=None, **kwargs):
        return RenameEntry(
            list(self.df.columns),
            selector_group=self,
            show_delete_button=show_delete_button,
        )

    def get_rename_dict(self):
        return {
            selector.column_dropdown.value: selector.new_name.value
            for selector in self.get_selectors()
        }


class SparkRenameMultipleColumnsTransformation(TransformationPlugin):

    name = "Rename columns"
    description = "Rename one or more columns"

    def __init__(self, *args, column=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.rename_section = RenameSection(self, self.get_df())

    def render(self):
        self.set_title("Rename column(s)")
        self.set_content(self.rename_section, self.rename_df_group)

    def get_description(self):
        rename_dict = self.rename_section.get_rename_dict()
        return (
            "<b>Rename column</b>"
            if len(rename_dict) <= 1
            else "<b>Rename multiple columns</b>"
        )

    def get_pyspark_chain_code(self):
        rename_dict = self.rename_section.get_rename_dict()
        statements = ""
        for old_name in rename_dict.keys():
            new_name = rename_dict[old_name]
            statements += f".withColumnRenamed({string_to_code(old_name)}, {string_to_code(new_name)})"
        return statements

    # def test_set_rename(self, old_column_name, new_column_name):
    #     self.rename_section.get_selectors()[-1].test_set_rename(
    #         old_column_name, new_column_name
    #     )
