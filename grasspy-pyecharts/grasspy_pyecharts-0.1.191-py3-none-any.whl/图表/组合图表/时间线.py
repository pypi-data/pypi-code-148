从 pyecharts.charts.composite_charts.timeline 导入 Timeline
从 汉化通用 导入 _反向注入
从 ...全局变量 导入 匚坐标轴类型, 匚朝向

类 〇时间线(Timeline):
    """时间线轮播多图"""
    套路 添加纲要(
        分身,
        坐标轴类型=匚坐标轴类型.类目,
        朝向=匚朝向.水平,
        记号=空,
        记号大小=空,
        播放间隔=空,
        控制按钮位置='left',
        自动播放=假,
        循环播放=真,
        反向播放=假,
        显示时间线组件=真,
        反向放置时间线=假,
        位置_左=空,
        位置_右=空,
        位置_上=空,
        位置_下='-5px',
        宽度=空,
        高度=空,
        线条样式选项々=空,
        标签选项々=空,
        图元样式选项々=空,
        原生图形选项々=空,
        当前项样式选项々=空,
        控制按钮样式选项々=空,
    ):
        返回 分身.add_schema(
            axis_type=坐标轴类型,
            orient=朝向,
            symbol=记号,
            symbol_size=记号大小,
            play_interval=播放间隔,
            control_position=控制按钮位置,
            is_auto_play=自动播放,
            is_loop_play=循环播放,
            is_rewind_play=反向播放,
            is_timeline_show=显示时间线组件,
            is_inverse=反向放置时间线,
            pos_left=位置_左,
            pos_right=位置_右,
            pos_top=位置_上,
            pos_bottom=位置_下,
            width=宽度,
            height=高度,
            linestyle_opts=线条样式选项々,
            label_opts=标签选项々,
            itemstyle_opts=图元样式选项々,
            graphic_opts=原生图形选项々,
            checkpointstyle_opts=当前项样式选项々,
            controlstyle_opts=控制按钮样式选项々,
        )

    套路 添加(分身, 图表, 时间点):
        返回 分身.add(图表, 时间点)

_反向注入(〇时间线, Timeline)