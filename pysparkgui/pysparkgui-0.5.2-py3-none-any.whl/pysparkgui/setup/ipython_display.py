# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

from IPython.display import display
from pysparkgui.widgets.table_output import TableOutput
import ipywidgets as widgets
import pandas as pd

from pysparkgui.helper import (
    log_jupyter_action,
    log_action,
    log_databricks_funnel_event,
    get_dataframe_variable_names,
)
import pysparkgui.config as _config
from pysparkgui.widgets import Button


# def pandas_display_df(df, *args, **kwargs):
#     log_jupyter_action("other", "JupyterCell", "pandas display(df)")

#     display_data = {"text/plain": df.__repr__(), "text/html": df._repr_html_()}
#     display(display_data, raw=True)


# class ToggleRow(widgets.HBox):
#     """
#     A widget that allows the user to switch from the static pandas.Dataframe view to the pysparkgui UI and back

#     :param df: the pandas.Dataframe
#     :param df_outlet: the widget in which the Dataframe is displayed
#     :param static_html: a widget that holds the static HTML content
#     :param pysparkgui_ui: the widget that holds the interactive pysparkgui_ui
#     :param show_pysparkgui_ui: bool, whether the pysparkgui UI should automatically be opened once the pysparkgui UI is ready. The user will activate this behaviour once she clicks on the "Show pysparkgui UI" button.

#     """

#     def __init__(
#         self, df, df_outlet, static_html, pysparkgui_ui=None, show_pysparkgui_ui=False
#     ):
#         super().__init__()
#         self.df = df

#         self.show_pysparkgui_ui = show_pysparkgui_ui
#         self.loading = True

#         self.static_html = static_html

#         if pysparkgui_ui is None:
#             pysparkgui_ui = self._get_loading_widget()
#         self.pysparkgui_ui = pysparkgui_ui
#         self.pysparkgui_ui_outlet = widgets.VBox([self.pysparkgui_ui])

#         self.render()
#         df_outlet.children = [static_html, self.pysparkgui_ui_outlet]

#     def _get_loading_widget(self):
#         return widgets.HTML("pysparkgui is loading ...")

#     def _get_show_static_html_button(self):
#         def click(button):
#             self.show_pysparkgui_ui = False
#             _config.SHOW_pysparkgui_UI = False
#             self.render()
#             try:
#                 log_action("general", "JupyterCell", "click 'Show static HTML' button")
#             except:
#                 pass

#         return Button(
#             description="Show static HTML",
#             css_classes=["pysparkgui-button-secondary-outline"],
#             on_click=click,
#         )

#     def _get_show_pysparkgui_button(self):
#         if self.loading:
#             return self._get_loading_widget()
#         else:

#             def click(button):
#                 self.show_pysparkgui_ui = True
#                 _config.SHOW_pysparkgui_UI = True
#                 # Only show new version notification once per session
#                 _config.SHOW_NEW_VERSION_NOTIFICATION = False
#                 self.render()
#                 self._maybe_notify_pysparkgui_ui()
#                 log_databricks_funnel_event("Show pysparkgui UI - click")
#                 log_action("general", "JupyterCell", "click 'Show pysparkgui UI' button")

#             return Button(
#                 description="Show pysparkgui UI",
#                 style="primary",
#                 css_classes=["pysparkgui-show-ui-button"],
#                 on_click=click,
#             )

#     def render(self):
#         if self.show_pysparkgui_ui:
#             header = self._get_show_static_html_button()
#             self.static_html.add_class("pysparkgui-hidden")
#             self.pysparkgui_ui_outlet.remove_class("pysparkgui-hidden")
#         else:
#             header = self._get_show_pysparkgui_button()
#             self.static_html.remove_class("pysparkgui-hidden")
#             self.pysparkgui_ui_outlet.add_class("pysparkgui-hidden")
#         self.children = [header]

#     def _maybe_notify_pysparkgui_ui(self):
#         try:
#             self.pysparkgui_ui.show_ui()
#         except AttributeError:
#             # in case that the ui is not a wrangler but an error we cannot call show_ui
#             # ... eg when the user df is not available as a variable
#             pass

#     def register_ui(self, pysparkgui_ui):
#         self.pysparkgui_ui = pysparkgui_ui
#         self.pysparkgui_ui_outlet.children = [pysparkgui_ui]
#         self.loading = False

