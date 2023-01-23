import dataclasses
from dataclasses import dataclass
from typing import Iterable, Iterator, cast

import daiquiri
from lxml import etree
from pandas import DataFrame
from pptx.chart.chart import Chart
from pptx.chart.datalabel import DataLabel
from pptx.chart.plot import _BasePlot
from pptx.chart.point import Point
from pptx.chart.series import _BaseCategorySeries
from pptx.dml.line import LineFormat
from pptx.oxml.ns import nsdecls

from dbnomics_pptx_tools.metadata import ChartSpec, DataLabelPosition
from dbnomics_pptx_tools.pptx_copy import copy_color_format_properties, copy_font_properties
from dbnomics_pptx_tools.xml_utils import remove_element

logger = daiquiri.getLogger(__name__)


@dataclass
class DataLabelRenderData:
    series: _BaseCategorySeries
    point: Point
    ratio: float
    new_ratio: float | None

    @property
    def ratio_distance(self) -> float | None:
        if self.new_ratio is None:
            return None
        return self.new_ratio - self.ratio


def add_data_label_to_last_point_of_each_series(
    chart: Chart, *, chart_spec: ChartSpec, pivoted_df: DataFrame, points_by_series_name: dict[str, list[Point]]
):
    logger.debug("Adding a data label to the last point of each series of the chart...")

    render_data_list = compute_data_label_positions(
        chart, chart_spec=chart_spec, pivoted_df=pivoted_df, points_by_series_name=points_by_series_name
    )

    for render_data in render_data_list:
        apply_render_data_to_chart(render_data, chart=chart)


def apply_render_data_to_chart(render_data: DataLabelRenderData, *, chart: Chart):
    logger.debug("Adding data label to chart for series %r...", render_data.series.name)
    value_axis_font = chart.value_axis.tick_labels.font

    data_label = cast(DataLabel, render_data.point.data_label)
    copy_font_properties(value_axis_font, data_label.font)
    dLbl_element = data_label._get_or_add_dLbl()

    numFmt_element = dLbl_element.find("./{*}numFmt")
    if numFmt_element is None:
        numFmt_element = etree.fromstring(f"""<c:numFmt {nsdecls("c")} />""")
        dLbl_element.append(numFmt_element)
    numFmt_element.attrib["formatCode"] = "0.0"
    numFmt_element.attrib["sourceLinked"] = "0"
    dLbl_element.find("./{*}showVal").attrib["val"] = "1"
    line = LineFormat(data_label._dLbl.get_or_add_spPr())
    copy_color_format_properties(render_data.series.format.line.color, line.color)

    ratio_distance = render_data.ratio_distance
    if ratio_distance is not None:
        logger.debug(
            "Moving the data label of the series %r because if is too close to the previous one",
            render_data.series.name,
        )
        layout_element = etree.fromstring(
            f"""
                <c:layout {nsdecls("c")}>
                    <c:manualLayout>
                        <c:x val="0"/>
                        <c:y val="{-ratio_distance}"/>
                    </c:manualLayout>
                </c:layout>
            """.strip()
        )
        dLbl_element.append(layout_element)


def compute_data_label_positions(
    chart: Chart, *, chart_spec: ChartSpec, pivoted_df: DataFrame, points_by_series_name: dict[str, list[Point]]
) -> list[DataLabelRenderData]:
    logger.debug("Computing data label positions...")
    render_data_list: list[DataLabelRenderData] = []

    for chart_series in cast(Iterable[_BaseCategorySeries], chart.series):
        series_id = chart_spec.find_series_id_by_name(chart_series.name)
        series = pivoted_df.reset_index()[series_id]
        last_value_index = series.last_valid_index()
        if last_value_index is None:
            logger.warning("The series %r (%r) only has NA values, skipping", chart_series.name, series_id)
            continue

        last_value = series[last_value_index]
        ratio = compute_data_label_ratio(last_value, chart=chart, pivoted_df=pivoted_df)
        last_point = points_by_series_name[chart_series.name][last_value_index]
        render_data_list.append(DataLabelRenderData(series=chart_series, point=last_point, ratio=ratio, new_ratio=None))

    render_data_list = sorted(render_data_list, key=lambda render_data: render_data.ratio)
    return list(iter_spaced_data_labels(render_data_list))


def compute_data_label_ratio(value: float, *, chart: Chart, pivoted_df: DataFrame) -> float:
    chart_min_value, chart_max_value = compute_value_axis_bounds(pivoted_df, chart=chart)
    chart_value_range = chart_max_value - chart_min_value
    return (value - chart_min_value) / chart_value_range


def compute_value_axis_bounds(pivoted_df: DataFrame, *, chart: Chart, margin_ratio: float = 0.1) -> tuple[float, float]:
    min_value = pivoted_df.min().min()
    max_value = pivoted_df.max().max()
    margin = (max_value - min_value) * margin_ratio
    minimum_scale = chart.value_axis.minimum_scale
    maximum_scale = chart.value_axis.maximum_scale
    return (
        minimum_scale if minimum_scale is not None else min_value - margin,
        maximum_scale if maximum_scale is not None else max_value + margin,
    )


def iter_spaced_data_labels(
    render_data_list: list[DataLabelRenderData], *, min_ratio_distance: float = 0.05
) -> Iterator[DataLabelRenderData]:
    if not render_data_list:
        return []

    yield render_data_list[0]
    last_ratio = render_data_list[0].ratio

    for current in render_data_list[1:]:
        if current.ratio - last_ratio < min_ratio_distance:
            new_ratio = last_ratio + min_ratio_distance
            yield dataclasses.replace(current, new_ratio=new_ratio)
            last_ratio = new_ratio
        else:
            yield current
            last_ratio = current.ratio


def remove_data_labels(chart: Chart, *, points_by_series_name: dict[str, list[Point]]) -> None:
    for plot_index, plot in enumerate(cast(Iterable[_BasePlot], chart.plots)):
        if plot.has_data_labels:
            logger.debug("Plot #%d has data labels, removing", plot_index)
            plot.has_data_labels = False
        for series in cast(Iterable[_BaseCategorySeries], plot.series):
            series_points = points_by_series_name[series.name]
            for point_position, point in enumerate(series_points, start=1):
                data_label = cast(DataLabel, point.data_label)
                if data_label._dLbl is not None:
                    logger.debug(
                        "Point %d/%d of series %r has a data label, removing",
                        point_position,
                        len(series_points),
                        series.name,
                    )
                    remove_element(data_label._dLbl)


def update_data_labels(chart: Chart, *, chart_spec: ChartSpec, pivoted_df: DataFrame):
    points_by_series_name = {series.name: list(series.points) for series in chart.series}
    remove_data_labels(chart, points_by_series_name=points_by_series_name)
    if DataLabelPosition.LAST_POINT.value in chart_spec.data_labels:
        add_data_label_to_last_point_of_each_series(
            chart, chart_spec=chart_spec, pivoted_df=pivoted_df, points_by_series_name=points_by_series_name
        )
