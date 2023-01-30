从 pyecharts.charts.basic_charts.graph 导入 Graph
从 ... 导入 选项
从 汉化通用 导入 _反向注入


类 〇关系图(Graph):
    
    套路 添加(
        分身,
        系列名称,
        节点々,
        链接々,
        类目々=空,
        *,
        选中=真,
        响应鼠标突出显示节点=真,
        漫游=真,
        可拖动=假,
        旋转标签=假,
        布局="force",
        记号=空,
        记号大小=10,
        边长=50,
        引力因子=0.2,
        斥力因子=50,
        边标签=空,
        边记号=空,
        边记号大小=10,
        标签选项々=选项.〇标签选项々(),
        线条样式选项々=选项.〇线条样式选项々(),
        提示框选项々=空,
        图元样式选项々=空,
    ):
        返回 分身.add(
            series_name=系列名称,
            nodes=节点々,
            links=链接々,
            categories=类目々,
            is_selected=选中,
            is_focusnode=响应鼠标突出显示节点,
            is_roam=漫游,
            is_draggable=可拖动,
            layout=布局,
            symbol=记号,
            symbol_size=记号大小,
            edge_length=边长,
            gravity=引力因子,
            repulsion=斥力因子,
            edge_label=边标签,
            edge_symbol=边记号,
            edge_symbol_size=边记号大小,
            label_opts=标签选项々,
            linestyle_opts=线条样式选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
        )

_反向注入(〇关系图, Graph)