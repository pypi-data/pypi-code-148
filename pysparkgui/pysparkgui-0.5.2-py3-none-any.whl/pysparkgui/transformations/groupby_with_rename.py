# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import (
    Transformation,
    list_to_string,
    DF_OLD,
    DF_NEW,
    PysparkguiError,
    string_to_code,
    notification,
    VSpace,
)

from pysparkgui.widgets import Multiselect, Singleselect, Text

from pysparkgui.transformations.base_components import (
    SelectorGroupMixin,
    SelectorMixin,
    SingleColumnSelector,
)


COUNT_MISSING_VALUES = "countMissingValues"
COUNT_ALL_VALUES = "countAllValues"
COUNT_DISTICT_VALUES = "countDistinct"


AGGREGATION_OPTIONS = [
    ("Count valid values", "count"),
    ("Count missing values", COUNT_MISSING_VALUES),
    ("Count all values", COUNT_ALL_VALUES),
    ("Count distinct values", COUNT_DISTICT_VALUES),
    ("Sum", "sum"),
    ("Mean / Average", "mean"),
    ("Min", "min"),
    ("Max", "max"),
    ("Variance", "variance"),
    ("Standard deviation", "stddev"),
    ("First value", "first"),
    ("Last value", "last"),
    # TBD: median and other percentile values
    # https://stackoverflow.com/questions/46845672/median-quantiles-within-pyspark-groupby
    
    # TBD: count missing values
    # https://sparkbyexamples.com/pyspark/pyspark-find-count-of-null-none-nan-values/

    # ("Count (size)", "size"),  # with missing values
    # ("Count (excl. missings)", "count"),
    # ("Median", "median"),
    # distribution metrics
    # ("Standard error of the mean - sem", "sem"),
    # ("Mean absolute deviation - mad", "mad"),
    # ("Skew", "skew"),
]

class AggregationSelector(SelectorMixin, widgets.HBox):
    """
    Manages one (<column to aggregate>, <aggregation function>, <new column name>) group plus the
    delete button to remove itself.
    """

    def __init__(self, df_columns, show_delete_button=True, **kwargs):
        super().__init__(show_delete_button=show_delete_button, **kwargs)

        self.aggregation_dropdown = Singleselect(
            options=AGGREGATION_OPTIONS,
            focus_after_init=show_delete_button,
            placeholder="Choose aggregation",
            set_soft_value=True,
            width="lg",
        )

        self.column_dropdown = SingleColumnSelector(options=df_columns, width="long-column-name")

        self.new_column_name = Text(
            placeholder="New column name (optional)",
            execute=self.selector_group,
            width="long-column-name",
        )

        PREFIX_WIDTH = {"width": "20px"}

        self.children = [
            widgets.VBox(
                [
                    self.aggregation_dropdown,
                    widgets.HBox([widgets.HTML("of", layout=PREFIX_WIDTH), self.column_dropdown]),
                    widgets.HBox([widgets.HTML("as", layout=PREFIX_WIDTH), self.new_column_name]),
                    VSpace("xl"),
                ]
            ),
            self.delete_selector_button,
        ]

    def has_valid_value(self):
        column_is_missing = not self.column_dropdown.value
        if column_is_missing:
            raise PysparkguiError(
                """In one of the calculations, you didn't specify a <b>column</b> that you want to aggregate.
                Please select a column to aggregate."""
            )
        # Attention: The following can never be reached as long as self.aggregation_dropdown has set_soft_value=True
        # aggregation_function_is_missing = not self.aggregation_dropdown.value
        # if aggregation_function_is_missing:
        #     raise PysparkguiError(
        #         """In of the calculations, you didn't specify an <b>aggregation function</b> (e.g. sum or mean)
        #         for your column."""
        #     )
        return True

    def get_aggregation_code(self):
        # e.g. f.sum("n").alias("n_sum")
        aggregation = self.aggregation_dropdown.value
        column = self.column_dropdown.value

        if aggregation == COUNT_MISSING_VALUES:
            code = f"f.count(f.when(f.col({string_to_code(column)}).isNull(), True))"
        elif aggregation == COUNT_ALL_VALUES:
            # This is quite convoluted if there is a more succinct way to express it that still works in this context, feel free to add it
            code = f"f.count(f.when(f.col({string_to_code(column)}).isNull(), True).otherwise(True))"
        else:
            code = f"f.{aggregation}({string_to_code(column)})"
        
        new_column_name = self.new_column_name.value
        if new_column_name:
            code += f".alias({string_to_code(new_column_name)})"
        elif aggregation == COUNT_DISTICT_VALUES:
            # Context: countDistinct does per default result in count(column_name) as new column name
            # This collides with the normal count and thus we explicitly correct the new column name for
            # countDistinct to countDistinct(column_name) via an alias unless the user already specified a different name
            adjusted_default_column_name = f"countDistinct({column})"
            code += f".alias({string_to_code(adjusted_default_column_name)})"
        return code

    # def test_select_aggregation_functions(
    #     self, aggregation_function: str, column_name: str, new_column_name: str
    # ):
    #     self.aggregation_dropdown.value = aggregation_function
    #     self.column_dropdown.value = column_name
    #     self.new_column_name.value = new_column_name


