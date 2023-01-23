# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import (
    Viewable,
    show_loader_and_maybe_error_modal,
    log_action,
    notification,
)

from pysparkgui.widgets import Text, Button


class ExportToVariableView(Viewable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.symbols = self.df_manager.symbols

    def render(self):
        header = widgets.HTML(f"Export current table to a name ('variable') in the notebook")

        self.variable_input = Text(value="", placeholder="Name ('variable')", execute=self)

        self.warning = widgets.VBox()

        self.execute_button = Button(
            description="Execute",
            style="primary",
            on_click=lambda button: self.execute(),
        )

        self.set_title("Export to name ('variable') in notebook")
        self.set_content(
            header,
            self.variable_input,
            self.warning,
            widgets.HTML("<br>"),
            self.execute_button,
        )

    @show_loader_and_maybe_error_modal
    def execute(self):
        if self.variable_input.value == "":
            self.warning.children = [
                notification("The name cannot be empty", type="error")
            ]
            return False
        else:
            self._assign_to_variable()
            return True

    def _assign_to_variable(self):
        df = self.df_manager.get_latest_df()
        self.symbols[self.variable_input.value] = df
        log_action("export", self, "export to variable")
