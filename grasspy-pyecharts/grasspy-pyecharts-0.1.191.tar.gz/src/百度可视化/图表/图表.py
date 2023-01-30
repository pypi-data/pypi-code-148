从 pyecharts.charts.chart 导入 Chart, RectChart, Chart3D, ThreeAxisChart
从 .. 导入 选项
从 汉化通用 导入 _反向注入
从 ..全局变量 导入 匚坐标轴类型


类 〇图表(Chart):
    套路 设置颜色々(分身, 颜色々):
        返回 分身.set_colors(颜色々)

    套路 设置系列选项々(
        分身,
        标签选项々 = 空,
        线条样式选项々 = 空,
        分割线选项々 = 空,
        区域填充样式选项々 = 空,
        坐标轴轴线选项々 = 空,
        标记点选项々 = 空,
        标记线选项々 = 空,
        标记区选项々 = 空,
        涟漪特效选项々 = 空,
        提示框选项々 = 空,
        图元样式选项々 = 空,
        **关键词参数々
    ):
        返回 分身.set_series_opts(
            label_opts=标签选项々,
            linestyle_opts=线条样式选项々,
            splitline_opts=分割线选项々,
            areastyle_opts=区域填充样式选项々,
            axisline_opts=坐标轴轴线选项々,
            markpoint_opts=标记点选项々,
            markline_opts=标记线选项々,
            markarea_opts=标记区选项々,
            effect_opts=涟漪特效选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
            **关键词参数々
        )

    套路 设置全局选项々(
        分身,
        标题选项々=选项.〇标题选项々(),
        图例选项々=选项.〇图例选项々(),
        提示框选项々=空,
        工具箱选项々=空,
        区域选择组件选项々=空,
        x轴选项々=空,
        y轴选项々=空,
        视觉映射选项々=空,
        数据缩放选项々=空,
        原生图形选项々=空,
        坐标轴指示器选项々=空,
    ):
        返回 分身.set_global_opts(
            title_opts=标题选项々,
            legend_opts=图例选项々,
            tooltip_opts=提示框选项々,
            toolbox_opts=工具箱选项々,
            brush_opts=区域选择组件选项々,
            xaxis_opts=x轴选项々,
            yaxis_opts=y轴选项々,
            visualmap_opts=视觉映射选项々,
            datazoom_opts=数据缩放选项々,
            graphic_opts=原生图形选项々,
            axispointer_opts=坐标轴指示器选项々,
        )

    套路 添加数据集(
        分身,
        源=空,
        维度々=空,
        源标题=空
    ):
        返回 分身.add_dataset(source=源, dimensions=维度々, source_header=源标题)

_反向注入(〇图表, Chart)


类 〇直角坐标系图表(RectChart):
    套路 扩展坐标轴(分身, x轴数据=空, x轴=空, y轴=空):
        返回 分身.extend_axis(xaxis_data=x轴数据, xaxis=x轴, yaxis=y轴)

    套路 添加x轴(分身, x轴数据):
        返回 分身.add_xaxis(x轴数据)

    套路 翻转坐标轴(分身):
        返回 分身.reversal_axis()

    套路 叠加(分身, 图表):
        返回 分身.overlap(图表)

_反向注入(〇直角坐标系图表, RectChart)


# 类 〇图表3D(〇图表):


类 〇三轴图表(ThreeAxisChart):
    套路 添加(
        分身,
        系列名称,
        数据,
        着色=空,
        图元样式选项々=空,
        标签选项々=选项.〇标签选项々(显示=假),
        x轴3d选项々=选项.〇三维坐标轴选项々(类型_=匚坐标轴类型.类目),
        y轴3d选项々=选项.〇三维坐标轴选项々(类型_=匚坐标轴类型.类目),
        z轴3d选项々=选项.〇三维坐标轴选项々(类型_=匚坐标轴类型.数值),
        三维栅格选项々=选项.〇三维栅格选项々(),
        编码=空
    ):
        返回 分身.add(
            系列名称,
            数据,
            shading=着色,
            itemstyle_opts=图元样式选项々,
            label_opts=标签选项々,
            xaxis3d_opts=x轴3d选项々,
            yaxis3d_opts=y轴3d选项々,
            zaxis3d_opts=z轴3d选项々,
            grid3d_opts=三维栅格选项々,
            encode=编码
        )

_反向注入(〇三轴图表, ThreeAxisChart)