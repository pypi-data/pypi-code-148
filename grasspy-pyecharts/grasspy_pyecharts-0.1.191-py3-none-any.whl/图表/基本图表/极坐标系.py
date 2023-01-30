从 pyecharts.charts.basic_charts.polar 导入 Polar
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇极坐标系(Polar):
    套路 添加纲要(
        分身,
        径向轴选项々=选项.〇径向轴选项々(),
        角度轴选项々=选项.〇角度轴选项々(),
    ):
        返回 分身.add_schema(radiusaxis_opts=径向轴选项々, angleaxis_opts=角度轴选项々)

    套路 添加(
        分身,
        系列名称,
        数据,
        *,
        选中=真,
        类型_="line",
        记号=空,
        记号大小=4,
        堆叠=空,
        标签选项々=选项.〇标签选项々(显示=假),
        区域填充样式选项々=选项.〇区域填充样式选项々(),
        涟漪特效选项々=选项.〇涟漪特效选项々(),
        提示框选项々=空,
        图元样式选项々=空,
    ):
        返回 分身.add(
            系列名称,
            数据,
            is_selected=选中,
            type_=类型_,
            symbol=记号,
            symbol_size=记号大小,
            stack=堆叠,
            label_opts=标签选项々,
            areastyle_opts=区域填充样式选项々,
            effect_opts=涟漪特效选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
        )


_反向注入(〇极坐标系, Polar)