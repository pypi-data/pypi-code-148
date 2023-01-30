from pyecharts.charts.composite_charts.grid import Grid

类 〇栅格(Grid):
    套路 添加(
        分身,
        图表,
        栅格选项々,
        *,
        栅格索引=0,
        控制坐标轴索引=假
    ):
        返回 分身.add(
            图表,
            栅格选项々,
            grid_index=栅格索引,
            is_control_axis_index=控制坐标轴索引
        )