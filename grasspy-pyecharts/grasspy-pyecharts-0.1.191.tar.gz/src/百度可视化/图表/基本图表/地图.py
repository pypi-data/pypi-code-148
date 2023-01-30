从 pyecharts.charts.basic_charts.map 导入 MapMixin
从 ..图表 导入 〇图表
从 ... 导入 选项
从 汉化通用 导入 _反向注入

类 〇地图混入(MapMixin):
    套路 添加(
        分身,
        系列名称,
        数据对,
        地图类型='中国',
        *,
        选中=真,
        漫游=真,
        中心=空,
        长宽比=0.75,
        包围坐标=空,
        最小缩放值=空,
        最大缩放值=空,
        名称属性='name',
        选中模式=假,
        缩放=1,
        名称映射=空,
        记号=空,
        地图值计算='sum',
        显示地图记号=真,
        布局中心=空,
        布局大小=空,
        标签选项々=选项.〇标签选项々(),
        提示框选项々=空,
        图元样式选项々=空,
        高亮标签样式々=空,
        高亮图元样式选项々=空,
    ):
        如果 地图类型 == '中国': 地图类型 = 'china'
        
        返回 分身.add(
            series_name=系列名称,
            data_pair=数据对,
            maptype=地图类型,
            is_selected=选中,
            is_roam=漫游,
            center=中心,
            aspect_scale=长宽比,
            bounding_coords=包围坐标,
            min_scale_limit=最小缩放值,
            max_scale_limit=最大缩放值,
            name_property=名称属性,
            selected_mode=选中模式,
            zoom=缩放,
            name_map=名称映射,
            symbol=记号,
            map_value_calculation=地图值计算,
            is_map_symbol_show=显示地图记号,
            layout_center=布局中心,
            layout_size=布局大小,
            label_opts=标签选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
            emphasis_itemstyle_opts=高亮图元样式选项々,
            emphasis_label_opts=高亮标签样式々,
        )


_反向注入(〇地图混入, MapMixin)


类 〇地图(〇图表, 〇地图混入):
    无操作