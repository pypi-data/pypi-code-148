从 pyecharts.charts.basic_charts.calendar 导入 Calendar
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇日历图(Calendar):
    套路 添加(
        分身,
        系列名称,
        y轴数据,
        *,
        选中=真,
        标签选项々=选项.〇标签选项々(),
        日历选项々=空,
        提示框选项々=空,
        图元样式选项々=空,
    ):
        返回 分身.add(
            series_name=系列名称,
            yaxis_data=y轴数据,
            is_selected=选中,
            label_opts=标签选项々,
            calendar_opts=日历选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
        )

_反向注入(〇日历图, Calendar)