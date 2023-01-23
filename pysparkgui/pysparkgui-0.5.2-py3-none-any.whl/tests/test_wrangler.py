import numpy as np
import pandas as pd
import pysparkgui

# from pysparkgui.df_manager import DfManager
from pysparkgui.spark_wrangler import SparkWrangler
from pysparkgui._authorization import auth


def create_wrangler(monkeypatch, is_databricks):
    def mock_is_databricks(*args):
        return is_databricks

    monkeypatch.setattr(auth, "is_databricks", mock_is_databricks)

    df = pd.DataFrame(np.random.randn(10, 4), columns=list("ABCD"))
    df_manager = DfManager(df)
    wrangler = SparkWrangler(df_manager=df_manager)
    # history_line is initialized on .render()
    wrangler.render()

    return wrangler


def feedback_survey_link_is_displayed(wrangler):
    return (
        wrangler.history_line.feedback_survey_link
        in wrangler.history_line.children[0].children
    )


def test__if_not_inside_databricks_notebook__feedback_survey_link_is_not_displayed(
    monkeypatch,
):
    wrangler = create_wrangler(monkeypatch, is_databricks=False)
    assert not feedback_survey_link_is_displayed(wrangler)


def test__if_inside_databricks_notebook__feedback_survey_link_is_displayed(
    monkeypatch,
):
    wrangler = create_wrangler(monkeypatch, is_databricks=True)
    assert feedback_survey_link_is_displayed(wrangler)
