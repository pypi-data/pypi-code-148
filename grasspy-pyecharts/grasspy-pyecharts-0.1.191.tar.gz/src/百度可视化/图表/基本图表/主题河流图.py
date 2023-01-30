从 pyecharts.charts.basic_charts.themeriver 导入 ThemeRiver
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇主题河流图(ThemeRiver):
    套路 添加(
        分身,
        系列名称,
        数据,
        *,
        选中=真,
        标签选项々=选项.〇标签选项々(),
        单轴选项々=选项.〇单轴选项々(),
        提示框选项々=空,
        图元样式选项々=空,
    ):
        返回 分身.add(
            系列名称,
            数据,
            is_selected=选中,
            label_opts=标签选项々,
            singleaxis_opts=单轴选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
        )


_反向注入(〇主题河流图, ThemeRiver)