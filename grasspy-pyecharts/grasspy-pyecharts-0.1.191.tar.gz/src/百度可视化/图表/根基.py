从 pyecharts.charts.base 导入 Base
从 汉化通用 导入 _反向注入

类 〇根基(Base):
    套路 渲染(分身, 路径='渲染.html', 模板名称='simple_chart.html',
             环境=空, **关键词参数々):
        返回 分身.render(path=路径, template_name=模板名称, env=环境, **关键词参数々)

    套路 渲染到笔记本(分身):
        返回 分身.render_notebook()

    @property
    套路 宽度(分身):
        返回 分身.width

    @宽度.赋值器
    套路 宽度(分身, 值):
        分身.width = 值
    
    @property
    套路 高度(分身):
        返回 分身.height

    @高度.赋值器
    套路 高度(分身, 值):
        分身.height = 值
    
    @property
    套路 渲染器(分身):
        返回 分身.renderer

    @渲染器.赋值器
    套路 渲染器(分身, 值):
        分身.renderer = 值
    
    @property
    套路 网页标题(分身):
        返回 分身.page_title

    @网页标题.赋值器
    套路 网页标题(分身, 值):
        分身.page_title = 值
    
    @property
    套路 主题(分身):
        返回 分身.theme

    @主题.赋值器
    套路 主题(分身, 值):
        分身.theme = 值
    
    @property
    套路 图表id(分身):
        返回 分身.chart_id

    @图表id.赋值器
    套路 图表id(分身, 值):
        分身.chart_id = 值

    
_反向注入(〇根基, Base)