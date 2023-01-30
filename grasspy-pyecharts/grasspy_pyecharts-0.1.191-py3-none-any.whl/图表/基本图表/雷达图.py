从 pyecharts.charts.basic_charts.radar 导入 Radar
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇雷达图(Radar):
    套路 添加纲要(
        分身,
        纲要,
        形状=空,
        中心=空,
        半径=空,
        文本样式选项々=选项.〇文本样式选项々(),
        分割线选项々=选项.〇分割线选项々(显示=真),
        分隔区域选项々=选项.〇分隔区域选项々(),
        坐标轴线选项々=选项.〇坐标轴线选项々(),
        径向轴选项々=空,
        角度轴选项々=空,
        极坐标系选项々=空,
    ):
        返回 分身.add_schema(
            纲要,
            shape=形状,
            center=中心,
            radius=半径,
            textstyle_opts=文本样式选项々,
            splitline_opt=分割线选项々,
            splitarea_opt=分隔区域选项々,
            axisline_opt=坐标轴线选项々,
            radiusaxis_opts=径向轴选项々,
            angleaxis_opts=角度轴选项々,
            polar_opts=极坐标系选项々,
        )

    套路 添加(
        分身,
        系列名称,
        数据,
        *,
        选中=真,
        记号=空,
        颜色=空,
        标签选项々=选项.〇标签选项々(),
        线条样式选项々=选项.〇线条样式选项々(),
        区域填充样式选项々=选项.〇区域填充样式选项々(),
        提示框选项々=空,
    ):
        返回 分身.add(
            系列名称,
            数据,
            is_selected=选中,
            symbol=记号,
            color=颜色,
            label_opts=标签选项々,
            linestyle_opts=线条样式选项々,
            areastyle_opts=区域填充样式选项々,
            tooltip_opts=提示框选项々,
        )


_反向注入(〇雷达图, Radar)