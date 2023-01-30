从 pyecharts.charts.basic_charts.scatter 导入 Scatter
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇散点图(Scatter):
    套路 添加y轴(
        分身,
        系列名称,
        y轴,
        *,
        选中=真,
        x轴索引=空,
        y轴索引=空,
        颜色=空,
        记号=空,
        记号大小=10,
        记号旋转=空,
        标签选项々=选项.〇标签选项々(位置="右"),
        标记点选项々=空,
        标记线选项々=空,
        标记区选项々=空,
        提示框选项々=空,
        图元样式选项々=空,
        编码=空,
    ):
        返回 分身.add_yaxis(
            系列名称,
            y轴,
            is_selected=选中,
            xaxis_index=x轴索引,
            yaxis_index=y轴索引,
            color=颜色,
            symbol=记号,
            symbol_size=记号大小,
            symbol_rotate=记号旋转,
            label_opts=标签选项々,
            markpoint_opts=标记点选项々,
            markline_opts=标记线选项々,
            markarea_opts=标记区选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
            encode=编码,
        )


_反向注入(〇散点图, Scatter)