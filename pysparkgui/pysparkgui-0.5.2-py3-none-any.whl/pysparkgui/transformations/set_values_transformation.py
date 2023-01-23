# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import Transformation, string_to_code, notification, VSpace
from pysparkgui.plugins import Singleselect, Text
from pysparkgui.transformations.base_components import (
    ValueSelector,
    SingleColumnSelector,
    SelectorGroupMixin,
    SelectorMixin,
)
from pysparkgui.transformations.spark_filter_transformer import ConditionSection

PREFIX_WIDTH = {"width": "30px"}

# Potential improvement: The column name selector could be a free text field with autocompletion for existing column names
#                        This way, we can remove the explicit choice between new or existing column and this will then be implicit based on what the user enters

class SingleCase(SelectorMixin, widgets.VBox):
    def __init__(self, df, **kwargs):
        super().__init__(**kwargs)
        self.df = df

        self.condition_section = ConditionSection(
            self.selector_group.transformation, self.df, focus_after_init=False
        )

        self.value_selector = ValueSelector(
            self, columns=self.df.columns
        )

        self.children = [
            widgets.HBox([widgets.HTML("To", layout=PREFIX_WIDTH), self.value_selector, self.delete_selector_button]),
            widgets.HBox([widgets.HTML("If", layout=PREFIX_WIDTH), self.condition_section,]),
            VSpace("2xl"),
        ]
    
    def is_valid_case(self):
        assert(self.condition_section.is_valid_condition())
        assert(self.value_selector.is_valid_value())
        return True
    
    def new_value_description(self):
        return self.value_selector.get_value_description()

    def new_value_code(self):
        return self.value_selector.get_value_code()

    def filter_expression_description(self):
        return self.condition_section.get_description()
    
    def filter_expression_code(self):
        return self.condition_section.get_code()

class MultipleCasesSection(SelectorGroupMixin, widgets.VBox):
    def __init__(self, transformation, df):
        super().__init__()
        self.df = df
        self.transformation = transformation

        self.init_selector_group("add case")

        self.children = [self.selector_group, self.add_selector_button]

    def create_selector(self, show_delete_button=None, **kwargs):
        return SingleCase(
            df=self.df,
            selector_group=self,
            show_delete_button=show_delete_button,
        )

    def get_cases(self):
        return [case for case in self.get_selectors()]


COLUMN_TYPE_NEW = "new"
COLUMN_TYPE_EXISTING = "existing"

class SparkSetValuesTransformation(Transformation):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.column = None
        self.df = self.get_df()

        self.column_type = Singleselect(
                options=[
                    ("New column", COLUMN_TYPE_NEW),
                    ("Existing column", COLUMN_TYPE_EXISTING),
                ],
                set_soft_value=True,
                width="sm",
                on_change=lambda _: self._update_column_selector(),
            )
        self.column_outlet = widgets.VBox()
        self._update_column_selector()

        self.multiple_cases_section = MultipleCasesSection(self, self.df)

        self.otherwise_value = ValueSelector(
            self, columns=self.df.columns
        )

        self.add_otherwise_checkbox = widgets.Checkbox(
            value=False, description="and otherwise"
        ).add_class("pysparkgui-checkbox")
        self.add_otherwise_checkbox.observe(
            lambda value: self._update_otherwise_section(), names="value"
        )
        self.otherwise_section = widgets.VBox([])

    def _update_column_selector(self):
        if self.column_type.value == COLUMN_TYPE_NEW:
            self.column = Text(
                value="",
                placeholder="New column name",
                width="long-column-name",
                execute=self,
            ).add_class("pysparkgui-element-next-to-selectize")
        else:  # existing column
            self.column = SingleColumnSelector(
                options=self.df.columns,
                set_soft_value=False,
                width="long-column-name",
            )
        self.column_outlet.children = [self.column]

    def render(self):
        self.set_title(f"Set column values based on condition")
        self.set_content(
            widgets.HTML("Set value of"),
            widgets.HBox([self.column_type, self.column_outlet]),
            VSpace("2xl"),
            self.multiple_cases_section,
            VSpace("2xl"),
            self.add_otherwise_checkbox,
            self.otherwise_section,
        )

    def _update_otherwise_section(self):
        if self.add_otherwise_checkbox.value:
            self.otherwise_section.children = [
                widgets.HBox([widgets.HTML("To", layout=PREFIX_WIDTH), self.otherwise_value]),
            ]
        else:
            self.otherwise_section.children = []

    def is_valid_transformation(self):
        for case in self.multiple_cases_section.get_cases():
            assert(case.is_valid_case())

        if self.add_otherwise_checkbox.value:
            assert(self.otherwise_value.is_valid_value())
        return True

    def get_description(self):
        description = f"<b>Set values</b> of <i>{self.column.value}</i>"

        for case in self.multiple_cases_section.get_cases():
            description += f" to <i>{case.new_value_description()}</i> where <i>{case.filter_expression_description()}</i>"

        if self.add_otherwise_checkbox.value:
            description += f" and otherwise to <i>{self.otherwise_value.get_value_description()}</i>"

        return description

    def get_pyspark_chain_code(self):
        column_code = string_to_code(self.column.value)
        
        cases_code = "f"
        for case in self.multiple_cases_section.get_cases():
            cases_code += f".when({case.filter_expression_code()}, {case.new_value_code()})"

        otherwise_code = ""
        if self.add_otherwise_checkbox.value:
            otherwise_code = f".otherwise({self.otherwise_value.get_value_code()})"
        if (not self.add_otherwise_checkbox.value) and (self.column_type.value == COLUMN_TYPE_EXISTING):
            otherwise_code = f".otherwise(f.col({column_code}))"
        return f".withColumn({column_code}, {cases_code}{otherwise_code})"

    def can_be_edited_without_schema_change(self):
        # The ability to add a new column allows this transformation to potentially perform a schema change
        return False

    def get_exception_message(self, exception):
        if "THEN and ELSE expressions should all be same type or coercible to a common type" in str(exception):
            if (not self.add_otherwise_checkbox.value) and (len(self.multiple_cases_section.get_cases()) == 1):
                # This error occurs when the user inadvertently tried to implicitly change the data type of a column
                # E.g. update a string column to sometimes have a boolean value but they did not specify what to do otherwise
                # Thus, per default, the otherwise value is the old column value but this leads to a data type mismatch
                return notification(
                    f"""Please add an 'otherwise' value for the case when the condition is not true""",
                    type="error",
                )
            else:
                return notification(
                    f"""
                    The new values that you try to set all need to have the same data type e.g. all numeric, or all text.<br>
                    <br>
                    Currently, it seems like you tried to set values with different data types.<br>
                    <br>
                    Please adjust the values so that they all have the same data type or are set to missing value.
                    """,
                    type="error",
                )
        return None

