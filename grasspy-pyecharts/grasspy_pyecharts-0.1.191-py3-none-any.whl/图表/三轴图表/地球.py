从 pyecharts.charts.chart 导入 Chart3D
从 pyecharts.charts.three_axis_charts.map_globe 导入 MapGlobe
从 ..基本图表.地图 导入 〇地图混入
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇地球(MapGlobe, Chart3D, 〇地图混入):
    套路 添加纲要(分身, 地图类型='中国'):
        如果 地图类型 == '中国': 地图类型 = 'china'
        
        返回 分身.add_schema(maptype=地图类型)

    套路 渲染(
        分身,
        路径="render.html",
        模板名称="simple_globe.html",
        环境=空,
        **关键词参数々
    ):
        返回 分身.render(
            path=路径,
            template_name=模板名称,
            env=环境,
            **关键词参数々,
        )

    套路 渲染到笔记本(分身):
        返回 分身.render_notebook()


# _反向注入(〇地图混入, MapMixin)

