从 pyecharts.charts.basic_charts.gauge 导入 Gauge
从 ... 导入 选项
从 汉化通用 导入 _反向注入


类 〇仪表盘(Gauge):
    
    套路 添加(
        分身,
        系列名称,
        数据对,
        *,
        选中=真,
        最小值_=0,
        最大值_=100,
        分段数=10,
        半径="75%",
        起始角度=225,
        结束角度=-45,
        顺时针增长=真,
        标题标签选项々=选项.〇仪表盘数据标题选项々(),
        内容标签选项々=选项.〇仪表盘数据内容选项々(
            格式器="{value}%"
        ),
        指针=选项.〇仪表盘指针选项々(),
        提示框选项々=空,
        坐标轴线选项々=空,
        图元样式选项々=空,
    ):
        返回 分身.add(
            series_name=系列名称,
            data_pair=数据对,
            is_selected=选中,
            min_=最小值_,
            max_=最大值_,
            split_number=分段数,
            radius=半径,
            start_angle=起始角度,
            end_angle=结束角度,
            is_clock_wise=顺时针增长,
            title_label_opts=标题标签选项々,
            detail_label_opts=内容标签选项々,
            pointer=指针,
            tooltip_opts=提示框选项々,
            axisline_opts=坐标轴线选项々,
            itemstyle_opts=图元样式选项々,
        )

_反向注入(〇仪表盘, Gauge)