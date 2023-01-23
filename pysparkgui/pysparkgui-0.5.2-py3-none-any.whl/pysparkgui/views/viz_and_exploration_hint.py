# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import TabViewable
from pysparkgui.widgets import CodeOutput
from pysparkgui._path import pysparkgui_LIBRARY_ROOT_PATH

class SparkVizAndExplorationHint(TabViewable):

    def render(self):
        df_name = self.df_manager.get_latest_df_name()
        
        content = []
        content.append(widgets.HTML(f"If you want to visualize or explore (profile) your table, please use the functionality that is built in to the Databricks notebook."))
        content.append(widgets.HTML(f"Therefore, run a new notebook cell which contains the following code:"))
        # there was a bug on 2022-10-18 in logfood master where the CodeOutput would not be shown here
        # content.append(CodeOutput(code=f"display({df_name})"))
        # thus, we use a plain HTML
        content.append(widgets.HTML(f"<pre>display({df_name})</pre>"))
        content.append(widgets.HTML(f"<br>For example, if your table is named <i>df</i>:"))
        explanation_image = widgets.Image(
            value=open(
                pysparkgui_LIBRARY_ROOT_PATH / "assets" / "img" / "viz_and_profile_tabs_in_databricks_display.png",
                "rb",
            ).read(),
            format="png",
            layout={"width": "625px", "height": "250px"},
        )
        content.append(explanation_image)

        self.set_title("Visualize and explore the table")
        self.set_content(widgets.VBox(content, layout={"height":"44em"}))


