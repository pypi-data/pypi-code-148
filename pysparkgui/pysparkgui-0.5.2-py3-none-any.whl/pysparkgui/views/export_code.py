# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import Viewable, log_action
from pysparkgui.config import get_option, set_option
from pysparkgui.widgets import CopyButton, Singleselect
from pysparkgui.spark_df_manager import CODE_FORMAT_CHAIN_STYLE, CODE_FORMAT_ASSIGNMENT_STYLE

class ExportCodeView(Viewable):
    """
    A view to export the current transformations code
    """

    def render(self):
        self.code = self.df_manager.get_setup_and_transformations_code()

        self.copy_button = CopyButton(
            copy_string=self.code,
            style="primary",
            on_click=lambda _: log_action("export", self, "click copy code"),
        )

        def update_code_format(singleselect):
            set_option("global.code_format", singleselect.value)
            self.render()
        
        self.code_format = Singleselect(
            options=[
                        ("Code format: assignment style", CODE_FORMAT_ASSIGNMENT_STYLE),
                        ("Code format: chain style", CODE_FORMAT_CHAIN_STYLE)
                    ],
            value=get_option("global.code_format"),
            set_soft_value=True,
            placeholder="Select code format",
            width="lg",
            on_change=update_code_format,
        )

        self.textarea = widgets.Textarea(value=self.code).add_class(
            "pysparkgui-width-auto"
        )
        self.textarea.add_class("pysparkgui-code-export")

        self.set_title("Export code")

        if self.code == "":
            self.set_content(
                widgets.HTML(
                    "Currently, there is no code to export. Please add some transformations"
                )
            )
        else:
            self.set_content(self.copy_button, self.code_format, self.textarea)
