# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import re
import pandas as pd
import ipywidgets as widgets

from pysparkgui.helper import (
    DF_OLD,
    DF_NEW,
    replace_code_placeholder,
    log_action,
    guess_dataframe_name,
)
from pysparkgui.widgets import Button
from pysparkgui.config import get_option


LAST_LIST_ITEM = -1


def updates_live_code_export(function):
    """Decorator that updates the live code export."""

    def function_that_updates_live_code_export(self, *args, **kwargs):
        result = function(self, *args, **kwargs)
        self.maybe_update_live_code_export_and_user_symbols()
        return result

    return function_that_updates_live_code_export


def remove_html_tags(raw_html):
    """Remove HTML tags of a string."""
    # https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


class SparkDfManager:
    def __init__(
        self,
        df,
        symbols={},
        setup_code=None,
        df_name=None,
        initial_user_code=None,
        command_guid=None,
    ):
        super().__init__()
        self._command_guid = "" if command_guid is None else command_guid
        self.code_formatter = CodeFormatter(self, setup_code, initial_user_code)

        if len(symbols) == 0:
            from pysparkgui.setup.user_symbols import get_user_symbols

            symbols = get_user_symbols()

        self.show_live_code_export = get_option("global.show_live_code_export")
        self.wrangler = None
        self.tab_section = None

        self.df = df
        self._original_df = df
        self.original_df_preview_columns_selection = None
        self._row_preview_result = {}
        self._original_df_row_count = None

        self.symbols = symbols
        self._original_df_name = (
            guess_dataframe_name(df, symbols) if (df_name is None) else df_name
        )

        self.transformations = []
        self.redo_transformations = []

    def register_wrangler(self, wrangler):
        self.wrangler = wrangler

    def register_tab_section(self, tab_section):
        """
        :param tab_section: TabSection. Manages all tabs.
        """
        self.tab_section = tab_section

    def _user_added_transformations(self):
        return len(self.transformations) > 0

    def undo_is_possible(self):
        """Returns True if undo is possible. If it returns False, the undo button is disabled."""
        return self._user_added_transformations()

    def redo_is_possible(self):
        return len(self.redo_transformations) > 0

    def render_steps(self):
        """Render the transformation steps. They're e.g. displayed in the Transformation history view."""
        if self._user_added_transformations():
            descriptions = []

            descriptions = self._maybe_add_user_transformation_descriptions(
                descriptions
            )

            steps = widgets.VBox(descriptions)
        else:
            steps = widgets.HTML(
                "Currently, there is nothing to show. Please add some transformations"
            )
        return steps

    def _maybe_add_user_transformation_descriptions(self, descriptions):
        for transformation in self.transformations:
            contents = []
            contents.append(widgets.HTML(transformation.result["description"]))
            if transformation.can_be_edited_without_schema_change():
                edit_button = Button(icon="pencil", style="secondary")
                edit_button.on_click(self._create_open_transformation_callback(transformation))
                contents.append(edit_button)
            descriptions.append(widgets.HBox(contents))

        if self.undo_is_possible():  # maybe only if last transformation is not editable anyway?
            edit_button = Button(
                description="Edit last step", icon="pencil", style="primary"
            )
            edit_button.on_click(
                lambda _: log_action(
                    "general", "HistoryView", "click edit last transformation button"
                )
            )
            edit_button.on_click(self._open_edit_last_transformation)
            descriptions.append(edit_button)
        return descriptions

    def _open_edit_last_transformation(self, *args, **kwargs):
        self.transformations[LAST_LIST_ITEM].add_to(self.wrangler.side_window_outlet)

    def _create_open_transformation_callback(self, transformation):
        # Attention: this call has to happen in a function in order to keep the reference to the right transformation
        # When inlining the code in a for loop, always the last transformation will be chosen
        return lambda _: transformation.add_to(self.wrangler.side_window_outlet)

    def notify_that_df_did_change(self):
        """Notify all relevant components that the data has changed."""
        if self.wrangler is not None:
            self.wrangler.df_did_change()
        if self.tab_section is not None:
            self.tab_section.df_did_change()

    def maybe_add_transformation(self, transformation):
        if self.is_new_transformation(transformation):
            self.redo_transformations = []
            self.transformations.append(transformation)

    def execute_subsequent_transformations(self, current_transformation):
        execute_again = False
        for transformation in self.transformations:
            if transformation is current_transformation:
                execute_again = True  # everything after this one
                continue  # to the next because the current_transformation already got executed
            if execute_again:
                transformation.execute_again_as_side_effect_of_a_previous_transformation()

    def is_new_transformation(self, current_transformation):
        for old_transformation in self.transformations:
            if old_transformation is current_transformation:
                return False
        return True

    @updates_live_code_export
    def undo(self):
        self._try_to_move_last_item_to_another_list(
            origin=self.transformations, target=self.redo_transformations
        )
        self.notify_that_df_did_change()

    @updates_live_code_export
    def redo(self):
        self._try_to_move_last_item_to_another_list(
            origin=self.redo_transformations, target=self.transformations
        )
        self.notify_that_df_did_change()

    def _maybe_update_user_symbols(self):
        if self.show_live_code_export and self._user_added_transformations():
            for transformation in self.transformations:
                df_name = transformation.result["new_df_name"]
                df = transformation.result["result_df"]
                self.symbols[df_name] = df
        else:
            df_name = self._original_df_name
            df = self._original_df
            self.symbols[df_name] = df

    def _try_to_move_last_item_to_another_list(self, origin, target):
        """Helper to handle undo/redo transformation events."""
        try:
            # if the user clicks the button faster then the app can render, there is a list index error
            last_item = origin[-1]

            # only continue if there was no error:
            del origin[-1]  # removes last item
            target.append(last_item)
        except:
            pass

    def maybe_update_live_code_export_and_user_symbols(self):
        self._maybe_update_jupyter_cell_with_live_code_export()
        self._maybe_update_user_symbols()

    def _maybe_update_jupyter_cell_with_live_code_export(self):
        """Writes the current code export to the jupyter cell."""
        if self.show_live_code_export:
            code = self.get_setup_and_transformations_code()
            if code != "":
                code += f"{self.get_latest_df_name()}"
        else:
            code = ""  # remove code export

        # if self.wrangler is not None:
        #     self.wrangler.grid.send(
        #         {
        #             "type": "bam_live_code_export",
        #             "code_export": code,
        #             "initial_user_code": self._initial_user_code,
        #             "command_guid": self._command_guid,
        #         }
        #     )

    def get_setup_and_transformations_code(self):
        return self.code_formatter.get_setup_and_transformations_code()

    def set_initial_user_code(self, code):
        self.code_formatter.set_initial_user_code(code)

    def get_initial_user_code(self):
        return self.code_formatter.get_initial_user_code()

    def set_command_guid(self, command_guid):
        self._command_guid = command_guid

    def set_preview_columns_selection(self, selection):
        if self._user_added_transformations():
            self.transformations[LAST_LIST_ITEM].result[
                "preview_columns_selection"
            ] = selection
        else:
            self.original_df_preview_columns_selection = selection

    def get_preview_columns_selection(self):
        if self._user_added_transformations():
            # later, when we are trying to add names to the selection,
            # we might need to access the last preview_columns_selection in case of an edit
            # otherwise, always adding to the current/last selection is not idempotent any more
            return self.transformations[LAST_LIST_ITEM].result[
                "preview_columns_selection"
            ]
        else:
            return self.original_df_preview_columns_selection

    def get_latest_df(self):
        # Attention: the latest is different from the previous!
        # The latest is always the resulting df from the last transformation (or the original df)
        # The previous is relative to the standpoint of a transformation
        if self._user_added_transformations():
            return self.transformations[-1].result["result_df"]
        else:
            return self.df

    def get_latest_df_name(self):
        # Attention: the latest is different from the previous!
        # The latest is always the resulting df from the last transformation (or the original df)
        # The previous is relative to the standpoint of a transformation
        if self._user_added_transformations():
            name = self.transformations[LAST_LIST_ITEM].result["new_df_name"]
        else:
            name = self._original_df_name
        return name

    def get_previous_df(self, transformation):
        # Attention: the latest is different from the previous!
        # The latest is always the resulting df from the last transformation (or the original df)
        # The previous is relative to the standpoint of a transformation
        if len(self.transformations) == 0:
            return self.df
        
        if transformation in self.transformations:
            previous_index = self.transformations.index(transformation)-1
            if previous_index < 0:
                return self.df
            else:
                return self.transformations[previous_index].result["result_df"]
        else:
            # TBD: if we later want to support that transformations can be added e.g. from the middle instead of always added to the bottom
            # we might pass in the reference to the previous transformation to the new transformation when creating it
            raise Exception("Cannot determine the previous Dataframe because the transformation is neither registered nor does it know the previous transformation.")

    def get_previous_df_name(self, transformation):
        # Attention: the latest is different from the previous!
        # The latest is always the resulting df from the last transformation (or the original df)
        # The previous is relative to the standpoint of a transformation
        if len(self.transformations) == 0:
            return self._original_df_name
        
        if transformation in self.transformations:
            previous_index = self.transformations.index(transformation)-1
            if previous_index < 0:
                return self._original_df_name
            else:
                return self.transformations[previous_index].result["new_df_name"]
        else:
            raise Exception("Cannot determine the previous Dataframe name because the transformation is neither registered nor does it know the previous transformation.")

    def get_row_count_for_latest_df(self):
        # try to get result from cache
        if self._user_added_transformations():
            result = self.transformations[-1].result["row_count"]
        else:
            result = self._original_df_row_count
        
        if result is None:
            # calculate result
            result = self.get_latest_df().count()
            # save result for later
            if self._user_added_transformations():
                self.transformations[-1].result["row_count"] = result
            else:
                self._original_df_row_count = result
        return result

    def get_row_preview_result_for_latest_df(self, sample_style, row_count, columns_list):
        if self._user_added_transformations():
            cache = self.transformations[-1].result["row_preview_result"]
        else:
            cache = self._row_preview_result

        key = f"{sample_style}-{row_count}-{str(columns_list)}"
        if key in cache:
            return cache[key]
        else:
            result = self._load_preview_df(sample_style, row_count, columns_list)
            cache[key] = result
            return result

    def _load_preview_df(self, sample_style, row_count, columns_list):
        from pyspark.sql import SparkSession
        spark = SparkSession.getActiveSession()

        df = self.get_latest_df()

        if sample_style == "first":
            df = df.limit(row_count)
        elif sample_style == "random":
            df = spark.createDataFrame(df.rdd.takeSample(withReplacement=False, num=row_count), schema=df.schema)
        elif sample_style == "last":
            # schema is passed because sometimes there are errors that the schema cannot be inferred
            # e.g. https://stackoverflow.com/questions/40517553/pyspark-valueerror-some-of-types-cannot-be-determined-after-inferring
            df = spark.createDataFrame(df.tail(row_count), schema=df.schema)
        else:
            raise NotImplementedError

        return df.select(columns_list).cache().toPandas()

    def user_imported(self, symbol):
        """
        Returns True if the user imported a library

        :param symbol: symbol to import, NOT string.

        Example:
        print("import pandas as pd") if not self.user_imported(pd)
        """
        return any([symbol is value for name, value in self.symbols.items()])

