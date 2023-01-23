# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.plugins import LoaderPlugin, DF_NEW, Singleselect
from pysparkgui.helper import AuthorizedPlugin
from pysparkgui.widgets import Text

class SparkTableLoader(AuthorizedPlugin, LoaderPlugin):
    """
    Allows the user to select pysparkgui's exposed dummy datasets, e.g. titanic and sales dataset.
    """

    name = "SparkGUI: load table"
    new_df_name_placeholder = "df"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_name = Text(
            value="florian_wetschoreck.wikipedia_apache_spark_and_hadoop",
            description="spark table name",
            width="xl",
            execute=self,
        )

    def render(self):
        self.set_title("SparkGUI: load table")
        self.set_content(
            widgets.HTML("Load table"),
            self.table_name,
            self.new_df_name_group,
            self.execute_button,
        )

    def get_code(self):
        return f"""
                    {DF_NEW} = spark.table("{self.table_name.value}")
                """
