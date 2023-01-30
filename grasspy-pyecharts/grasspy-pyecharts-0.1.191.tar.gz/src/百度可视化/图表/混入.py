from pyecharts.charts.mixins import ChartMixin
从 汉化通用 导入 _反向注入

类 〇图表混入(ChartMixin):
    套路 添加js函数(分身, *函数々):
        返回 分身.add_js_funcs(*函数々)

    套路 加载js(分身):
        返回 分身.load_javascript()

_反向注入(〇图表混入, ChartMixin)