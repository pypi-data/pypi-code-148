从 pyecharts.charts.basic_charts.funnel 导入 Funnel
从 ... 导入 选项
从 汉化通用 导入 _反向注入


类 〇漏斗图(Funnel):
    
    套路 添加(
        分身,
        系列名称,
        数据对,
        *,
        选中=真,
        颜色=空,
        排序_="",
        间隙=0,
        标签选项々=选项.〇标签选项々(),
        提示框选项々=空,
        图元样式选项々=空,
    ):
        如果 排序_ == '降序': 排序_ = 'descending'
        如果 排序_ == '升序': 排序_ = 'ascending'

        返回 分身.add(
            series_name=系列名称,
            data_pair=数据对,
            is_selected=选中,
            color=颜色,
            sort_=排序_,
            gap=间隙,
            label_opts=标签选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
        )

_反向注入(〇漏斗图, Funnel)