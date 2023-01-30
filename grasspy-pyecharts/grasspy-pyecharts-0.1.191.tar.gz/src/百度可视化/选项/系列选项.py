从 pyecharts.options.series_options 导入 *
从 ..公用 导入 _标签位置字典

class 〇图元样式选项々(ItemStyleOpts):
    def __init__(
        self,
        颜色: Optional[JSFunc] = None,
        颜色0: Optional[str] = None,
        边框颜色: Optional[str] = None,
        边框颜色0: Optional[str] = None,
        边框宽度: Optional[Numeric] = None,
        边框类型: Optional[str] = None,
        不透明度: Optional[Numeric] = None,
        area_color: Optional[str] = None,
    ):
        self.opts: dict = {
            "color": 颜色,
            "color0": 颜色0,
            "borderColor": 边框颜色,
            "borderColor0": 边框颜色0,
            "borderWidth": 边框宽度,
            "borderType": 边框类型,
            "opacity": 不透明度,
            "areaColor": area_color,
        }


class 〇文本样式选项々(TextStyleOpts):
    def __init__(
        self,
        颜色: Optional[str] = None,
        字体样式: Optional[str] = None,
        字体粗细: Optional[str] = None,
        字体族: Optional[str] = None,
        字体大小: Optional[Numeric] = None,
        align: Optional[str] = None,
        垂直对齐: Optional[str] = None,
        line_height: Optional[str] = None,
        背景颜色: Optional[str] = None,
        边框颜色: Optional[str] = None,
        边框宽度: Optional[Numeric] = None,
        边框半径: Union[Numeric, Sequence, None] = None,
        padding: Union[Numeric, Sequence, None] = None,
        shadow_color: Optional[str] = None,
        shadow_blur: Optional[Numeric] = None,
        宽度: Optional[str] = None,
        高度: Optional[str] = None,
        富文本: Optional[dict] = None,
    ):
        self.opts: dict = {
            "color": 颜色,
            "fontStyle": 字体样式,
            "fontWeight": 字体粗细,
            "fontFamily": 字体族,
            "fontSize": 字体大小,
            "align": align,
            "verticalAlign": 垂直对齐,
            "lineHeight": line_height,
            "backgroundColor": 背景颜色,
            "borderColor": 边框颜色,
            "borderWidth": 边框宽度,
            "borderRadius": 边框半径,
            "padding": padding,
            "shadowColor": shadow_color,
            "shadowBlur": shadow_blur,
            "width": 宽度,
            "height": 高度,
            "rich": 富文本,
        }


class 〇标签选项々(LabelOpts):
    def __init__(
        self,
        显示: bool = True,
        位置: Union[str, Sequence] = "上",
        颜色: Optional[str] = None,
        距离: Union[Numeric, Sequence, None] = None,
        字体大小: Optional[Numeric] = None,
        字体样式: Optional[str] = None,
        字体粗细: Optional[str] = None,
        字体族: Optional[str] = None,
        旋转: Optional[Numeric] = None,
        外边距: Optional[Numeric] = 8,
        间隔: Union[Numeric, str, None] = None,
        水平对齐: Optional[str] = None,
        垂直对齐: Optional[str] = None,
        格式器: Optional[JSFunc] = None,
        背景颜色: Optional[str] = None,
        边框颜色: Optional[str] = None,
        边框宽度: Optional[Numeric] = None,
        边框半径: Optional[Numeric] = None,
        富文本: Optional[dict] = None,
    ):
        位置 = _标签位置字典.获取(位置, 位置)  # 根据示例，还有 outside, center, middle 等选项？

        如果 是实例(格式器, 字符串型):
            格式器 = 格式器.替换('{值}', '{value}')

        self.opts: dict = {
            "show": 显示,
            "position": 位置,
            "color": 颜色,
            "distance": 距离,
            "rotate": 旋转,
            "margin": 外边距,
            "interval": 间隔,
            "fontSize": 字体大小,
            "fontStyle": 字体样式,
            "fontWeight": 字体粗细,
            "fontFamily": 字体族,
            "align": 水平对齐,
            "verticalAlign": 垂直对齐,
            "formatter": 格式器,
            "backgroundColor": 背景颜色,
            "borderColor": 边框颜色,
            "borderWidth": 边框宽度,
            "borderRadius": 边框半径,
            "rich": 富文本,
        }


