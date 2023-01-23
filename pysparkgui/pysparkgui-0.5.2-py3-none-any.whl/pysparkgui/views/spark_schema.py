# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import TabViewable


class SparkSchemaView(TabViewable):
    """
    A view to see the current spark schema
    """

    def render(self):
        df = self.df_manager.get_latest_df()
        
        columns = []
        columns.append(widgets.HTML(f"<b>Column name - Data type</b>"))

        for column_name, data_type in df.dtypes:
            columns.append(widgets.HTML(f"{column_name} - {data_type}"))

        self.set_title("Schema")
        self.set_content(widgets.VBox(columns, layout={"height":"44em"}))

