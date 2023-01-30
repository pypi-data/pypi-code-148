从 pyecharts.charts.basic_charts.sunburst 导入 Sunburst
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇旭日图(Sunburst):
    套路 添加(
        分身,
        系列名称,
        数据对,
        *,
        中心=空,
        半径=空,
        高亮策略="descendant",
        节点单击="rootToNode",
        排序_="desc",
        层级=空,
        标签选项々=选项.〇标签选项々(),
        图元样式选项々=空,
    ):
        返回 分身.add(
            系列名称,
            数据对,
            center=中心,
            radius=半径,
            highlight_policy=高亮策略,
            node_click=节点单击,
            sort_=排序_,
            levels=层级,
            label_opts=标签选项々,
            itemstyle_opts=图元样式选项々,
        )


_反向注入(〇旭日图, Sunburst)