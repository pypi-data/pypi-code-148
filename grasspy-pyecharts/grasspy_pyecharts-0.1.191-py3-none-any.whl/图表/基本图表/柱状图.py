从 pyecharts.charts.basic_charts.bar 导入 Bar
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇柱状图(Bar):
    套路 添加y轴(
        分身,
        系列名称,
        y轴,
        *,
        选中=真,
        x轴索引=空,
        y轴索引=空,
        启用图例悬停时的联动高亮=真,
        颜色=空,
        显示背景=假,
        背景样式=空,
        堆叠=空,
        柱条宽度=空,
        柱条最大宽度=空,
        柱条最小宽度=空,
        柱条最小高度=0,
        类目间隙="20%",
        间隙="30%",
        大数据量优化=假,
        大数据量优化阈值=400,
        维度々=空,
        系列排布 = "column",
        数据集索引=0,
        裁剪=真,
        z层级=0,
        z=2,
        标签选项々=选项.〇标签选项々(),
        标记点选项々=空,
        标记线选项々=空,
        提示框选项々=空,
        图元样式选项々=空,
        编码=空,
    ):
        如果 是实例(y轴, 列表型):
            取 数据项 于 y轴:
                如果 是实例(数据项, 字典型):
                    如果 '值' 在 数据项:
                        数据项['value'] = 数据项.弹出('值')
                        
        返回 分身.add_yaxis(
            series_name=系列名称,
            y_axis=y轴,
            is_selected=选中,
            xaxis_index=x轴索引,
            yaxis_index=y轴索引,
            is_legend_hover_link=启用图例悬停时的联动高亮,
            color=颜色,
            is_show_background=显示背景,
            background_style=背景样式,
            stack=堆叠,
            bar_width=柱条宽度,
            bar_max_width=柱条最大宽度,
            bar_min_width=柱条最小宽度,
            bar_min_height=柱条最小高度,
            category_gap=类目间隙,
            gap=间隙,
            is_large=大数据量优化,
            large_threshold=大数据量优化阈值,
            dimensions=维度々,
            series_layout_by=系列排布,
            dataset_index=数据集索引,
            is_clip=裁剪,
            z_level=z层级,
            z=z,
            label_opts=标签选项々,
            markpoint_opts=标记点选项々,
            markline_opts=标记线选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
            encode=编码,
        )

_反向注入(〇柱状图, Bar)