class AggregationSection(SelectorGroupMixin, widgets.VBox):
    """Manages a group of `AggregationSelector`s."""

    def __init__(self, transformation):
        super().__init__()
        self.transformation = transformation
        self.df_columns = list(self.transformation.get_df().columns)

        self.init_selector_group("add calculation")

        self.children = [
            widgets.HTML("Calculate"),
            self.selector_group,
            self.add_selector_button,
        ]

    def create_selector(self, show_delete_button=None, **kwargs):
        return AggregationSelector(
            self.df_columns, selector_group=self, show_delete_button=show_delete_button
        )

    def get_aggregation_code(self):
        return ", ".join([selector.get_aggregation_code() for selector in self.get_selectors() if selector.has_valid_value()])

    def execute(self):
        self.transformation.execute()

    # def test_select_aggregation_functions(
    #     self, aggregation_function: str, column_name: str, new_column_name: str
    # ):
    #     self.get_selectors()[-1].test_select_aggregation_functions(
    #         aggregation_function, column_name, new_column_name
    #     )


class SparkGroupbyWithRename(Transformation):
    """
    Group rows by columns and calculate a SINGLE aggregation that can be named.

    Manages the whole transformation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.groupby_columns = Multiselect(
            options=list(self.get_df().columns),
            placeholder="Choose column(s) - optional",
            focus_after_init=False,
            width="long-column-name",
        )

        self.aggregation_section = AggregationSection(self)

        self.merge_result = Singleselect(
            placeholder="Choose style",
            options=[("New Table", False), ("New Columns", True)],
            set_soft_value=True,
            width="md",
        )

    def render(self):
        self.set_title("Calculate column summaries (aggregations)")
        self.set_content(
            widgets.VBox(
                [
                    self.aggregation_section,
                    VSpace("xl"),
                    widgets.HTML("Group By"),
                    self.groupby_columns,
                    VSpace("xl"),
                    widgets.HTML("Store result as"),
                    self.merge_result,
                    self.rename_df_group,
                ]
            )
        )

    def get_description(self):
        columns_list = list_to_string(self.groupby_columns.value, quoted=False)
        description = (
            f"<b>Group by</b> {columns_list} <b>and calculate new column(s)</b>"
        )

        if self.merge_result.value:
            description = f"<b>Add new column(s)</b> based on {description}"
        return description

    def get_exception_message(self, exception):
        # That error is not thrown as part of the transformation but afterwards
        # if ("Reference" in str(exception)) and ("is ambiguous, could be:" in str(exception)):
        #     # count and countDistinct get assigned the same name when the user does not specify a name
        #     # this will lead to an error in pyspark
        #     # In addition, this error is triggered when the user assigns the same names
        #     return notification(
        #         f"""
        #         There has been an error because the names for the new columns are not unique. E.g. multiple calculations got assigned the same name for the new column.<br>
        #         <br>
        #         Please manually assign new column names and make sure that they are all unique.<br>
        #         <br>
        #         In case that you use <i>{COUNT_DISTICT_VALUES_LABEL}</i> and <i>{COUNT_VALID_VALUES_LABEL}</i> please give at least one a new name.
        #         """,
        #         type="error",
        #     )
        return None

    def is_valid_transformation(self):
        if (len(self.groupby_columns.value) == 0) and self.merge_result.value:
            raise PysparkguiError(
                """
                This combination is not supported yet.<br>
                You need to either add a groupby column or store the result as a new table.<br>
                If you want support for calculating new aggregated columns without groupby, please reach out.
                """
            )
        return True

    def get_code(self):
        aggregations_code = self.aggregation_section.get_aggregation_code()
        groupby_columns = self.groupby_columns.value

        potential_groupby_code = f".groupby({groupby_columns})" if len(groupby_columns) >= 1 else ""
        df_expression = f"{DF_OLD}{potential_groupby_code}.agg({aggregations_code})"

        if self.merge_result.value and (len(groupby_columns) >= 1):
            return f"""{DF_NEW} = {DF_OLD}.join({df_expression}, on={groupby_columns}, how='left')"""
        else:
            return f"""{DF_NEW} = {df_expression}"""

    def get_pyspark_chain_code(self):
        if self.merge_result.value:
            return None  # this statement cannot be expressed in chain style as far as Flo knows as of 2022-10-20
        else:
            groupby_columns = self.groupby_columns.value
            potential_groupby_code = f".groupby({groupby_columns})" if len(groupby_columns) >= 1 else ""
            return f"{potential_groupby_code}.agg({self.aggregation_section.get_aggregation_code()})"

    # def get_metainfos(self):
    #     return {
    #         "groupby_type": self.merge_result.label,
    #         "groupby_columns_count": len(self.groupby_columns.value),
    #     }

    # def reset_preview_columns_selection(self):
    #     if self.merge_result.value:
    #         return False
    #     else:  # create new table
    #         return True

    # def test_select_groupby_columns(self, groupby_columns: list):
    #     self.groupby_columns.value = groupby_columns
    #     return self  # allows method chaining

    # def test_select_aggregation(
    #     self,
    #     aggregation_function: str = "",
    #     column_name: str = "",
    #     new_column_name: str = "",
    # ):
    #     self.aggregation_section.test_select_aggregation_functions(
    #         aggregation_function, column_name, new_column_name
    #     )

    # def test_select_merge_result(self, merge_result: bool):
    #     self.merge_result.value = merge_result
