# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.plugins import TransformationPlugin, Text, Singleselect, PysparkguiError


class SparkDrawSample(TransformationPlugin):

    name = "Random sample"
    description = "Draw a random sample of table rows with or without replacement"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fraction = Text(
            placeholder="Number between 0.0 and 100.0",
            width="lg",
            on_submit=lambda _: self.execute(),
        )
        self.replacement = Singleselect(
            options=[
                ("The same row cannot be drawn twice ('without replacement')", False),
                ("The same row can be drawn twice ('with replacement')", True),
            ],
            set_soft_value=True,
            width="2xl",
        )
        self.seed = Singleselect(
            options=[
                ("Keep sample constant ('stable seed')", 0),
                ("Change sample after every execution ('no seed')", None),
            ],
            set_soft_value=True,
            width="2xl",
        )


    def render(self):
        self.set_title("Draw a random sample")
        self.set_content(
            widgets.HTML("Fraction - percentage of total rows that are drawn"),
            self.fraction,
            widgets.HTML("Replacement"),
            self.replacement,
            widgets.HTML("Randomness"),
            self.seed,
            self.rename_df_group,
            )

    def is_valid_transformation(self):
        try:
            fraction = float(self.fraction.value)
            assert(fraction >= 0.0)
            assert(fraction <= 100.0)
        except:
            raise PysparkguiError("""It seems like the fraction is not a valid number between 0.0 and 100.0
            <br>Please make sure to use a point as decimal separator and not a comma.""")
        return True

    def get_description(self):
        replacement = self.replacement.label.lower()
        seed = self.seed.label.lower()
        return (
            f"<b>Random sample:</b> draw {self.fraction.value}% of rows where {replacement} and {seed}"
        )

    def get_pyspark_chain_code(self):
        return f".sample(fraction={float(self.fraction.value)/100.0}, withReplacement={self.replacement.value}, seed={self.seed.value})"

    def can_be_edited_without_schema_change(self):
        return True