#         self.render()
#         self._maybe_notify_pysparkgui_ui()


# def display_rich_df(df, app):
#     """
#     Displays a rich representation of the Dataframe that supports the formats:
#     text/plain, text/html, and ipywidgets.

#     The frontend then decides based on its capabilities which representation to show.
#     The frontend usually shows the richest representation that is supports.
#     Usually, the ipywidget-representation should be considered the richest representation.

#     :param df: Dataframe
#     :param app: ipywidget pysparkgui app
#     """
#     app_widget_data = {"model_id": app._model_id}
#     full_widget_data = {
#         "text/plain": df.__repr__(),
#         # "text/html": df._repr_html_(),
#         "application/vnd.jupyter.widget-view+json": app_widget_data,
#     }
#     display(full_widget_data, raw=True)


# def pysparkgui_display_df(df, *args, **kwargs):
#     """
#     Displays the interactive pysparkgui representation of a pandas.Dataframe
#     :param df: pandas.Dataframe
#     """
#     from pysparkgui.setup.user_symbols import get_user_symbols

#     show_pysparkgui_ui = _config.SHOW_pysparkgui_UI
#     if show_pysparkgui_ui:
#         log_jupyter_action("other", "JupyterCell", "pysparkgui display(df) - UI")
#     else:
#         log_jupyter_action("other", "JupyterCell", "pysparkgui display(df) - static")

#     df_html_output = TableOutput(df)
#     df_outlet = widgets.VBox([df_html_output])

#     toggle_row = ToggleRow(
#         df, df_outlet, df_html_output, show_pysparkgui_ui=show_pysparkgui_ui
#     )

#     app_outlet = widgets.VBox([toggle_row, df_outlet])
#     display_rich_df(df, app_outlet)

#     # Attention: symbols and df_name need to be determined before thread
#     # because otherwise the symbols cannot be retrieved via inspect
#     # and the df identities and names might change in parallel/following code
#     symbols = get_user_symbols()
#     possible_df_names = get_dataframe_variable_names(df, symbols)
#     df_name = None if len(possible_df_names) == 0 else possible_df_names[0]

#     lazy_load_pysparkgui_ui(df, toggle_row, symbols, df_name)


# def lazy_load_pysparkgui_ui(df, toggle_row, symbols, df_name):
#     """
#     Asynchronously creates and shows the pysparkgui Dataframe UI

#     :param df: pandas.Dataframe
#     :param toggle_row: ToggleRow - the manager for toggling the representations
#     :param symbols: dict - user namespace symbols
#     :param df_name: str - variable name of the df
#     """
#     from pysparkgui.spark_wrangler import create_dataframe_ui

#     def load_pysparkgui_ui():
#         toggle_row.register_ui(
#             create_dataframe_ui(
#                 df, symbols=symbols, origin="ipython_display", df_name=df_name
#             )
#         )

#     from pysparkgui.helper import execute_asynchronously

#     execute_asynchronously(load_pysparkgui_ui)


# def extend_pandas_ipython_display():
#     """
#     Changes the representation of all pandas.Dataframes to use the interactive pysparkgui representation
#     """
#     pd.DataFrame._ipython_display_ = pysparkgui_display_df


# def reset_pandas_ipython_display():
#     """
#     Reset the pandas.Dataframe representation to not include the rich pysparkgui UI
#     """
#     pd.DataFrame._ipython_display_ = pandas_display_df


def extend_spark_ipython_display():
    import pyspark
    pyspark.sql.dataframe.DataFrame._ipython_display_ = sparkgui_display_df


def sparkgui_display_df(df, *args, **kwargs):
    from pysparkgui.spark_wrangler import create_dataframe_ui
    from pysparkgui.setup.user_symbols import get_user_symbols

    # Attention: symbols and df_name need to be determined before any threads
    # because otherwise the symbols cannot be retrieved via inspect
    # and the df identities and names might change in parallel/following code
    symbols = get_user_symbols()
    possible_df_names = get_dataframe_variable_names(df, symbols)
    df_name = None if len(possible_df_names) == 0 else possible_df_names[0]

    display(
        create_dataframe_ui(
                df,
                symbols=symbols,
                df_name=df_name,
            )
        )

