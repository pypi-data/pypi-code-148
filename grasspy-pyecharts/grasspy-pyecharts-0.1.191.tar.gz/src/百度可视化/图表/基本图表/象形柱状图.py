从 pyecharts.charts.basic_charts.pictorialbar 导入 PictorialBar
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇象形柱状图(PictorialBar):
    套路 添加y轴(
        分身,
        系列名称,
        y轴,
        *,
        记号=空,
        记号大小=空,
        记号位置=空,
        记号偏移=空,
        记号旋转=空,
        记号重复=空,
        记号重复方向=空,
        记号边距=空,
        裁剪记号=假,
        选中=真,
        x轴索引=空,
        y轴索引=空,
        颜色=空,
        类目间隙="20%",
        间隙=空,
        标签选项々=选项.〇标签选项々(),
        标记点选项々=空,
        标记线选项々=空,
        提示框选项々=空,
        图元样式选项々=空,
        编码=空,
    ):
        返回 分身.add_yaxis(
            系列名称,
            y轴,
            symbol=记号,
            symbol_size=记号大小,
            symbol_pos=记号位置,
            symbol_offset=记号偏移,
            symbol_rotate=记号旋转,
            symbol_repeat=记号重复,
            symbol_repeat_direction=记号重复方向,
            symbol_margin=记号边距,
            is_symbol_clip=裁剪记号,
            is_selected=选中,
            xaxis_index=x轴索引,
            yaxis_index=y轴索引,
            color=颜色,
            category_gap=类目间隙,
            gap=间隙,
            label_opts=标签选项々,
            markpoint_opts=标记点选项々,
            markline_opts=标记线选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
            encode=编码,
        )


_反向注入(〇象形柱状图, PictorialBar)