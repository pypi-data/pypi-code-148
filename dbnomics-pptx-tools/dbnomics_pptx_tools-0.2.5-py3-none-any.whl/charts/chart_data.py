from datetime import datetime
from typing import Iterator, cast

import daiquiri
import numpy as np
import pandas as pd
from pandas import DataFrame, DatetimeIndex
from pptx.chart.data import CategoryChartData

from dbnomics_pptx_tools.metadata import ChartSpec
from dbnomics_pptx_tools.repo import SeriesRepo

logger = daiquiri.getLogger(__name__)


def build_category_chart_data(chart_spec: ChartSpec, *, pivoted_df: DataFrame) -> CategoryChartData:
    chart_data = CategoryChartData()

    chart_data.categories = cast(DatetimeIndex, pivoted_df.index).to_pydatetime()

    for series_spec in chart_spec.series:
        series_id = series_spec.id
        if series_id not in pivoted_df:
            logger.warning("Could not find series %r in the pivoted DataFrame", series_id)
            continue
        series = pivoted_df[series_id]
        series = series.replace({np.NaN: None})
        chart_data.add_series(series_spec.name, series.values)

    return chart_data


def filter_df_to_domain(df: DataFrame, *, max_datetime: datetime | None, min_datetime: datetime | None) -> DataFrame:
    if min_datetime is not None:
        df = df.query("period >= @min_datetime")
    if max_datetime is not None:
        df = df.query("period <= @max_datetime")
    return df


def load_chart_df(chart_spec: ChartSpec, *, repo: SeriesRepo) -> DataFrame:
    def iter_series_dfs() -> Iterator[DataFrame]:
        for series_spec in chart_spec.series:
            series_id = series_spec.id
            df = repo.load(series_id)
            if df.empty:
                logger.warning("Series %r is empty", series_id)
                continue
            df["chart_series_name"] = series_spec.name
            df["value"] = series_spec.apply_transformers(df["value"], series_id=series_id)
            yield df

    return pd.concat(iter_series_dfs())
