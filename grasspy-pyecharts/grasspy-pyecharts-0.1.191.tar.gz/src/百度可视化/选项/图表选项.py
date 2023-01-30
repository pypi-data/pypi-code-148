从 pyecharts.options.charts_options 导入 *


class 〇柱状图数据项(BarItem):
    def __init__(
        self,
        名称: Union[int, str],
        值: Numeric,
        *,
        标签选项々: Union[LabelOpts, dict, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "label": 标签选项々,
            "itemStyle": 图元样式选项々,
            "tooltip": 提示框选项々,
        }


class 〇箱形图数据项(BoxplotItem):
    def __init__(
        self,
        名称: Union[int, str],
        值: Sequence,
        *,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "itemStyle": 图元样式选项々,
            "tooltip": 提示框选项々,
        }


class 〇K线图数据项(CandleStickItem):
    def __init__(
        self,
        名称: Union[str, int],
        值: Sequence,
        *,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "itemStyle": 图元样式选项々,
            "tooltip": 提示框选项々,
        }


class 〇涟漪特效散点图数据项(EffectScatterItem):
    def __init__(
        self,
        名称: Union[str, Numeric],
        值: Union[str, Numeric],
        *,
        记号: Optional[str] = None,
        记号大小: Union[Sequence[Numeric], Numeric] = None,
        记号旋转: Optional[Numeric] = None,
        记号保持长宽比: bool = False,
        记号偏移: Optional[Sequence] = None,
        标签选项々: Union[LabelOpts, dict, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "symbol": 记号,
            "symbolSize": 记号大小,
            "symbolRotate": 记号旋转,
            "symbolKeepAspect": 记号保持长宽比,
            "symbolOffset": 记号偏移,
            "label": 标签选项々,
            "itemStyle": 图元样式选项々,
            "tooltip": 提示框选项々,
        }


class 〇漏斗图数据项(FunnelItem):
    def __init__(
        self,
        名称: Union[str, int],
        值: Union[Sequence, str, Numeric],
        *,
        显示标签视觉引导线: Optional[bool] = None,
        标签视觉引导线宽度: Optional[int] = None,
        标签视觉引导线样式选项々: Union[LineStyleOpts, dict, None] = None,
        标签选项々: Union[LabelOpts, dict, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "labelLine": {
                "show": 显示标签视觉引导线,
                "length": 标签视觉引导线宽度,
                "lineStyle": 标签视觉引导线样式选项々,
            },
            "label": 标签选项々,
            "itemStyle": 图元样式选项々,
            "tooltip": 提示框选项々,
        }


class 〇折线图数据项(LineItem):
    def __init__(
        self,
        名称: Union[str, Numeric] = None,
        值: Union[str, Numeric] = None,
        *,
        记号: Optional[str] = "circle",
        记号大小: Numeric = 4,
        记号旋转: Optional[Numeric] = None,
        记号保持长宽比: bool = False,
        记号偏移: Optional[Sequence] = None,
        标签选项々: Union[LabelOpts, dict, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "symbol": 记号,
            "symbolSize": 记号大小,
            "symbolRotate": 记号旋转,
            "symbolKeepAspect": 记号保持长宽比,
            "symbolOffset": 记号偏移,
            "label": 标签选项々,
            "itemStyle": 图元样式选项々,
            "tooltip": 提示框选项々,
        }


class 〇地图数据项(MapItem):
    def __init__(
        self,
        名称: Optional[str] = None,
        值: Union[Sequence, Numeric, str] = None,
        选中: bool = False,
        标签选项々: Union[LabelOpts, dict, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "selected": 选中,
            "label": 标签选项々,
            "itemStyle": 图元样式选项々,
            "tooltip": 提示框选项々,
        }


class 〇饼图数据项(PieItem):
    def __init__(
        self,
        名称: Optional[str] = None,
        值: Optional[Numeric] = None,
        选中: bool = False,
        标签选项々: Union[LabelOpts, dict, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "selected": 选中,
            "label": 标签选项々,
            "itemStyle": 图元样式选项々,
            "tooltip": 提示框选项々,
        }


class 〇雷达图数据项(RadarItem):
    def __init__(
        self,
        名称: Optional[str] = None,
        值: Union[Sequence, Numeric, str] = None,
        记号: Optional[str] = None,
        记号大小: Union[Sequence[Numeric], Numeric] = None,
        记号旋转: Optional[Numeric] = None,
        记号保持长宽比: bool = False,
        记号偏移: Optional[Sequence] = None,
        标签选项々: Union[LabelOpts, dict, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
        线条样式选项々: Union[LineStyleOpts, dict, None] = None,
        区域填充样式选项々: Union[AreaStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "symbol": 记号,
            "symbolSize": 记号大小,
            "symbolRotate": 记号旋转,
            "symbolKeepAspect": 记号保持长宽比,
            "symbolOffset": 记号偏移,
            "label": 标签选项々,
            "itemStyle": 图元样式选项々,
            "tooltip": 提示框选项々,
            "lineStyle": 线条样式选项々,
            "areaStyle": 区域填充样式选项々,
        }


class 〇散点图数据项(ScatterItem):
    def __init__(
        self,
        名称: Union[str, Numeric] = None,
        值: Union[str, Numeric] = None,
        记号: Optional[str] = None,
        记号大小: Union[Sequence[Numeric], Numeric] = None,
        记号旋转: Optional[Numeric] = None,
        记号保持长宽比: bool = False,
        记号偏移: Optional[Sequence] = None,
        标签选项々: Union[LabelOpts, dict, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "symbol": 记号,
            "symbolSize": 记号大小,
            "symbolRotate": 记号旋转,
            "symbolKeepAspect": 记号保持长宽比,
            "symbolOffset": 记号偏移,
            "label": 标签选项々,
            "itemStyle": 图元样式选项々,
            "tooltip": 提示框选项々,
        }


class 〇旭日图数据项(SunburstItem):
    def __init__(
        self,
        值: Optional[Numeric] = None,
        名称: Optional[str] = None,
        链接: Optional[str] = None,
        目标: Optional[str] = "blank",
        标签选项々: Union[LabelOpts, dict, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        子节点々: Optional[Sequence] = None,
    ):
        self.opts: dict = {
            "value": 值,
            "name": 名称,
            "link": 链接,
            "target": 目标,
            "label": 标签选项々,
            "itemStyle": 图元样式选项々,
            "children": 子节点々,
        }


class 〇主题河流图数据项(ThemeRiverItem):
    def __init__(
        self,
        日期: Optional[str] = None,
        值: Optional[Numeric] = None,
        名称: Optional[str] = None,
    ):
        self.opts: dict = {"date": 日期, "value": 值, "name": 名称}


class 〇树图数据项(TreeItem):
    def __init__(
        self,
        名称: Optional[str] = None,
        值: Optional[Numeric] = None,
        标签选项々: Union[LabelOpts, dict, None] = None,
        子节点々: Optional[Sequence] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "value": 值,
            "children": 子节点々,
            "label": 标签选项々,
        }


# Chart Options
class 〇关系图节点(GraphNode):
    def __init__(
        self,
        名称: Optional[str] = None,
        x: Optional[Numeric] = None,
        y: Optional[Numeric] = None,
        固定: bool = False,
        值: Union[str, Sequence, None] = None,
        类目: Optional[int] = None,
        记号: Optional[str] = None,
        记号大小: Union[Numeric, Sequence, None] = None,
        标签选项々: Union[LabelOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "x": x,
            "y": y,
            "fixed": 固定,
            "value": 值,
            "category": 类目,
            "symbol": 记号,
            "symbolSize": 记号大小,
            "label": 标签选项々,
        }


class 〇关系边(GraphLink):
    def __init__(
        self,
        源: Union[str, int, None] = None,
        目标: Union[str, int, None] = None,
        值: Optional[Numeric] = None,
        记号: Union[str, Sequence, None] = None,
        记号大小: Union[Numeric, Sequence, None] = None,
        线条样式选项々: Union[LineStyleOpts, dict, None] = None,
        标签选项々: Union[LabelOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "source": 源,
            "target": 目标,
            "value": 值,
            "symbol": 记号,
            "symbolSize": 记号大小,
            "lineStyle": 线条样式选项々,
            "label": 标签选项々,
        }


class 〇关系图类目(GraphCategory):
    def __init__(
        self,
        名称: Optional[str] = None,
        记号: Optional[str] = None,
        记号大小: Union[Numeric, Sequence, None] = None,
        标签选项々: Union[LabelOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "symbol": 记号,
            "symbolSize": 记号大小,
            "label": 标签选项々,
        }


class BMapNavigationControlOpts(BasicOpts):
    def __init__(
        self,
        position: Numeric = BMapType.ANCHOR_TOP_LEFT,
        offset_width: Numeric = 10,
        offset_height: Numeric = 10,
        type_: Numeric = BMapType.NAVIGATION_CONTROL_LARGE,
        is_show_zoom_info: bool = False,
        is_enable_geo_location: bool = False,
    ):
        bmap_nav_config = json.dumps(
            {
                "anchor": position,
                "offset": {"width": offset_width, "height": offset_height},
                "type": type_,
                "showZoomInfo": is_show_zoom_info,
                "enableGeolocation": is_enable_geo_location,
            }
        )

        self.opts: dict = {
            "functions": [
                "bmap.addControl(new BMap.NavigationControl({}));".format(
                    bmap_nav_config
                )
            ]
        }


class BMapOverviewMapControlOpts(BasicOpts):
    def __init__(
        self,
        position: Numeric = BMapType.ANCHOR_BOTTOM_RIGHT,
        offset_width: Numeric = 10,
        offset_height: Numeric = 50,
        is_open: bool = False,
    ):
        bmap_overview_config = json.dumps(
            {
                "anchor": position,
                "offset": {"width": offset_width, "height": offset_height},
                "isOpen": is_open,
            }
        )

        self.opts: dict = {
            "functions": [
                "var overview = new BMap.OverviewMapControl({});".format(
                    bmap_overview_config
                ),
                "bmap.addControl(overview);",
            ]
        }


class BMapScaleControlOpts(BasicOpts):
    def __init__(
        self,
        position: Numeric = BMapType.ANCHOR_BOTTOM_LEFT,
        offset_width: Numeric = 80,
        offset_height: Numeric = 21,
    ):
        bmap_scale_config = json.dumps(
            {
                "anchor": position,
                "offset": {"width": offset_width, "height": offset_height},
            }
        )

        self.opts: dict = {
            "functions": [
                "bmap.addControl(new BMap.ScaleControl({}));".format(bmap_scale_config)
            ]
        }


class BMapTypeControlOpts(BasicOpts):
    def __init__(
        self,
        position: Numeric = BMapType.ANCHOR_TOP_RIGHT,
        type_: Numeric = BMapType.MAPTYPE_CONTROL_HORIZONTAL,
    ):
        bmap_type_config = json.dumps({"anchor": position, "type": type_})

        self.opts: dict = {
            "functions": [
                "bmap.addControl(new BMap.MapTypeControl({}));".format(bmap_type_config)
            ]
        }


class BMapCopyrightTypeOpts(BasicOpts):
    def __init__(
        self,
        position: Numeric = BMapType.ANCHOR_BOTTOM_LEFT,
        offset_width: Numeric = 2,
        offset_height: Numeric = 2,
        copyright_: str = "",
    ):
        bmap_copyright_config = json.dumps(
            {
                "anchor": position,
                "offset": {"width": offset_width, "height": offset_height},
            }
        )

        bmap_copyright_content_config = json.dumps({"id": 1, "content": copyright_})

        self.opts: dict = {
            "functions": [
                "var copyright = new BMap.CopyrightControl({});".format(
                    bmap_copyright_config
                ),
                "copyright.addCopyright({});".format(bmap_copyright_content_config),
                "bmap.addControl(copyright);",
            ]
        }


class BMapGeoLocationControlOpts(BasicOpts):
    def __init__(
        self,
        position: Numeric = BMapType.ANCHOR_BOTTOM_LEFT,
        offset_width: Numeric = 10,
        offset_height: Numeric = 10,
        is_show_address_bar: bool = True,
        is_enable_auto_location: bool = False,
    ):
        bmap_geo_location_config = json.dumps(
            {
                "anchor": position,
                "offset": {"width": offset_width, "height": offset_height},
                "showAddressBar": is_show_address_bar,
                "enableAutoLocation": is_enable_auto_location,
            }
        )

        self.opts: dict = {
            "functions": [
                "bmap.addControl(new BMap.GeolocationControl({}))".format(
                    bmap_geo_location_config
                )
            ]
        }


class ComponentTitleOpts:
    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
        title_style: Optional[dict] = None,
        subtitle_style: Optional[dict] = None,
    ):
        self.title = title.replace("\n", "<br/>")
        self.subtitle = subtitle.replace("\n", "<br/>")
        self.title_style: str = ""
        self.subtitle_style: str = ""
        title_style = title_style or {"style": "font-size: 18px; font-weight:bold;"}
        subtitle_style = subtitle_style or {"style": "font-size: 12px;"}
        self._convert_dict_to_string(title_style, subtitle_style)

    def _convert_dict_to_string(self, title_style: dict, subtitle_style: dict):
        for k, v in title_style.items():
            self.title_style += '{}="{}" '.format(k, v)
        for k, v in subtitle_style.items():
            self.subtitle_style += '{}="{}" '.format(k, v)


class 〇网页布局选项々(PageLayoutOpts):
    def __init__(
        self,
        左右对齐内容: Optional[str] = None,
        外边距: Optional[str] = None,
        显示: Optional[str] = None,
        弹性盒_换行: Optional[str] = None,
    ):
        self.opts: dict = {
            "justify-content": 左右对齐内容,
            "margin": 外边距,
            "display": 显示,
            "flex-wrap": 弹性盒_换行,
        }


class BaseGraphic(BasicOpts):
    pass


class 〇原生图形形状选项々(GraphicShapeOpts):
    def __init__(
        self,
        x: Numeric = 0,
        y: Numeric = 0,
        宽度: Numeric = 0,
        高度: Numeric = 0,
        r: Union[Sequence, Numeric, None] = None,
    ):
        self.opts: dict = {
            "x": x,
            "y": y,
            "width": 宽度,
            "height": 高度,
            "r": r,
        }


class 〇原生图形基本样式选项々(GraphicBasicStyleOpts):
    def __init__(
        self,
        填充颜色: str = "#000",
        笔画颜色: Optional[str] = None,
        笔画宽度: Numeric = 0,
        阴影长度: Optional[Numeric] = None,
        阴影偏移x: Optional[Numeric] = None,
        阴影偏移y: Optional[Numeric] = None,
        阴影颜色: Optional[str] = None,
    ):
        self.opts: dict = {
            "fill": 填充颜色,
            "stroke": 笔画颜色,
            "line_width": 笔画宽度,
            "shadowBlur": 阴影长度,
            "shadowOffsetX": 阴影偏移x,
            "shadowOffsetY": 阴影偏移y,
            "shadowColor": 阴影颜色,
        }


class 〇原生图形图片样式选项々(GraphicImageStyleOpts):
    def __init__(
        self,
        图片: Optional[str] = None,
        x: Numeric = 0,
        y: Numeric = 0,
        宽度: Numeric = 0,
        高度: Numeric = 0,
        不透明度: Numeric = 1,
        原生图形基本样式选项々: Union[GraphicBasicStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "image": 图片,
            "x": x,
            "y": y,
            "width": 宽度,
            "height": 高度,
            "opacity": 不透明度,
        }

        if 原生图形基本样式选项々:
            if isinstance(原生图形基本样式选项々, GraphicBasicStyleOpts):
                self.opts.update(原生图形基本样式选项々.opts)
            else:
                self.opts.update(原生图形基本样式选项々)


class 〇原生图形文本样式选项々(GraphicTextStyleOpts):
    def __init__(
        self,
        文本: Optional[JSFunc] = None,
        x: Numeric = 0,
        y: Numeric = 0,
        字体: Optional[str] = None,
        文本水平对齐: str = "left",
        文本垂直对齐: Optional[str] = None,
        原生图形基本样式选项々: Union[GraphicBasicStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "text": 文本,
            "x": x,
            "y": y,
            "font": 字体,
            "textAlign": 文本水平对齐,
            "textVerticalAlign": 文本垂直对齐,
        }

        if 原生图形基本样式选项々:
            if isinstance(原生图形基本样式选项々, GraphicBasicStyleOpts):
                self.opts.update(原生图形基本样式选项々.opts)
            else:
                self.opts.update(原生图形基本样式选项々)


class 〇原生图形元素(GraphicItem):
    def __init__(
        self,
        id_: Optional[str] = None,
        操作: str = "merge",
        位置: [Sequence, Numeric, None] = None,
        旋转: Union[Numeric, JSFunc, None] = 0,
        缩放: Union[Sequence, Numeric, None] = None,
        原点: Union[Numeric, Sequence, None] = None,
        左: Union[Numeric, str, None] = None,
        右: Union[Numeric, str, None] = None,
        上: Union[Numeric, str, None] = None,
        下: Union[Numeric, str, None] = None,
        包围: str = "all",
        z: Numeric = 0,
        z层级: Numeric = 0,
        静默: bool = False,
        可见: bool = False,
        忽略: bool = False,
        光标: str = "pointer",
        可拖动: bool = False,
        渐进渲染: bool = False,
        宽度: Numeric = 0,
        高度: Numeric = 0,
    ):
        self.opts: dict = {
            "id": id_,
            "$action": 操作,
            "position": 位置,
            "rotation": 旋转,
            "scale": 缩放,
            "origin": 原点,
            "left": 左,
            "right": 右,
            "top": 上,
            "bottom": 下,
            "bounding": 包围,
            "z": z,
            "zlevel": z层级,
            "silent": 静默,
            "invisible": 可见,
            "ignore": 忽略,
            "cursor": 光标,
            "draggable": 可拖动,
            "progressive": 渐进渲染,
            "width": 宽度,
            "height": 高度,
        }


class 〇原生图形元素组件(GraphicGroup):
    def __init__(
        self,
        原生图形元素: Union[GraphicItem, dict, None] = None,
        根据子节点的名称属性重绘: bool = False,
        子节点々: Optional[Sequence[BaseGraphic]] = None,
    ):
        self.opts: dict = {
            "type": "group",
            "diffChildrenByName": 根据子节点的名称属性重绘,
            "children": 子节点々,
        }

        if 原生图形元素:
            if isinstance(原生图形元素, GraphicItem):
                self.opts.update(原生图形元素.opts)
            else:
                self.opts.update(原生图形元素)


class 〇原生图形图片(GraphicImage):
    def __init__(
        self,
        原生图形元素: Union[GraphicItem, dict, None] = None,
        原生图形图片样式选项々: Union[GraphicImageStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {"type": "image"}

        if 原生图形元素:
            if isinstance(原生图形元素, GraphicItem):
                self.opts.update(原生图形元素.opts)
            else:
                self.opts.update(原生图形元素)

        if 原生图形图片样式选项々:
            if isinstance(原生图形图片样式选项々, GraphicImageStyleOpts):
                self.opts.update(style=原生图形图片样式选项々.opts)
            else:
                self.opts.update(style=原生图形图片样式选项々)


class 〇原生图形文本(GraphicText):
    def __init__(
        self,
        原生图形元素: Union[GraphicItem, dict, None] = None,
        原生图形文本样式选项々: Union[GraphicTextStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {"type": "text"}

        if 原生图形元素:
            if isinstance(原生图形元素, GraphicItem):
                self.opts.update(原生图形元素.opts)
            else:
                self.opts.update(原生图形元素)

        if 原生图形文本样式选项々:
            if isinstance(原生图形文本样式选项々, GraphicTextStyleOpts):
                self.opts.update(style=原生图形文本样式选项々.opts)
            else:
                self.opts.update(style=原生图形文本样式选项々)


class 〇原生图形矩形(GraphicRect):
    def __init__(
        self,
        原生图形元素: Union[GraphicItem, dict, None] = None,
        原生图形形状选项々: Union[GraphicShapeOpts, dict, None] = None,
        原生图形基本样式选项々: Union[GraphicBasicStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {"type": "rect"}

        if 原生图形元素:
            if isinstance(原生图形元素, GraphicItem):
                self.opts.update(原生图形元素.opts)
            else:
                self.opts.update(原生图形元素)

        if 原生图形形状选项々:
            if isinstance(原生图形形状选项々, GraphicShapeOpts):
                self.opts.update(shape=原生图形形状选项々.opts)
            else:
                self.opts.update(原生图形形状选项々)

        if 原生图形基本样式选项々:
            if isinstance(原生图形基本样式选项々, GraphicBasicStyleOpts):
                self.opts.update(style=原生图形基本样式选项々.opts)
            else:
                self.opts.update(style=原生图形基本样式选项々)


class 〇桑基图层级选项々(SankeyLevelsOpts):
    def __init__(
        self,
        深度: Numeric = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
        线条样式选项々: Union[LineStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "depth": 深度,
            "itemStyle": 图元样式选项々,
            "lineStyle": 线条样式选项々,
        }


class 〇矩形树图元素样式选项々(TreeMapItemStyleOpts):
    def __init__(
        self,
        颜色: Optional[str] = None,
        颜色透明度: Union[Numeric, Sequence] = None,
        颜色饱和度: Union[Numeric, Sequence] = None,
        边框颜色: Optional[str] = None,
        边框宽度: Numeric = 0,
        边框颜色饱和度: Union[Numeric, Sequence] = None,
        间隙宽度: Numeric = 0,
        描边颜色: Optional[str] = None,
        描边宽度: Optional[Numeric] = None,
    ):
        self.opts: dict = {
            "color": 颜色,
            "colorAlpha": 颜色透明度,
            "colorSaturation": 颜色饱和度,
            "gapWidth": 间隙宽度,
            "borderColor": 边框颜色,
            "borderWidth": 边框宽度,
            "borderColorSaturation": 边框颜色饱和度,
            "strokeColor": 描边颜色,
            "strokeWidth": 描边宽度,
        }


class 〇矩形树图层级选项々(TreeMapLevelsOpts):
    def __init__(
        self,
        颜色透明度: Union[Numeric, Sequence] = None,
        颜色饱和度: Union[Numeric, Sequence] = None,
        颜色映射依据: str = "index",
        矩形树图元素样式选项々: Union[TreeMapItemStyleOpts, dict, None] = None,
        标签选项々: Union[LabelOpts, dict, None] = None,
        父节点标签选项々: Union[LabelOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "colorAlpha": 颜色透明度,
            "colorSaturation": 颜色饱和度,
            "colorMappingBy": 颜色映射依据,
            "itemStyle": 矩形树图元素样式选项々,
            "label": 标签选项々,
            "upperLabel": 父节点标签选项々,
        }


class 〇三维地图标签选项々(Map3DLabelOpts):
    def __init__(
        self,
        显示: bool = True,
        距离: Numeric = None,
        格式器: Optional[JSFunc] = None,
        文本样式: Union[TextStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "distance": 距离,
            "formatter": 格式器,
            "textStyle": 文本样式,
        }


class Map3DRealisticMaterialOpts(BasicOpts):
    def __init__(
        self,
        detail_texture: Optional[JSFunc] = None,
        texture_tiling: Numeric = 1,
        texture_offset: Numeric = 0,
        roughness: Numeric = 0.5,
        metalness: Numeric = 0,
        roughness_adjust: Numeric = 0.5,
        metalness_adjust: Numeric = 0.5,
        normal_texture: Optional[JSFunc] = None,
    ):
        self.opts: dict = {
            "detailTexture": detail_texture,
            "textureTiling": texture_tiling,
            "textureOffset": texture_offset,
            "roughness": roughness,
            "metalness": metalness,
            "roughnessAdjust": roughness_adjust,
            "metalnessAdjust": metalness_adjust,
            "normalTexture": normal_texture,
        }


class Map3DLambertMaterialOpts(BasicOpts):
    def __init__(
        self,
        detail_texture: Optional[JSFunc] = None,
        texture_tiling: Numeric = 1,
        texture_offset: Numeric = 0,
    ):
        self.opts: dict = {
            "detailTexture": detail_texture,
            "textureTiling": texture_tiling,
            "textureOffset": texture_offset,
        }


class Map3DColorMaterialOpts(BasicOpts):
    def __init__(
        self,
        detail_texture: Optional[JSFunc] = None,
        texture_tiling: Numeric = 1,
        texture_offset: Numeric = 0,
    ):
        self.opts: dict = {
            "detailTexture": detail_texture,
            "textureTiling": texture_tiling,
            "textureOffset": texture_offset,
        }


class Map3DLightOpts(BasicOpts):
    def __init__(
        self,
        main_color: str = "#fff",
        main_intensity: Numeric = 1,
        is_main_shadow: bool = False,
        main_shadow_quality: str = "medium",
        main_alpha: Numeric = 40,
        main_beta: Numeric = 40,
        ambient_color: str = "#fff",
        ambient_intensity: Numeric = 0.2,
        ambient_cubemap_texture: Optional[str] = None,
        ambient_cubemap_diffuse_intensity: Numeric = 0.5,
        ambient_cubemap_specular_intensity: Numeric = 0.5,
    ):
        self.opts: dict = {
            "main": {
                "color": main_color,
                "intensity": main_intensity,
                "shadow": is_main_shadow,
                "shadowQuality": main_shadow_quality,
                "alpha": main_alpha,
                "beta": main_beta,
            },
            "ambient": {"color": ambient_color, "intensity": ambient_intensity},
            "ambientCubemap": {
                "texture": ambient_cubemap_texture,
                "diffuseIntensity": ambient_cubemap_diffuse_intensity,
                "specularIntensity": ambient_cubemap_specular_intensity,
            },
        }


class Map3DPostEffectOpts(BasicOpts):
    def __init__(
        self,
        is_enable: bool = False,
        is_bloom_enable: bool = False,
        bloom_intensity: Numeric = 0.1,
        is_depth_field_enable: bool = False,
        depth_field_focal_distance: Numeric = 50,
        depth_field_focal_range: Numeric = 20,
        depth_field_fstop: Numeric = 2.8,
        depth_field_blur_radius: Numeric = 10,
        is_ssao_enable: bool = False,
        ssao_quality: str = "medium",
        ssao_radius: Numeric = 2,
        ssao_intensity: Numeric = 1,
        is_color_correction_enable: bool = False,
        color_correction_lookup_texture: Optional[JSFunc] = None,
        color_correction_exposure: Numeric = 0,
        color_correction_brightness: Numeric = 0,
        color_correction_contrast: Numeric = 1,
        color_correction_saturation: Numeric = 1,
        is_fxaa_enable: bool = False,
    ):
        self.opts: dict = {
            "enable": is_enable,
            "bloom": {"enable": is_bloom_enable, "bloomIntensity": bloom_intensity},
            "depthOfField": {
                "enable": is_depth_field_enable,
                "focalDistance": depth_field_focal_distance,
                "focalRange": depth_field_focal_range,
                "fstop": depth_field_fstop,
                "blurRadius": depth_field_blur_radius,
            },
            "SSAO": {
                "enable": is_ssao_enable,
                "quality": ssao_quality,
                "radius": ssao_radius,
                "intensity": ssao_intensity,
            },
            "colorCorrection": {
                "enable": is_color_correction_enable,
                "lookupTexture": color_correction_lookup_texture,
                "exposure": color_correction_exposure,
                "brightness": color_correction_brightness,
                "contrast": color_correction_contrast,
                "saturation": color_correction_saturation,
            },
            "FXAA": {"enable": is_fxaa_enable},
        }


class Map3DViewControlOpts(BasicOpts):
    def __init__(
        self,
        projection: str = "perspective",
        auto_rotate: bool = False,
        auto_rotate_direction: str = "cw",
        auto_rotate_speed: Numeric = 10,
        auto_rotate_after_still: Numeric = 3,
        damping: Numeric = 0.8,
        rotate_sensitivity: Union[Numeric, Sequence] = 1,
        zoom_sensitivity: Numeric = 1,
        pan_sensitivity: Numeric = 1,
        pan_mouse_button: str = "left",
        rotate_mouse_button: str = "middle",
        距离: Numeric = 100,
        min_distance: Numeric = 40,
        max_distance: Numeric = 400,
        orthographic_size: Numeric = 100,
        min_orthographic_size: Numeric = 20,
        max_orthographic_size: Numeric = 400,
        alpha: Numeric = 40,
        beta: Numeric = 0,
        center: Optional[Sequence] = None,
        min_alpha: Numeric = 5,
        max_alpha: Numeric = 90,
        min_beta: Numeric = -80,
        max_beta: Numeric = 80,
        animation: bool = True,
        animation_duration_update: Numeric = 1000,
        动画缓入缓出更新: str = "cubicInOut",
    ):
        self.opts: dict = {
            "projection": projection,
            "autoRotate": auto_rotate,
            "autoRotateDirection": auto_rotate_direction,
            "autoRotateSpeed": auto_rotate_speed,
            "autoRotateAfterStill": auto_rotate_after_still,
            "damping": damping,
            "rotateSensitivity": rotate_sensitivity,
            "zoomSensitivity": zoom_sensitivity,
            "panSensitivity": pan_sensitivity,
            "panMouseButton": pan_mouse_button,
            "rotateMouseButton": rotate_mouse_button,
            "distance": 距离,
            "minDistance": min_distance,
            "maxDistance": max_distance,
            "orthographicSize": orthographic_size,
            "minOrthographicSize": min_orthographic_size,
            "maxOrthographicSize": max_orthographic_size,
            "alpha": alpha,
            "beta": beta,
            "center": center,
            "minAlpha": min_alpha,
            "maxAlpha": max_alpha,
            "minBeta": min_beta,
            "maxBeta": max_beta,
            "animation": animation,
            "animationDurationUpdate": animation_duration_update,
            "animationEasingUpdate": 动画缓入缓出更新,
        }


class 〇柱状图背景样式选项々(BarBackgroundStyleOpts):
    def __init__(
        self,
        颜色: str = "rgba(180, 180, 180, 0.2)",
        边框颜色: str = "#000",
        边框宽度: Numeric = 0,
        边框类型: str = "solid",
        柱条边框半径: Union[Numeric, Sequence] = 0,
        阴影长度: Optional[Numeric] = None,
        阴影颜色: Optional[str] = None,
        阴影偏移x: Numeric = 0,
        阴影偏移y: Numeric = 0,
        不透明度: Optional[Numeric] = None,
    ):
        self.opts: dict = {
            "color": 颜色,
            "borderColor": 边框颜色,
            "borderWidth": 边框宽度,
            "borderType": 边框类型,
            "barBorderRadius": 柱条边框半径,
            "shadowBlur": 阴影长度,
            "shadowColor": 阴影颜色,
            "shadowOffsetX": 阴影偏移x,
            "shadowOffsetY": 阴影偏移y,
            "opacity": 不透明度,
        }


class 〇仪表盘数据标题选项々(GaugeTitleOpts):
    def __init__(
        self,
        显示: bool = True,
        相对中心偏移: Sequence = None,
        颜色: str = "#333",
        字体样式: str = "normal",
        字体粗细: str = "normal",
        字体族: str = "sans-serif",
        字体大小: Numeric = 15,
        背景颜色: str = "transparent",
        边框颜色: str = "transparent",
        边框宽度: Numeric = 0,
        边框半径: Numeric = 0,
        内边距: Numeric = 0,
        阴影颜色: Optional[str] = "transparent",
        阴影长度: Optional[Numeric] = 0,
        阴影偏移x: Numeric = 0,
        阴影偏移y: Numeric = 0,
    ):
        if 相对中心偏移 is None:
            相对中心偏移 = [0, "20%"]
        self.opts: dict = {
            "show": 显示,
            "offsetCenter": 相对中心偏移,
            "color": 颜色,
            "fontStyle": 字体样式,
            "fontWeight": 字体粗细,
            "fontFamily": 字体族,
            "fontSize": 字体大小,
            "backgroundColor": 背景颜色,
            "borderColor": 边框颜色,
            "borderWidth": 边框宽度,
            "borderRadius": 边框半径,
            "padding": 内边距,
            "shadowColor": 阴影颜色,
            "shadowBlur": 阴影长度,
            "shadowOffsetX": 阴影偏移x,
            "shadowOffsetY": 阴影偏移y,
        }


class 〇仪表盘数据内容选项々(GaugeDetailOpts):
    def __init__(
        self,
        显示: bool = True,
        背景颜色: str = "transparent",
        边框宽度: Numeric = 0,
        边框颜色: str = "transparent",
        相对中心偏移: Sequence = None,
        格式器: Optional[JSFunc] = None,
        颜色: str = "auto",
        字体样式: str = "normal",
        字体粗细: str = "normal",
        字体族: str = "sans-serif",
        字体大小: Numeric = 15,
        边框半径: Numeric = 0,
        内边距: Numeric = 0,
        阴影颜色: Optional[str] = "transparent",
        阴影长度: Optional[Numeric] = 0,
        阴影偏移x: Numeric = 0,
        阴影偏移y: Numeric = 0,
    ):
        if 相对中心偏移 is None:
            相对中心偏移 = [0, "40%"]
        self.opts: dict = {
            "show": 显示,
            "backgroundColor": 背景颜色,
            "borderWidth": 边框宽度,
            "borderColor": 边框颜色,
            "offsetCenter": 相对中心偏移,
            "formatter": 格式器,
            "color": 颜色,
            "fontStyle": 字体样式,
            "fontWeight": 字体粗细,
            "fontFamily": 字体族,
            "fontSize": 字体大小,
            "borderRadius": 边框半径,
            "padding": 内边距,
            "shadowColor": 阴影颜色,
            "shadowBlur": 阴影长度,
            "shadowOffsetX": 阴影偏移x,
            "shadowOffsetY": 阴影偏移y,
        }


class 〇仪表盘指针选项々(GaugePointerOpts):
    def __init__(
        self,
        显示: bool = True,
        长度: Union[str, Numeric] = "80%",
        宽度: Numeric = 8,
    ):
        self.opts: dict = {"show": 显示, "length": 长度, "width": 宽度}


class 〇饼图标签视觉引导线选项々(PieLabelLineOpts):
    def __init__(
        self,
        显示: bool = True,
        长度: Numeric = None,
        长度2: Numeric = None,
        平滑: Union[bool, Numeric] = False,
        线条样式选项々: Union[LineStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "length": 长度,
            "length2": 长度2,
            "smooth": 平滑,
            "lineStyle": 线条样式选项々,
        }


class 〇时间轴当前项样式(TimelineCheckPointerStyle):
    def __init__(
        self,
        记号: str = "circle",
        记号大小: Union[Numeric, Sequence[Numeric]] = 13,
        记号旋转: Optional[Numeric] = None,
        记号保持长宽比: bool = False,
        记号偏移: Optional[Sequence[Union[str, Numeric]]] = None,
        颜色: str = "#c23531",
        边框宽度: Numeric = 5,
        边框颜色: str = "rgba(194,53,49,0.5)",
        是动画: bool = True,
        动画时长: Numeric = 300,
        动画缓入缓出: str = "quinticInOut",
    ):
        if 记号偏移 is None:
            记号偏移 = [0, 0]

        self.opts: dict = {
            "symbol": 记号,
            "symbolSize": 记号大小,
            "symbolRotate": 记号旋转,
            "symbolKeepAspect": 记号保持长宽比,
            "symbolOffset": 记号偏移,
            "color": 颜色,
            "borderWidth": 边框宽度,
            "borderColor": 边框颜色,
            "animation": 是动画,
            "animationDuration": 动画时长,
            "animationEasing": 动画缓入缓出,
        }


class 〇时间轴控制按钮样式(TimelineControlStyle):
    def __init__(
        self,
        显示: bool = True,
        显示播放按钮: bool = True,
        显示后退按钮: bool = True,
        显示前进按钮: bool = True,
        按钮大小: Numeric = 22,
        按钮间隙: Numeric = 12,
        位置: str = "left",
        播放图标: Optional[str] = None,
        停止图标: Optional[str] = None,
        后退图标: Optional[str] = None,
        前进图标: Optional[str] = None,
        颜色: str = "#304654",
        边框颜色: str = "#304654",
        边框宽度: Numeric = 1,
    ):
        self.opts: dict = {
            "show": 显示,
            "showPlayBtn": 显示播放按钮,
            "showPrevBtn": 显示后退按钮,
            "showNextBtn": 显示前进按钮,
            "itemSize": 按钮大小,
            "itemGap": 按钮间隙,
            "position": 位置,
            "playIcon": 播放图标,
            "stopIcon": 停止图标,
            "prevIcon": 后退图标,
            "nextIcon": 前进图标,
            "color": 颜色,
            "borderColor": 边框颜色,
            "borderWidth": 边框宽度,
        }