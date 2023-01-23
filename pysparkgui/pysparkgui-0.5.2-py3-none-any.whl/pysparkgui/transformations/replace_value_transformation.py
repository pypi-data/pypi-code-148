# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import pandas as pd
import numpy as np
import ipywidgets as widgets

from pysparkgui.helper import Transformation, notification, DF_OLD, string_to_code

from pysparkgui.transformations.base_components import (
    ValueSelector,
    SingleColumnSelector,
)

REPLACE_IN_ALL_COLUMNS_STRING = "BAMBOO_REPLACE_IN_ALL_COLUMNS"


class SparkReplaceValueTransformation(Transformation):
    """Substitute *exact* cell values in one or all columns."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df = self.get_df()
        self.column = None
        all_columns_option = [("[All columns]", REPLACE_IN_ALL_COLUMNS_STRING)]
        column_names = [(column, column) for column in self.df.columns]

        self.column_dropdown = SingleColumnSelector(
            placeholder="Choose column(s)",
            value=self.column,
            options=all_columns_option + column_names,
            set_soft_value=True,
            focus_after_init=True,
            width="long-column-name",
            on_change=self._on_column_change,
        )

        self.find_value_box = widgets.VBox()
        self.replace_value_box = widgets.VBox()

        self._on_column_change()

    def _update_value_selectors(self):
        # # Not needed right now because there is no value autocomplete for valid column values
        # if self.column_dropdown.value == REPLACE_IN_ALL_COLUMNS_STRING:
        #     self.find_value = ValueSelector(self)
        #     self.replace_value = ValueSelector(self)
        # else:
        #     # series = self.df[self.column]
        #     self.find_value = ValueSelector(self, series=None)
        #     self.replace_value = ValueSelector(self, series=None)
        self.find_value = ValueSelector(self)
        self.replace_value = ValueSelector(self)

        self.find_value_box.children = [self.find_value]
        self.replace_value_box.children = [self.replace_value]

    def render(self):
        self.set_title("Find and Replace exact values")
        self.outlet.set_content(
            widgets.VBox(
                [
                    widgets.HTML("In"),
                    self.column_dropdown,
                    widgets.HTML("Find the exact value"),
                    self.find_value_box,
                    widgets.HTML("And replace with"),
                    self.replace_value_box,
                    widgets.HTML("<br>"),
                    self.execute_button,
                    widgets.HTML("<br>"),
                    notification(
                        """<b>Cannot do what you want?</b><br>
                                <ul>
                                    <li>If you want to <b>replace partial text e.g. words</b>, please use 'Text transformations'.</li>
                                    <li>If you want to <b>replace values based on a True/False logic condition</b>, please use 'Conditional find and replace value ('if else logic')'.</li>
                                </ul>"""
                    ),
                ]
            )
        )

    def _replacing_in_all_columns(self):
        return self.column == REPLACE_IN_ALL_COLUMNS_STRING

    def _on_column_change(self, *args, **kwargs):
        self.column = self.column_dropdown.value
        self._update_value_selectors()

    def get_column_description(self):
        if self._replacing_in_all_columns():
            return "all columns"
        else:
            return f"<i>{self.column}</i>"

    def get_description(self):
        find_value = self.find_value.get_value_description()
        replace_value = self.replace_value.get_value_description()
        return f"<b>Replace</b> {find_value} with {replace_value} in {self.get_column_description()}"

    def get_pyspark_chain_code(self):
        find_value = self.find_value.get_value_code()
        replace_value = self.replace_value.get_value_code()
        subset = None if self._replacing_in_all_columns() else [self.column]

        return f".replace({find_value}, value={replace_value}, subset={subset})"

    def can_be_edited_without_schema_change(self):
        return True

    def is_valid_transformation(self):
        return self.find_value.is_valid_value() and self.replace_value.is_valid_value()

    def get_exception_message(self, exception):
        if "Mixed type replacements are not supported" in str(exception):
            return notification(
                f"""
                The value that you try to find and the value that you want to replace need to have the same data type e.g. both numeric, or both text.<br>
                Currently, you tried to replace with a different data type.<br>
                You can either change your logic or change the data type of your column(s).
                """,
                type="error",
            )
        return None
