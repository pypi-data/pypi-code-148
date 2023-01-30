从 pyecharts.charts.basic_charts.geo 导入 GeoChartBase, Geo
从 ... 导入 选项
从 ...全局变量 导入 匚图表类型
从 汉化通用 导入 _反向注入

类 〇地理坐标根基(GeoChartBase):

    套路 添加坐标(分身, 名称, 经度, 纬度):
        返回 分身.add_coordinate(名称, 经度, 纬度)
    
    套路 添加坐标_json(分身, json文件):
        返回 分身.add_coordinate_json(json文件)
    
    套路 获取坐标(分身, 名称):
        返回 分身.get_coordinate(名称)

    套路 添加(
        分身,
        系列名称,
        数据对,
        类型_=匚图表类型.散点图,
        *,
        选中=真,
        记号=空,
        记号大小=12,
        模糊大小=20,
        点大小=20,
        颜色=空,
        多段线=假,
        大规模线图优化=假,
        大规模线图优化阈值=2000,
        渐进式渲染图形数=400,
        渐进式渲染图形数阈值=3000,
        标签选项々=选项.〇标签选项々(),
        涟漪特效选项々=选项.〇涟漪特效选项々(),
        线条样式选项々=选项.〇线条样式选项々(),
        提示框选项々=空,
        图元样式选项々=空,
        渲染图元=空,
        编码=空,

    ):
        返回 分身.add(
            series_name=系列名称,
            data_pair=数据对,
            type_=类型_,
            is_selected=选中,
            symbol=记号,
            symbol_size=记号大小,
            blur_size=模糊大小,
            point_size=点大小,
            color=颜色,
            is_polyline=多段线,
            is_large=大规模线图优化,
            large_threshold=大规模线图优化阈值,
            progressive=渐进式渲染图形数,
            progressive_threshold=渐进式渲染图形数阈值,
            label_opts=标签选项々,
            effect_opts=涟漪特效选项々,
            linestyle_opts=线条样式选项々,
            tooltip_opts=提示框选项々,
            itemstyle_opts=图元样式选项々,
            render_item=渲染图元,
            encode=编码,
        )

_反向注入(〇地理坐标根基, GeoChartBase)


类 〇地理坐标(Geo):
    
    套路 添加纲要(
        分身,
        地图类型='中国',
        漫游=真,
        缩放=空,
        中心=空,
        长宽比=0.75,
        包围坐标=空,
        最小缩放值=空,
        最大缩放值=空,
        名称属性='name',
        选中模式=假,
        布局中心=空,
        布局大小=空,
        标签选项々=空,
        图元样式选项々=空,
        高亮图元样式选项々=空,
        高亮标签样式々=空,
    ):
        如果 地图类型 == '中国': 地图类型 = 'china'
        
        返回 分身.add_schema(
            maptype=地图类型,
            is_roam=漫游,
            zoom=缩放,
            center=中心,
            aspect_scale=长宽比,
            bounding_coords=包围坐标,
            min_scale_limit=最小缩放值,
            max_scale_limit=最大缩放值,
            name_property=名称属性,
            selected_mode=选中模式,
            layout_center=布局中心,
            layout_size=布局大小,
            label_opts=标签选项々,
            itemstyle_opts=图元样式选项々,
            emphasis_itemstyle_opts=高亮图元样式选项々,
            emphasis_label_opts=高亮标签样式々,
        )

_反向注入(〇地理坐标, Geo)