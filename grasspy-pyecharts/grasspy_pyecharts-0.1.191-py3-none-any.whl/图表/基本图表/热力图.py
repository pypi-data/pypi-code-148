从 pyecharts.charts.basic_charts.heatmap 导入 HeatMap
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇热力图(HeatMap):
    套路 添加y轴(
        分身,
        系列名称,
        y轴数据,
        值,
        *,
        选中=真,
        x轴索引=空,
        y轴索引=空,
        标签选项々=选项.〇标签选项々(),
        标记点选项々=空,
        标记线选项々=空,
        提示框选项々=空,
        图元样式选项々=空,
    ):
        返回 分身.add_yaxis(
            系列名称,
            y轴数据,
            值,
            is_selected=选中,
            xaxis_index=x轴索引,
            yaxis_index=y轴索引,
            label_opts=标签选项々,
            markpoint_opts=标记点选项々,
            markline_opts=标记线选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
        )


_反向注入(〇热力图, HeatMap)