class 〇线条样式选项々(LineStyleOpts):
    def __init__(
        self,
        显示: bool = True,
        宽度: Numeric = 1,
        不透明度: Numeric = 1,
        弯曲度: Numeric = 0,
        类型_: str = "solid",
        颜色: Union[str, Sequence, None] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "width": 宽度,
            "opacity": 不透明度,
            "curveness": 弯曲度,
            "type": 类型_,
            "color": 颜色,
        }


class 〇分割线选项々(SplitLineOpts):
    def __init__(
        self, 显示: bool = False, 线条样式选项々: LineStyleOpts = LineStyleOpts()
    ):
        self.opts: dict = {"show": 显示, "lineStyle": 线条样式选项々}


class 〇标记点数据项(MarkPointItem):
    def __init__(
        self,
        名称: Optional[str] = None,
        类型_: Optional[str] = None,
        值索引: Optional[Numeric] = None,
        值维度: Optional[str] = None,
        坐标: Optional[Sequence] = None,
        x: Optional[Numeric] = None,
        y: Optional[Numeric] = None,
        值: Optional[Numeric] = None,
        记号: Optional[str] = None,
        记号大小: Union[Numeric, Sequence, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "type": 类型_,
            "valueIndex": 值索引,
            "valueDim": 值维度,
            "coord": 坐标,
            "x": x,
            "y": y,
            "value": 值,
            "symbol": 记号,
            "symbolSize": 记号大小,
            "itemStyle": 图元样式选项々,
        }


class 〇标记点选项々(MarkPointOpts):
    def __init__(
        self,
        数据: Sequence[Union[MarkPointItem, dict]] = None,
        记号: Optional[str] = None,
        记号大小: Union[None, Numeric] = None,
        标签选项々: LabelOpts = LabelOpts(position="inside", color="#fff"),
    ):
        self.opts: dict = {
            "symbol": 记号,
            "symbolSize": 记号大小,
            "label": 标签选项々,
            "data": 数据,
        }


class 〇标记线数据项(MarkLineItem):
    def __init__(
        self,
        名称: Optional[str] = None,
        类型_: Optional[str] = None,
        x: Union[str, Numeric, None] = None,
        x坐标: Union[str, Numeric, None] = None,
        y: Union[str, Numeric, None] = None,
        y坐标: Union[str, Numeric, None] = None,
        值索引: Optional[Numeric] = None,
        值维度: Optional[str] = None,
        坐标: Optional[Sequence] = None,
        记号: Optional[str] = None,
        记号大小: Optional[Numeric] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "type": 类型_,
            "valueIndex": 值索引,
            "valueDim": 值维度,
            "xAxis": x,
            "x": x坐标,
            "yAxis": y,
            "y": y坐标,
            "coord": 坐标,
            "symbol": 记号,
            "symbolSize": 记号大小,
        }


class 〇标记线选项々(MarkLineOpts):
    def __init__(
        self,
        静默: bool = False,
        数据: Sequence[Union[MarkLineItem, dict]] = None,
        记号: Optional[str] = None,
        记号大小: Union[None, Numeric] = None,
        精度: int = 2,
        标签选项々: LabelOpts = LabelOpts(),
        线条样式选项々: Union[LineStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "silent": 静默,
            "symbol": 记号,
            "symbolSize": 记号大小,
            "precision": 精度,
            "label": 标签选项々,
            "lineStyle": 线条样式选项々,
            "data": 数据,
        }


class 〇标记区数据项(MarkAreaItem):
    def __init__(
        self,
        名称: Optional[str] = None,
        类型_: Tuple[Optional[str], Optional[str]] = (None, None),
        值索引: Tuple[Optional[Numeric], Optional[Numeric]] = (None, None),
        值维度: Tuple[Optional[str], Optional[str]] = (None, None),
        x: Tuple[Union[str, Numeric, None], Union[str, Numeric, None]] = (None, None),
        y: Tuple[Union[str, Numeric, None], Union[str, Numeric, None]] = (None, None),
        标签选项々: Union[LabelOpts, dict, None] = None,
        图元样式选项々: Union[ItemStyleOpts, dict, None] = None,
    ):
        self.opts: Sequence = [
            {
                "name": 名称,
                "type": 类型_[0],
                "valueIndex": 值索引[0],
                "valueDim": 值维度[0],
                "xAxis": x[0],
                "yAxis": y[0],
                "label": 标签选项々,
                "itemStyle": 图元样式选项々,
            },
            {
                "type": 类型_[1],
                "valueIndex": 值索引[1],
                "valueDim": 值维度[1],
                "xAxis": x[1],
                "yAxis": y[1],
            },
        ]


class 〇标记区选项々(MarkAreaOpts):
    def __init__(
        self,
        静默: bool = False,
        标签选项々: LabelOpts = LabelOpts(),
        数据: Sequence[Union[MarkAreaItem, Sequence, dict]] = None,
        图元样式选项々: ItemStyleOpts = None,
    ):
        self.opts: dict = {
            "silent": 静默,
            "label": 标签选项々,
            "data": 数据,
            "itemStyle": 图元样式选项々,
        }


class 〇涟漪特效选项々(EffectOpts):
    def __init__(
        self,
        显示: bool = True,
        brush_type: str = "stroke",
        scale: Numeric = 2.5,
        period: Numeric = 4,
        颜色: Optional[str] = None,
        记号: Optional[str] = None,
        记号大小: Optional[Numeric] = None,
        trail_length: Optional[Numeric] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "brushType": brush_type,
            "scale": scale,
            "period": period,
            "color": 颜色,
            "symbol": 记号,
            "symbolSize": 记号大小,
            "trailLength": trail_length,
        }


class 〇三维线样式选项々(Lines3DEffectOpts):
    def __init__(
        self,
        显示: bool = True,
        period: Numeric = 4,
        constant_speed: Optional[Numeric] = None,
        trail_width: Numeric = 4,
        trail_length: Numeric = 0.1,
        trail_color: Optional[str] = None,
        trail_opacity: Optional[Numeric] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "period": period,
            "constantSpeed": constant_speed,
            "trailWidth": trail_width,
            "trailLength": trail_length,
            "trailColor": trail_color,
            "trailOpacity": trail_opacity,
        }


class 〇区域填充样式选项々(AreaStyleOpts):
    def __init__(self, 不透明度: Optional[Numeric] = 0, 颜色: Optional[str] = None):
        self.opts: dict = {"opacity": 不透明度, "color": 颜色}


class 〇分隔区域选项々(SplitAreaOpts):
    def __init__(self, 显示=True, 区域填充样式选项々: AreaStyleOpts = AreaStyleOpts()):
        self.opts: dict = {"show": 显示, "areaStyle": 区域填充样式选项々}


class 〇矩形树图面包屑选项々(TreeMapBreadcrumbOpts):
    def __init__(
        self,
        显示: bool = True,
        pos_left: Union[str, Numeric] = "center",
        pos_right: Union[str, Numeric] = "auto",
        pos_top: Union[str, Numeric] = "auto",
        pos_bottom: Union[str, Numeric] = 0,
        高度: Numeric = 22,
        empty_item_width: Numeric = 25,
        item_opts: ItemStyleOpts = ItemStyleOpts(),
    ):
        self.opts: dict = {
            "show": 显示,
            "left": pos_left,
            "right": pos_right,
            "top": pos_top,
            "bottom": pos_bottom,
            "height": 高度,
            "emptyItemWidth": empty_item_width,
            "itemStyle": item_opts,
        }


class 〇次级刻度选项々(MinorTickOpts):
    def __init__(
        self,
        显示: bool = False,
        split_number: Numeric = 5,
        长度: Numeric = 3,
        线条样式选项々: Union[LineStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "splitNumber": split_number,
            "length": 长度,
            "lineStyle": 线条样式选项々,
        }


class 〇次级分割线选项々(MinorSplitLineOpts):
    def __init__(
        self,
        显示: bool = False,
        宽度: Numeric = 1,
        类型_: str = "solid",
        不透明度: Union[Numeric, None] = None,
        线条样式选项々: Union[LineStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "width": 宽度,
            "type": 类型_,
            "opacity": 不透明度,
            "lineStyle": 线条样式选项々,
        }
