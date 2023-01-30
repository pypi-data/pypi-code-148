从 pyecharts.charts.basic_charts.liquid 导入 Liquid
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇水球图(Liquid):
    套路 添加(
        分身,
        系列名称,
        数据,
        *,
        形状="圆",
        颜色=空,
        背景颜色=空,
        显示动画=真,
        显示轮廓=真,
        轮廓边框距离=8,
        轮廓样式=空,
        中心=空,
        提示框选项々=空,
        标签选项々=选项.〇标签选项々(字体大小=50, 位置='内部'),
    ):
        形状字典 = {
            '圆' : 'circle',
            '矩形' : 'rect',
            '圆角矩形' : 'roundRect',
            '三角形' : 'triangle',
            '菱形' : 'diamond',
            '插销' : 'pin',
            '箭头' : 'arrow',
        }
        形状 = 形状字典.获取(形状, 形状)
        
        返回 分身.add(
            系列名称,
            数据,
            shape=形状,
            color=颜色,
            background_color=背景颜色,
            is_animation=显示动画,
            is_outline_show=显示轮廓,
            outline_border_distance=轮廓边框距离,
            outline_itemstyle_opts=轮廓样式,
            center=中心,
            tooltip_opts=提示框选项々,
            label_opts=标签选项々,
        )


_反向注入(〇水球图, Liquid)