从 pyecharts.charts.basic_charts.kline 导入 Kline
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇蜡烛图(Kline):
    套路 添加y轴(
        分身,
        系列名称,
        y轴,
        *,
        选中=真,
        x轴索引=空,
        y轴索引=空,
        标记线选项々=空,
        标记点选项々=空,
        提示框选项々=空,
        图元样式选项々=空,
    ):
        返回 分身.add_yaxis(
            series_name=系列名称,
            y_axis=y轴,
            is_selected=选中,
            xaxis_index=x轴索引,
            yaxis_index=y轴索引,
            markline_opts=标记线选项々,
            markpoint_opts=标记点选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
        )

_反向注入(〇蜡烛图, Kline)