# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import Transformation, DF_OLD, DF_NEW, string_to_code

from pysparkgui.widgets.selectize import Singleselect, Multiselect
# from pysparkgui.transformations.columns_selector import ColumnsSelector

KEEP = "keep"
DELETE = "delete"


class SparkSelectColumns(Transformation):
    """Select/delete one or multiple columns."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.select_type = Singleselect(
            options=[("Select", KEEP), ("Delete", DELETE)],
            set_soft_value=True,
            focus_after_init=True,
            width="sm",
        )
        
        self.columns = Multiselect(
            options=self.get_df().columns,
            placeholder="Choose column(s)",
            width="long-column-name",
        )
        # self.columns = ColumnsSelector(
        #     transformation=self, show_all_columns=False, width="long-column-name"
        # )

    def render(self):
        self.set_title("Select or delete columns")
        self.set_content(self.select_type, self.columns, self.rename_df_group)

    def get_description(self):
        type_ = self.select_type.value
        if type_ == KEEP:
            return f"<b>Select columns</b> {self.columns.value}"
        else:
            return f"<b>Delete columns</b> {self.columns.value}"

    def get_pyspark_chain_code(self):
        type_ = self.select_type.value
        if type_ == KEEP:
            # .select accepts a list
            code = f".select({self.columns.value})"
        else:
            # .drop does not accept a list and thus we need multiple, chained calls of drop
            code = ""
            for column in self.columns.value:
                code += f".drop({string_to_code(column)})"
        return code

    # def reset_preview_columns_selection(self):
    #     # reset when selecting new columns but keep selection when just dropping columns
    #     type_ = self.select_type.value
    #     return type_ == KEEP

    # def get_metainfos(self):
    #     return {
    #         "select_columns_count": len(self.columns.value),
    #         "select_columns_type": self.select_type.value,
    #     }

    # def test_select_columns(self, columns):
    #     self.select_type.value = KEEP
    #     self.columns.value = columns

    # def test_drop_columns(self, columns):
    #     self.select_type.value = DELETE
    #     self.columns.value = columns