CODE_FORMAT_CHAIN_STYLE = "chain"
CODE_FORMAT_ASSIGNMENT_STYLE = "assignment"

class CodeFormatter:
    def __init__(
        self,
        df_manager,
        setup_code=None,
        initial_user_code=None,
    ):
        self.df_manager = df_manager
        self.set_setup_code(setup_code)
        self.set_initial_user_code(initial_user_code)

    def set_setup_code(self, setup_code):
        if setup_code is None:
            self._setup_code = ""
        else:
            self._setup_code = setup_code.strip() + "\n"

    def set_initial_user_code(self, initial_user_code):
        self._initial_user_code = "" if initial_user_code is None else initial_user_code

    def get_initial_user_code(self):
        return self._initial_user_code

    def get_setup_and_transformations_code(self):
        """
        Helper that returns the full code for all the stuff that has been done to the dataframe.
        Currently, the full code contains imports for all pyspark symbols, setup code (e.g. from the data loader
        plugin) and transformations code.
        """

        # TBD
        setup_code = self._setup_code
        transformations_code = self._get_transformations_code()
        if (setup_code == "") and (transformations_code == ""):
            return ""
        else:
            # TBD: spark: adjust import
            # imports_code = "import pandas as pd; import numpy as np\n"
            imports_code = "import pyspark.sql.functions as f\n"
            return imports_code + setup_code + transformations_code

    def _get_transformations_code(self):
        # syntax_style = "pyspark"

        if len(self.df_manager.transformations) == 0:
            return ""

        format = get_option("global.code_format")
        if format == CODE_FORMAT_ASSIGNMENT_STYLE:
            code = self._get_assignment_transformations_code()
        else:  # CODE_FORMAT_CHAIN_STYLE
            if all([transformation.result['code']['pyspark_chain_format'] is not None for transformation in self.df_manager.transformations]):
                code = self._get_chained_transformations_code()
            else:
                unsupported_transformation = [transformation for transformation in self.df_manager.transformations if transformation.result['code']['pyspark_chain_format'] is None][0]
                description = remove_html_tags(unsupported_transformation.result["description"])
                code = f"""
# The following step cannot be exported to the current code format:
# {description}
# Please select a different code format. The pyspark assignment style will always work.
""".strip()

        # Don't add the df again because otherwise we nudge the people to execute the cell again
        # AND afterwards do more transformations which then cannot be executed in the same cell any more
        # because the pandas operations are usually not idempotent
        # code += DF_OLD
        return code

    def _get_assignment_transformations_code(self):
        code = ""

        for transformation in self.df_manager.transformations:
            new_code = ""

            if get_option("global.export_transformation_descriptions"):
                description = remove_html_tags(transformation.result["description"])
                new_code += f"# {description}\n"

            new_code += f"{transformation.result['code']['pyspark_assignment_format']}\n"
            new_code = replace_code_placeholder(
                new_code,
                old_df_name=transformation.result["old_df_name"],
                new_df_name=transformation.result["new_df_name"],
            )

            code += new_code
        return code
    
    def _get_chained_transformations_code(self):
        old_df_name = self.df_manager.transformations[0].result["old_df_name"]
        new_df_name = self.df_manager.transformations[LAST_LIST_ITEM].result["new_df_name"]

        INDENTATION = "    "
        chain_steps = ""
        for transformation in self.df_manager.transformations:
            if get_option("global.export_transformation_descriptions"):
                description = remove_html_tags(transformation.result["description"])
                chain_steps += f"{INDENTATION}# {description}\n"

            new_code = transformation.result['code']['pyspark_chain_format']
            # Usually, the chained code should not contain DF_OLD or DF_NEW placeholder but you never know
            new_code = replace_code_placeholder(
                new_code,
                old_df_name=transformation.result["old_df_name"],
                new_df_name=transformation.result["new_df_name"],
            )
            chain_steps += f"{INDENTATION}{new_code}\n"

        return f"""
{new_df_name} = (
    {old_df_name}
    {chain_steps.strip()}
)
{new_df_name}
""".strip()
