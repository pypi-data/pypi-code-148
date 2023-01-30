从 pyecharts.charts.basic_charts.effectscatter 导入 EffectScatter
从 ... 导入 选项
从 汉化通用 导入 _反向注入


类 〇涟漪特效散点图(EffectScatter):
    
    套路 添加y轴(
        分身,
        系列名称,
        y轴,
        *,
        选中=真,
        x轴索引=空,
        y轴索引=空,
        颜色=空,
        记号=空,
        记号大小=10,
        记号旋转=空,
        标签选项々=选项.〇标签选项々(),
        涟漪特效选项々=选项.〇涟漪特效选项々(),
        提示框选项々=空,
        图元样式选项々=空,
    ):
        返回 分身.add_yaxis(
            series_name=系列名称,
            y_axis=y轴,
            is_selected=选中,
            xaxis_index=x轴索引,
            yaxis_index=y轴索引,
            color=颜色,
            symbol=记号,
            symbol_size=记号大小,
            symbol_rotate=记号旋转,
            label_opts=标签选项々,
            effect_opts=涟漪特效选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
        )

_反向注入(〇涟漪特效散点图, EffectScatter)