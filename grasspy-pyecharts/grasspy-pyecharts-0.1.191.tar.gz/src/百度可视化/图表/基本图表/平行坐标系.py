从 pyecharts.charts.basic_charts.parallel 导入 Parallel
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇平行坐标系(Parallel):
    套路 添加纲要(分身, 纲要, 平行坐标系选项々=空):
        返回 分身.add_schema(纲要, parallel_opts=平行坐标系选项々)

    套路 添加(
        分身,
        系列名称,
        数据,
        *,
        平滑=假,
        选中=真,
        线条样式选项々=选项.〇线条样式选项々(),
        提示框选项々=空,
        图元样式选项々=空,
    ):
        返回 分身.add(
            系列名称,
            数据,
            is_smooth=平滑,
            is_selected=选中,
            linestyle_opts=线条样式选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
        )


_反向注入(〇平行坐标系, Parallel)