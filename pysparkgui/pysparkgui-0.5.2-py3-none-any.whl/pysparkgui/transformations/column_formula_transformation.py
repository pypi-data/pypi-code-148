# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import (
    Transformation,
    notification,
    DF_OLD,
    VSpace,
    PysparkguiError,
    string_to_code,
    replace_column_names_in_formula,
)

from pysparkgui.widgets import Text, BamAutocompleteTextV1


class SparkColumnFormulaTransformation(Transformation):
    """Create a new column from a formula e.g. math expression."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.new_column_input = Text(
            focus_after_init=True,
            description="New column name",
            width="long-column-name",
            execute=self,
            css_classes=["pysparkgui-new-column-name"],
        )

        self.column_names = self.get_df().columns
        self.parsed_formula = ""

        self.formula_input = BamAutocompleteTextV1(column_names=self.column_names)
        self.formula_input.on_submit(lambda _: self.execute())

    # We overwrite the execute method so that formula is parsed before the actual execution.
    def execute(self):
        self._parse_formula()
        super().execute()

    def render(self):
        self.set_title("Create new column from formula")
        self.set_content(
            self.new_column_input,
            VSpace("sm"),
            widgets.HTML("Column formula"),
            self.formula_input,
            VSpace("lg"),
            notification(
                """
    <p>Formulas can contain math, logic expressions, or text</p>
    <p>Examples:</p>
    <ul>
        <li><code>(column1 + column2) / (column3 * 2)</code></li>
        <li><code>(column1 > 10) or (column2 <= 50)</code></li>
        <li><code>(column1 and column2) or (not column3)</code></li>
        <li><code>constant text value for my new column</code></li>
    </ul>
"""
            ),
        )

    def _parse_formula(self, *args):
        """Parse the formula and replace all column names."""
        contains_any_column_name = any([column in self.formula_input.value for column in self.column_names])
        if contains_any_column_name:
            self.parsed_formula = replace_column_names_in_formula(
                self.formula_input.value, self.column_names
            ).replace("and", "&").replace("or", "|").replace("not", "~")
        else:
            # Assumption: the user wants to fill the column with a constant text value
            self.parsed_formula = f"f.lit({string_to_code(self.formula_input.value)})"

    def get_description(self):
        return f"<b>Create new column</b> <i>{self.new_column_input.value}</i> from formula <i>{self.formula_input.value}</i>"

    def is_valid_transformation(self):
        if self.new_column_input.value == "":
            raise PysparkguiError(
                "The name for the new column is empty.<br>Please enter a 'New column name'"
            )
        if self.parsed_formula == "":
            raise PysparkguiError(
                "The formula is empty.<br>Please enter a 'Column formula'"
            )
        return True

    def get_pyspark_chain_code(self):
        return f".withColumn({string_to_code(self.new_column_input.value)}, {self.parsed_formula})"
