从 pyecharts.charts.basic_charts.pie 导入 Pie
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇饼图(Pie):
    套路 添加(
        分身,
        系列名称,
        数据对,
        *,
        颜色=空,
        半径=空,
        中心=空,
        玫瑰类型=空,
        顺时针=空,
        标签选项々=选项.〇标签选项々(),
        标签视觉引导线选项々=空,
        提示框选项々=空,
        图元样式选项々=空,
        编码=空,
    ):
        返回 分身.add(
            系列名称,
            数据对,
            color=颜色,
            radius=半径,
            center=中心,
            rosetype=玫瑰类型,
            is_clockwise=顺时针,
            label_opts=标签选项々,
            label_line_opts=标签视觉引导线选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
            encode=编码
        )


_反向注入(〇饼图, Pie)