从 ..全局变量 导入 匚渲染类型, 匚主题类型, 匚朝向
从 ..公用 导入 _上下位置字典, _左右位置字典
从 pyecharts.options.global_options 导入 *


类 〇动画选项々(AnimationOpts):
    套路 __init__(
        分身,
        动画=真,
        动画阈值=2000,
        动画时长=1000,
        动画缓入缓出="cubicOut",
        动画延迟=0,
        动画时长更新=300,
        动画缓入缓出更新="cubicOut",
        动画延迟更新=0
    ):
        分身.opts = {
            "animation": 动画,
            "animationThreshold": 动画阈值,
            "animationDuration": 动画时长,
            "animationEasing": 动画缓入缓出,
            "animationDelay": 动画延迟,
            "animationDurationUpdate": 动画时长更新,
            "animationEasingUpdate": 动画缓入缓出更新,
            "animationDelayUpdate": 动画延迟更新,
        }


类 〇初始化选项々(InitOpts):
    套路 __init__(
        分身,
        宽度="900px",
        高度="500px",
        图表id=空,
        渲染器=匚渲染类型.画布,
        网页标题='百度图表顶呱呱',
        主题=匚主题类型.白色,
        背景颜色=空,
        js主机="",
        动画选项々=〇动画选项々()
    ):
        分身.opts = {
            "width": 宽度,
            "height": 高度,
            "chart_id": 图表id,
            "renderer": 渲染器,
            "page_title": 网页标题,
            "theme": 主题,
            "bg_color": 背景颜色,
            "js_host": js主机,
            "animationOpts": 动画选项々,
        }


类 〇工具箱保存图片选项々(ToolBoxFeatureSaveAsImageOpts):
    套路 __init__(
        分身,
        类型_: str = "png",
        名称: Optional[str] = None,
        背景颜色: str = "auto",
        联动背景颜色: str = "#fff",
        排除组件々: Optional[Sequence[str]] = None,
        显示: bool = True,
        提示语: str = "保存为图片",
        图标: Optional[JSFunc] = None,
        像素比: Numeric = 1,
    ):
        分身.opts = {
            "type": 类型_,
            "name": 名称,
            "backgroundColor": 背景颜色,
            "connectedBackgroundColor": 联动背景颜色,
            "excludeComponents": 排除组件々,
            "show": 显示,
            "title": 提示语,
            "icon": 图标,
            "pixelRatio": 像素比,
        }


class 〇工具箱还原选项々(ToolBoxFeatureRestoreOpts):
    def __init__(
        self, 显示: bool = True, 提示语: str = "还原", 图标: Optional[JSFunc] = None
    ):
        self.opts: dict = {"show": 显示, "title": 提示语, "icon": 图标}


class 〇工具箱数据视图选项々(ToolBoxFeatureDataViewOpts):
    def __init__(
        self,
        显示: bool = True,
        提示语: str = "数据视图",
        图标: Optional[JSFunc] = None,
        只读: bool = False,
        选项转内容: Optional[JSFunc] = None,
        内容转选项: Optional[JSFunc] = None,
        话术: Optional[Sequence[str]] = None,
        背景颜色: str = "#fff",
        文本域颜色: str = "#fff",
        文本域边框颜色: str = "#333",
        文本颜色: str = "#000",
        按钮颜色: str = "#c23531",
        按钮文本颜色: str = "#fff",
    ):
        if 话术 is None:
            话术 = ["数据视图", "关闭", "刷新"]

        self.opts: dict = {
            "show": 显示,
            "title": 提示语,
            "icon": 图标,
            "readOnly": 只读,
            "optionToContent": 选项转内容,
            "contentToOption": 内容转选项,
            "lang": 话术,
            "backgroundColor": 背景颜色,
            "textareaColor": 文本域颜色,
            "textareaBorderColor": 文本域边框颜色,
            "textColor": 文本颜色,
            "buttonColor": 按钮颜色,
            "buttonTextColor": 按钮文本颜色,
        }


class 〇工具箱数据缩放选项々(ToolBoxFeatureDataZoomOpts):
    def __init__(
        self,
        显示: bool = True,
        缩放提示语: str = "数据缩放",
        还原提示语: str = "数据缩放还原",
        缩放图标: Optional[JSFunc] = None,
        还原图标: Optional[JSFunc] = None,
        x轴索引: Union[Numeric, Sequence, bool] = False,
        y轴索引: Union[Numeric, Sequence, bool] = False,
        过滤模式: str = "过滤",
    ):
        过滤模式字典 = {
            "过滤" : "filter",
            "弱过滤" : "weakFilter",
            "空" : "empty",
            "无" : "none",
        }
        过滤模式 = 过滤模式字典.获取(过滤模式, 过滤模式)

        self.opts: dict = {
            "show": 显示,
            "title": {"zoom": 缩放提示语, "back": 还原提示语},
            "icon": {"zoom": 缩放图标, "back": 还原图标},
            "xAxisIndex": x轴索引,
            "yAxisIndex": y轴索引,
            "filterMode": 过滤模式,
        }


class 〇工具箱动态类型切换选项々(ToolBoxFeatureMagicTypeOpts):
    def __init__(
        self,
        显示: bool = True,
        类型_: Optional[Sequence] = None,
        折线图提示语: str = "切换为折线图",
        柱状图提示语: str = "切换为柱状图",
        堆叠提示语: str = "切换为堆叠",
        平铺提示语: str = "切换为平铺",
        折线图图标: Optional[JSFunc] = None,
        柱状图图标: Optional[JSFunc] = None,
        堆叠图标: Optional[JSFunc] = None,
        平铺图标: Optional[JSFunc] = None,
    ):
        if 类型_ is None:
            类型_ = ["line", "bar", "stack", "tiled"]

        self.opts: dict = {
            "show": 显示,
            "type": 类型_,
            "title": {
                "line": 折线图提示语,
                "bar": 柱状图提示语,
                "stack": 堆叠提示语,
                "tiled": 平铺提示语,
            },
            "icon": {
                "line": 折线图图标,
                "bar": 柱状图图标,
                "stack": 堆叠图标,
                "tiled": 平铺图标,
            },
        }


class 〇工具箱区域选择组件选项々(ToolBoxFeatureBrushOpts):
    def __init__(
        self,
        类型_: Optional[str] = None,
        矩形选择图标: Optional[JSFunc] = None,
        圈选图标: Optional[JSFunc] = None,
        横向选择图标: Optional[JSFunc] = None,
        纵向选择图标: Optional[JSFunc] = None,
        保持选择图标: Optional[JSFunc] = None,
        清除选择图标: Optional[JSFunc] = None,
        矩形选择提示语: str = "矩形选择",
        圈选提示语: str = "圈选",
        横向选择提示语: str = "横向选择",
        纵向选择提示语: str = "纵向选择",
        保持选择提示语: str = "保持选择",
        清除选择提示语: str = "清除选择",
    ):
        类型字典 = {
            '矩形' : 'rect',
            '圈选' : 'polygon',
            '横向' : 'lineX',
            '纵向' : 'lineY',
            '保持' : 'keep',
            '清除' : 'clear',
        }
        类型_ = 类型字典.获取(类型_, 类型_)

        self.opts: dict = {
            "type": 类型_,
            "icon": {
                "rect": 矩形选择图标,
                "polygon": 圈选图标,
                "lineX": 横向选择图标,
                "lineY": 纵向选择图标,
                "keep": 保持选择图标,
                "clear": 清除选择图标,
            },
            "title": {
                "rect": 矩形选择提示语,
                "polygon": 圈选提示语,
                "lineX": 横向选择提示语,
                "lineY": 纵向选择提示语,
                "keep": 保持选择提示语,
                "clear": 清除选择提示语,
            },
        }


class 〇工具箱工具选项々(ToolBoxFeatureOpts):
    def __init__(
        self,
        保存为图片: Union[
            ToolBoxFeatureSaveAsImageOpts, dict
        ] = 〇工具箱保存图片选项々(),
        还原: Union[ToolBoxFeatureRestoreOpts, dict] = 〇工具箱还原选项々(),
        数据视图: Union[
            ToolBoxFeatureDataViewOpts, dict
        ] = 〇工具箱数据视图选项々(),
        数据缩放: Union[
            ToolBoxFeatureDataZoomOpts, dict
        ] = 〇工具箱数据缩放选项々(),
        动态类型切换: Union[
            ToolBoxFeatureMagicTypeOpts, dict
        ] = 〇工具箱动态类型切换选项々(),
        区域选择组件: Union[ToolBoxFeatureBrushOpts, dict] = 〇工具箱区域选择组件选项々(),
    ):
        self.opts: dict = {
            "saveAsImage": 保存为图片,
            "restore": 还原,
            "dataView": 数据视图,
            "dataZoom": 数据缩放,
            "magicType": 动态类型切换,
            "brush": 区域选择组件,
        }


class 〇工具箱选项々(ToolboxOpts):
    def __init__(
        self,
        显示: bool = True,
        朝向: str = 匚朝向.水平,
        项目大小: Numeric = 15,
        项目间隙: Numeric = 10,
        位置_左: str = "80%",
        位置_右: Optional[str] = None,
        位置_上: Optional[str] = None,
        位置_下: Optional[str] = None,
        工具配置: Union[ToolBoxFeatureOpts, dict] = 〇工具箱工具选项々(),
    ):
        位置_左 = _左右位置字典.获取(位置_左, 位置_左)
        位置_右 = _左右位置字典.获取(位置_右, 位置_右)
        位置_上 = _上下位置字典.获取(位置_上, 位置_上)
        位置_下 = _上下位置字典.获取(位置_下, 位置_下)

        self.opts: dict = {
            "show": 显示,
            "orient": 朝向,
            "itemSize": 项目大小,
            "itemGap": 项目间隙,
            "left": 位置_左,
            "right": 位置_右,
            "top": 位置_上,
            "bottom": 位置_下,
            "feature": 工具配置,
        }


class 〇区域选择组件选项々(BrushOpts):
    def __init__(
        self,
        工具箱按钮: Optional[Sequence] = None,
        区域选择联动: Union[Sequence, str] = None,
        系列索引: Union[Sequence, Numeric, str] = None,
        地理索引: Union[Sequence, Numeric, str] = None,
        x轴索引: Union[Sequence, Numeric, str] = None,
        y轴索引: Union[Sequence, Numeric, str] = None,
        区域选择类型: str = "矩形",
        区域选择模式: str = "单选",
        可变形或平移: bool = True,
        区域选择样式: Optional[dict] = None,
        限频类型: str = "固定频率",
        限频延迟: Numeric = 0,
        单击移除: bool = True,
        选中区域外视觉: dict = None,
    ):
        如果 区域选择联动 == '全部': 区域选择联动 = 'all'
        如果 系列索引 == '全部': 系列索引 = 'all'
        如果 地理索引 == '全部': 地理索引 = 'all'
        如果 x轴索引 == '全部': x轴索引 = 'all'
        如果 y轴索引 == '全部': y轴索引 = 'all'

        区域选择类型字典 = {
            '矩形' : 'rect',
            '圈选' : 'polygon',
            '横向' : 'lineX',
            '纵向' : 'lineY',
        }
        区域选择类型 = 区域选择类型字典.获取(区域选择类型, 区域选择类型)

        如果 区域选择模式 == '单选': 区域选择模式 = 'single'
        如果 区域选择模式 == '多选': 区域选择模式 = 'multiple'

        如果 限频类型 == '固定频率': 限频类型 = 'fixRate'
        如果 限频类型 == '去抖': 限频类型 = 'debounce'

        if 工具箱按钮 is None:
            工具箱按钮 = ["rect", "polygon", "keep", "clear"]

        if 区域选择样式 is None:
            区域选择样式 = {
                "borderWidth": 1,
                "color": "rgba(120,140,180,0.3)",
                "borderColor": "rgba(120,140,180,0.8)",
            }

        self.opts: dict = {
            "toolbox": 工具箱按钮,
            "brushLink": 区域选择联动,
            "seriesIndex": 系列索引,
            "geoIndex": 地理索引,
            "xAxisIndex": x轴索引,
            "yAxisIndex": y轴索引,
            "brushType": 区域选择类型,
            "brushMode": 区域选择模式,
            "transformable": 可变形或平移,
            "brushStyle": 区域选择样式,
            "throttleType": 限频类型,
            "throttleDelay": 限频延迟,
            "removeOnClick": 单击移除,
            "outOfBrush": 选中区域外视觉,
        }


class 〇标题选项々(TitleOpts):
    def __init__(
        self,
        主标题: Optional[str] = None,
        主标题链接: Optional[str] = None,
        主标题链接目标: Optional[str] = None,
        副标题: Optional[str] = None,
        副标题链接: Optional[str] = None,
        副标题链接目标: Optional[str] = None,
        位置_左: Optional[str] = None,
        位置_右: Optional[str] = None,
        位置_上: Optional[str] = None,
        位置_下: Optional[str] = None,
        内边距: Union[Sequence, Numeric] = 5,
        主副标题间距: Numeric = 10,
        主标题文本样式选项々: Union[TextStyleOpts, dict, None] = None,
        副标题文本样式选项々: Union[TextStyleOpts, dict, None] = None,
    ):
        位置_左 = _左右位置字典.获取(位置_左, 位置_左)
        位置_右 = _左右位置字典.获取(位置_右, 位置_右)
        位置_上 = _上下位置字典.获取(位置_上, 位置_上)
        位置_下 = _上下位置字典.获取(位置_下, 位置_下)

        self.opts: Sequence = [
            {
                "text": 主标题,
                "link": 主标题链接,
                "target": 主标题链接目标,
                "subtext": 副标题,
                "sublink": 副标题链接,
                "subtarget": 副标题链接目标,
                "left": 位置_左,
                "right": 位置_右,
                "top": 位置_上,
                "bottom": 位置_下,
                "padding": 内边距,
                "itemGap": 主副标题间距,
                "textStyle": 主标题文本样式选项々,
                "subtextStyle": 副标题文本样式选项々,
            }
        ]


class 〇数据缩放选项々(DataZoomOpts):
    def __init__(
        self,
        显示: bool = True,
        类型_: str = "滑块",
        实时更新: bool = True,
        范围起始百分比: Union[Numeric, None] = 20,
        范围结束百分比: Union[Numeric, None] = 80,
        起始值: Union[int, str, None] = None,
        结束值: Union[int, str, None] = None,
        朝向: str = 匚朝向.水平,
        x轴索引: Union[int, Sequence[int], None] = None,
        y轴索引: Union[int, Sequence[int], None] = None,
        缩放锁定: bool = False,
        位置_左: Optional[str] = None,
        位置_右: Optional[str] = None,
        位置_上: Optional[str] = None,
        位置_下: Optional[str] = None,
        过滤模式: str = "过滤",
    ):
        如果 类型_ == '滑块': 类型_ = 'slider'
        如果 类型_ == '内部': 类型_ = 'inside'

        位置_左 = _左右位置字典.获取(位置_左, 位置_左)
        位置_右 = _左右位置字典.获取(位置_右, 位置_右)
        位置_上 = _上下位置字典.获取(位置_上, 位置_上)
        位置_下 = _上下位置字典.获取(位置_下, 位置_下)

        过滤模式字典 = {
            "过滤" : "filter",
            "弱过滤" : "weakFilter",
            "空" : "empty",
            "无" : "none",
        }
        过滤模式 = 过滤模式字典.获取(过滤模式, 过滤模式)

        self.opts: dict = {
            "show": 显示,
            "type": 类型_,
            "realtime": 实时更新,
            "startValue": 起始值,
            "endValue": 结束值,
            "start": 范围起始百分比,
            "end": 范围结束百分比,
            "orient": 朝向,
            "xAxisIndex": x轴索引,
            "yAxisIndex": y轴索引,
            "zoomLock": 缩放锁定,
            "left": 位置_左,
            "right": 位置_右,
            "top": 位置_上,
            "bottom": 位置_下,
            "filterMode": 过滤模式,
        }


class 〇图例选项々(LegendOpts):
    def __init__(
        self,
        类型_: Optional[str] = None,
        选择模式: Union[str, bool, None] = None,
        显示: bool = True,
        位置_左: Union[str, Numeric, None] = None,
        位置_右: Union[str, Numeric, None] = None,
        位置_上: Union[str, Numeric, None] = None,
        位置_下: Union[str, Numeric, None] = None,
        朝向: Optional[str] = None,
        对齐: Optional[str] = None,
        内边距: int = 5,
        项目间隙: int = 10,
        项目宽度: int = 25,
        项目高度: int = 14,
        无效颜色: Optional[str] = None,
        文本样式选项々: Union[TextStyleOpts, dict, None] = None,
        图例图标: Optional[str] = None,
    ):
        如果 类型_ == '普通': 类型_ = 'plain'
        如果 类型_ == '滚动': 类型_ = 'scroll'

        如果 选择模式 == '单选': 选择模式 = 'single'
        如果 选择模式 == '多选': 选择模式 = 'multiple'

        位置_左 = _左右位置字典.获取(位置_左, 位置_左)
        位置_右 = _左右位置字典.获取(位置_右, 位置_右)
        位置_上 = _上下位置字典.获取(位置_上, 位置_上)
        位置_下 = _上下位置字典.获取(位置_下, 位置_下)

        如果 对齐 == '左': 对齐 = 'left'
        如果 对齐 == '右': 对齐 = 'right'

        self.opts: dict = {
            "type": 类型_,
            "selectedMode": 选择模式,
            "show": 显示,
            "left": 位置_左,
            "right": 位置_右,
            "top": 位置_上,
            "bottom": 位置_下,
            "orient": 朝向,
            "align": 对齐,
            "padding": 内边距,
            "itemGap": 项目间隙,
            "itemWidth": 项目宽度,
            "itemHeight": 项目高度,
            "inactiveColor": 无效颜色,
            "textStyle": 文本样式选项々,
            "icon": 图例图标,
        }


class 〇视觉映射选项々(VisualMapOpts):
    def __init__(
        self,
        显示: bool = True,
        类型_: str = "颜色",
        最小值_: Numeric = 0,
        最大值_: Numeric = 100,
        两端文本: Optional[Sequence] = None,
        过渡颜色: Optional[Sequence[str]] = None,
        过渡图元大小: Optional[Sequence[int]] = None,
        图元不透明度: Optional[Numeric] = None,
        朝向: str = 匚朝向.竖直,
        位置_左: Optional[str] = None,
        位置_右: Optional[str] = None,
        位置_上: Optional[str] = None,
        位置_下: Optional[str] = None,
        分段数: int = 5,
        系列索引: Union[Numeric, Sequence, None] = None,
        维度: Optional[Numeric] = None,
        显示拖拽手柄: bool = True,
        是分段型: bool = False,
        反转_: bool = False,
        精度: Optional[int] = None,
        分段々: Optional[Sequence] = None,
        范围外: Optional[Sequence] = None,
        长条宽度: int = 0,
        长条高度: int = 0,
        背景颜色: Optional[str] = None,
        边框颜色: Optional[str] = None,
        边框宽度: int = 0,
        文本样式选项々: Union[TextStyleOpts, dict, None] = None,
    ):
        _inrange_op: dict = {}
        if 类型_ == "颜色" or 类型_ == "color":
            过渡颜色 = 过渡颜色 or ["#50a3ba", "#eac763", "#d94e5d"]
            _inrange_op.update(color=过渡颜色)
        elif 类型_ == "大小" or 类型_ == "size":
            过渡图元大小 = 过渡图元大小 or [20, 50]
            _inrange_op.update(symbolSize=过渡图元大小)
        if 图元不透明度 is not None:
            _inrange_op.update(opacity=图元不透明度)

        位置_左 = _左右位置字典.获取(位置_左, 位置_左)
        位置_右 = _左右位置字典.获取(位置_右, 位置_右)
        位置_上 = _上下位置字典.获取(位置_上, 位置_上)
        位置_下 = _上下位置字典.获取(位置_下, 位置_下)

        _visual_typ = "piecewise" if 是分段型 else "continuous"

        if 是分段型 and 长条宽度 == 0 and 长条高度 == 0:
            长条宽度, 长条高度 = 20, 14
        elif 长条宽度 == 0 and 长条高度 == 0:
            长条宽度, 长条高度 = 20, 140

        self.opts: dict = {
            "show": 显示,
            "type": _visual_typ,
            "min": 最小值_,
            "max": 最大值_,
            "text": 两端文本,
            "textStyle": 文本样式选项々,
            "inRange": _inrange_op,
            "calculable": 显示拖拽手柄,
            "inverse": 反转_,
            "precision": 精度,
            "splitNumber": 分段数,
            "dimension": 维度,
            "seriesIndex": 系列索引,
            "orient": 朝向,
            "left": 位置_左,
            "top": 位置_上,
            "bottom": 位置_下,
            "right": 位置_右,
            "showLabel": True,
            "itemWidth": 长条宽度,
            "itemHeight": 长条高度,
            "outOfRange": 范围外,
            "backgroundColor": 背景颜色,
            "borderColor": 边框颜色,
            "borderWidth": 边框宽度,
        }
        if 是分段型:
            self.opts.update(pieces=分段々)


class 〇提示框选项々(TooltipOpts):
    def __init__(
        self,
        显示: bool = True,
        触发类型: str = "数据项",
        触发条件: str = "鼠标移动|鼠标点击",
        坐标轴指示器类型: str = "直线",
        显示内容: bool = True,
        永远显示内容: bool = False,
        显示延迟: Numeric = 0,
        隐藏延迟: Numeric = 100,
        位置: Union[str, Sequence, JSFunc] = None,
        格式器: Optional[JSFunc] = None,
        背景颜色: Optional[str] = None,
        边框颜色: Optional[str] = None,
        边框宽度: Numeric = 0,
        内边距: Numeric = 5,
        文本样式选项々: TextStyleOpts = TextStyleOpts(font_size=14),
    ):
        如果 触发类型 == '数据项': 触发类型 = 'item'
        如果 触发类型 == '坐标轴': 触发类型 = 'axis'
        如果 触发类型 == '无': 触发类型 = 'none'

        触发条件 = 触发条件.替换('鼠标移动', 'mousemove').替换('鼠标点击', 'click')
        如果 触发条件 == '无': 触发条件 = 'none'

        坐标轴指示器类型字典 = {
            '直线' : 'line',
            '阴影' : 'shadow',
            '无' : 'none',
            '十字' : 'cross',
        }
        坐标轴指示器类型 = 坐标轴指示器类型字典.获取(坐标轴指示器类型, 坐标轴指示器类型)

        位置字典 = {
            '内部' : 'inside',
            '上' : 'top',
            '左' : 'left',
            '右' : 'right',
            '下' : 'bottom',
        }
        如果 是实例(位置, 字符串型): 位置 = 位置字典.获取(位置, 位置)

        self.opts: dict = {
            "show": 显示,
            "trigger": 触发类型,
            "triggerOn": 触发条件,
            "axisPointer": {"type": 坐标轴指示器类型},
            "showContent": 显示内容,
            "alwaysShowContent": 永远显示内容,
            "showDelay": 显示延迟,
            "hideDelay": 隐藏延迟,
            "position": 位置,
            "formatter": 格式器,
            "textStyle": 文本样式选项々,
            "backgroundColor": 背景颜色,
            "borderColor": 边框颜色,
            "borderWidth": 边框宽度,
            "padding": 内边距,
        }


class 〇坐标轴线选项々(AxisLineOpts):
    def __init__(
        self,
        显示: bool = True,
        在0刻度上: bool = True,
        在哪个轴的0刻度上: int = 0,
        箭头: Optional[str] = None,
        线条样式选项々: Union[LineStyleOpts, dict, None] = None,
    ):
        如果 箭头 == '无': 箭头 = 'none'
        如果 箭头 == '箭头': 箭头 = 'arrow'
        如果 是实例(箭头, 列表型):
            取 i, s 于 枚举(箭头):
                如果 s == '无': 箭头[i] = 'none'
                如果 s == '箭头': 箭头[i] = 'arrow'

        self.opts: dict = {
            "show": 显示,
            "onZero": 在0刻度上,
            "onZeroAxisIndex": 在哪个轴的0刻度上,
            "symbol": 箭头,
            "lineStyle": 线条样式选项々,
        }


class 〇坐标轴刻度选项々(AxisTickOpts):
    def __init__(
        self,
        显示: bool = True,
        同标签对齐: bool = False,
        内部: bool = False,
        长度: Optional[Numeric] = None,
        线条样式选项々: Union[LineStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "alignWithLabel": 同标签对齐,
            "inside": 内部,
            "length": 长度,
            "lineStyle": 线条样式选项々,
        }


class 〇坐标轴指示器选项々(AxisPointerOpts):
    def __init__(
        self,
        显示: bool = False,
        联动: Sequence[dict] = None,
        类型_: str = "直线",
        标签: Union[LabelOpts, dict, None] = None,
        线条样式选项々: Union[LineStyleOpts, dict, None] = None,
    ):
        类型字典 = {
            '直线' : 'line',
            '阴影' : 'shadow',
            '无' : 'none',
        }
        类型_ = 类型字典.获取(类型_, 类型_)

        self.opts: dict = {
            "show": 显示,
            "type": 类型_,
            "link": 联动,
            "label": 标签,
            "lineStyle": 线条样式选项々,
        }


class 〇坐标轴选项々(AxisOpts):
    def __init__(
        self,
        类型_: Optional[str] = None,
        名称: Optional[str] = None,
        显示: bool = True,
        比例: bool = False,
        反向: bool = False,
        名称位置: str = "end",
        名称间隙: Numeric = 15,
        名称旋转: Optional[Numeric] = None,
        间隔: Optional[Numeric] = None,
        栅格索引: Numeric = 0,
        位置: Optional[str] = None,
        偏移: Numeric = 0,
        分段数: Numeric = 5,
        两边留白: Union[str, bool, None] = None,
        最小值_: Union[Numeric, str, None] = None,
        最大值_: Union[Numeric, str, None] = None,
        最小间隔: Numeric = 0,
        最大间隔: Optional[Numeric] = None,
        坐标轴线选项々: Union[AxisLineOpts, dict, None] = None,
        坐标轴刻度选项々: Union[AxisTickOpts, dict, None] = None,
        坐标轴标签选项々: Union[LabelOpts, dict, None] = None,
        坐标轴指示器选项々: Union[AxisPointerOpts, dict, None] = None,
        名称文本样式选项々: Union[TextStyleOpts, dict, None] = None,
        分隔区域选项々: Union[SplitAreaOpts, dict, None] = None,
        分割线选项々: Union[SplitLineOpts, dict] = SplitLineOpts(),
        次级刻度选项々: Union[MinorTickOpts, dict, None] = None,
        次级分割线选项々: Union[MinorSplitLineOpts, dict, None] = None,
    ):
        名称位置字典 = {
            '开始' : 'start',
            '中间' : 'middle',
            '末尾' : 'end',
        }
        名称位置 = 名称位置字典.获取(名称位置, 名称位置)

        如果 位置 == '上': 位置 = 'top'
        如果 位置 == '下': 位置 = 'bottom'

        self.opts: dict = {
            "type": 类型_,
            "name": 名称,
            "show": 显示,
            "scale": 比例,
            "nameLocation": 名称位置,
            "nameGap": 名称间隙,
            "nameRotate": 名称旋转,
            "interval": 间隔,
            "nameTextStyle": 名称文本样式选项々,
            "gridIndex": 栅格索引,
            "axisLine": 坐标轴线选项々,
            "axisTick": 坐标轴刻度选项々,
            "axisLabel": 坐标轴标签选项々,
            "axisPointer": 坐标轴指示器选项々,
            "inverse": 反向,
            "position": 位置,
            "offset": 偏移,
            "splitNumber": 分段数,
            "boundaryGap": 两边留白,
            "min": 最小值_,
            "max": 最大值_,
            "minInterval": 最小间隔,
            "maxInterval": 最大间隔,
            "splitLine": 分割线选项々,
            "splitArea": 分隔区域选项々,
            "minorTick": 次级刻度选项々,
            "minorSplitLine": 次级分割线选项々,
        }


class 〇栅格选项々(GridOpts):
    def __init__(
        self,
        显示: bool = False,
        z层级: Numeric = 0,
        z: Numeric = 2,
        位置_左: Union[Numeric, str, None] = None,
        位置_上: Union[Numeric, str, None] = None,
        位置_右: Union[Numeric, str, None] = None,
        位置_下: Union[Numeric, str, None] = None,
        宽度: Union[Numeric, str, None] = None,
        高度: Union[Numeric, str, None] = None,
        包含标签: bool = False,
        背景颜色: str = "transparent",
        边框颜色: str = "#ccc",
        边框宽度: Numeric = 1,
        提示框选项々: Union[TooltipOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "zlevel": z层级,
            "z": z,
            "left": 位置_左,
            "top": 位置_上,
            "right": 位置_右,
            "bottom": 位置_下,
            "width": 宽度,
            "height": 高度,
            "containLabel": 包含标签,
            "backgroundColor": 背景颜色,
            "borderColor": 边框颜色,
            "borderWidth": 边框宽度,
            "tooltip": 提示框选项々,
        }


class 〇三维栅格选项々(Grid3DOpts):
    def __init__(
        self,
        宽度: Numeric = 200,
        高度: Numeric = 100,
        深度: Numeric = 80,
        旋转: bool = False,
        旋转速度: Numeric = 10,
        旋转灵敏度: Numeric = 1,
    ):
        self.opts: dict = {
            "boxWidth": 宽度,
            "boxHeight": 高度,
            "boxDepth": 深度,
            "viewControl": {
                "autoRotate": 旋转,
                "autoRotateSpeed": 旋转速度,
                "rotateSensitivity": 旋转灵敏度,
            },
        }


class 〇三维坐标轴选项々(Axis3DOpts):
    def __init__(
        self,
        数据: Optional[Sequence] = None,
        类型_: Optional[str] = None,
        名称: Optional[str] = None,
        名称间隙: Numeric = 20,
        最小值_: Union[str, Numeric, None] = None,
        最大值_: Union[str, Numeric, None] = None,
        分段数: Optional[Numeric] = None,
        间隔: Optional[Numeric] = None,
        外边距: Numeric = 8,
        文本样式选项々: Union[TextStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "data": 数据,
            "name": 名称,
            "nameGap": 名称间隙,
            "nameTextStyle": 文本样式选项々,
            "splitNum": 分段数,
            "type": 类型_,
            "min": 最小值_,
            "max": 最大值_,
            "axisLabel": {"margin": 外边距, "interval": 间隔},
        }


class 〇平行坐标系选项々(ParallelOpts):
    def __init__(
        self,
        位置_左: str = "5%",
        位置_右: str = "13%",
        位置_下: str = "10%",
        位置_上: str = "20%",
        布局: Optional[str] = None,
    ):
        self.opts: dict = {
            "left": 位置_左,
            "right": 位置_右,
            "bottom": 位置_下,
            "top": 位置_上,
            "layout": 布局,
        }


class 〇平行坐标轴选项々(ParallelAxisOpts):
    def __init__(
        self,
        维度: Numeric,
        名称: str,
        数据: Sequence = None,
        类型_: Optional[str] = None,
        最小值_: Union[str, Numeric, None] = None,
        最大值_: Union[str, Numeric, None] = None,
        比例: bool = False,
    ):
        self.opts: dict = {
            "dim": 维度,
            "name": 名称,
            "data": 数据,
            "type": 类型_,
            "min": 最小值_,
            "max": 最大值_,
            "scale": 比例,
        }


class 〇雷达指示器(RadarIndicatorItem):
    def __init__(
        self,
        名称: Optional[str] = None,
        最小值_: Optional[Numeric] = None,
        最大值_: Optional[Numeric] = None,
        颜色: Optional[str] = None,
    ):
        self.opts: dict = {"name": 名称, "max": 最大值_, "min": 最小值_, "color": 颜色}


class 〇日历星期轴样式选项々(CalendarDayLabelOpts):
    def __init__(
        self,
        显示: bool = True,
        第一天: int = 0,
        外边距: Optional[int] = None,
        位置: str = "start",
        名称映射: Union[str, Sequence] = "en",
        标签文本颜色: str = "#000",
        标签字体样式: str = "normal",
        标签字体粗细: str = "normal",
        标签字体族: str = "sans-serif",
        标签字体大小: int = 12,
        水平对齐: Optional[str] = None,
        垂直对齐: Optional[str] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "firstDay": 第一天,
            "margin": 外边距,
            "position": 位置,
            "nameMap": 名称映射,
            "color": 标签文本颜色,
            "fontStyle": 标签字体样式,
            "fontWeight": 标签字体粗细,
            "fontFamily": 标签字体族,
            "fontSize": 标签字体大小,
            "align": 水平对齐,
            "verticalAlign": 垂直对齐,
        }


class 〇日历月份轴样式选项々(CalendarMonthLabelOpts):
    def __init__(
        self,
        显示: bool = True,
        水平对齐: Optional[str] = None,
        外边距: Optional[int] = None,
        位置: str = "start",
        名称映射: Union[str, Sequence] = "en",
        格式器: JSFunc = None,
        标签文本颜色: str = "#000",
        标签字体样式: str = "normal",
        标签字体粗细: str = "normal",
        标签字体族: str = "sans-serif",
        标签字体大小: int = 12,
        垂直对齐: Optional[str] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "align": 水平对齐,
            "margin": 外边距,
            "position": 位置,
            "nameMap": 名称映射,
            "formatter": 格式器,
            "color": 标签文本颜色,
            "fontStyle": 标签字体样式,
            "fontWeight": 标签字体粗细,
            "fontFamily": 标签字体族,
            "fontSize": 标签字体大小,
            "verticalAlign": 垂直对齐,
        }


class 〇日历年样式选项々(CalendarYearLabelOpts):
    def __init__(
        self,
        显示: bool = True,
        外边距: Optional[int] = None,
        位置: Optional[str] = None,
        格式器: JSFunc = None,
        标签文本颜色: str = "#000",
        标签字体样式: str = "normal",
        标签字体粗细: str = "normal",
        标签字体族: str = "sans-serif",
        标签字体大小: int = 12,
        align: Optional[str] = None,
        垂直对齐: Optional[str] = None,
    ):
        self.opts: dict = {
            "show": 显示,
            "margin": 外边距,
            "position": 位置,
            "formatter": 格式器,
            "color": 标签文本颜色,
            "fontStyle": 标签字体样式,
            "fontWeight": 标签字体粗细,
            "fontFamily": 标签字体族,
            "fontSize": 标签字体大小,
            "align": align,
            "verticalAlign": 垂直对齐,
        }


class 〇日历选项々(CalendarOpts):
    def __init__(
        self,
        位置_左: Optional[str] = None,
        位置_上: Optional[str] = None,
        位置_右: Optional[str] = None,
        位置_下: Optional[str] = None,
        宽度: Optional[str] = "auto",
        高度: Optional[str] = None,
        朝向: Optional[str] = "horizontal",
        范围_: Union[str, Sequence, int] = None,
        每格大小: Union[int, Sequence] = 20,
        分割线选项々: Union[SplitLineOpts, dict, None] = None,
        单元格样式选项々: Union[ItemStyleOpts, dict, None] = None,
        星期轴样式选项々: Union[CalendarDayLabelOpts, dict, None] = None,
        月份轴样式选项々: Union[CalendarMonthLabelOpts, dict, None] = None,
        年样式选项々: Union[CalendarYearLabelOpts, dict, None] = None,
    ):
        self.opts: dict = {
            "left": 位置_左,
            "top": 位置_上,
            "right": 位置_右,
            "bottom": 位置_下,
            "width": 宽度,
            "height": 高度,
            "orient": 朝向,
            "range": 范围_,
            "cellSize": 每格大小,
            "splitLine": 分割线选项々,
            "itemStyle": 单元格样式选项々,
            "dayLabel": 星期轴样式选项々,
            "monthLabel": 月份轴样式选项々,
            "yearLabel": 年样式选项々,
        }


class 〇单轴选项々(SingleAxisOpts):
    def __init__(
        self,
        名称: Optional[str] = None,
        最大值_: Union[str, Numeric, None] = None,
        最小值_: Union[str, Numeric, None] = None,
        位置_左: Optional[str] = None,
        位置_右: Optional[str] = None,
        位置_上: Optional[str] = None,
        位置_下: Optional[str] = None,
        宽度: Optional[str] = None,
        高度: Optional[str] = None,
        朝向: Optional[str] = None,
        类型_: Optional[str] = None,
    ):
        self.opts: dict = {
            "name": 名称,
            "max": 最大值_,
            "min": 最小值_,
            "left": 位置_左,
            "right": 位置_右,
            "top": 位置_上,
            "bottom": 位置_下,
            "width": 宽度,
            "height": 高度,
            "orient": 朝向,
            "type": 类型_,
        }


class 〇径向轴项(RadiusAxisItem):
    def __init__(
        self,
        值: Optional[str] = None,
        文本样式选项々: Union[TextStyleOpts, dict, None] = None,
    ):
        self.opts: dict = {"value": 值, "textStyle": 文本样式选项々}


class 〇角度轴项(AngleAxisItem):
    def __init__(
        self,
        值: Optional[str] = None,
        文本样式选项々: Optional[TextStyleOpts] = None,
    ):
        super().__init__(值, 文本样式选项々)


class 〇径向轴选项々(RadiusAxisOpts):
    def __init__(
        self,
        极坐标系索引: Optional[int] = None,
        数据: Optional[Sequence[Union[RadiusAxisItem, dict, str]]] = None,
        两边留白: Union[bool, Sequence] = None,
        类型_: Optional[str] = None,
        名称: Optional[str] = None,
        名称位置: Optional[str] = None,
        最小值_: Union[str, Numeric, None] = None,
        最大值_: Union[str, Numeric, None] = None,
        比例: bool = False,
        间隔: Optional[Numeric] = None,
        分割线选项々: Union[SplitLineOpts, dict, None] = None,
        分隔区域选项々: Union[SplitAreaOpts, dict, None] = None,
        坐标轴刻度选项々: Union[AxisTickOpts, dict, None] = None,
        坐标轴线选项々: Union[AxisLineOpts, dict, None] = None,
        坐标轴标签选项々: Union[LabelOpts, dict, None] = None,
        z: Optional[int] = None,
    ):
        _data = []
        if 数据:
            for d in 数据:
                if isinstance(d, RadiusAxisItem):
                    d = d.opts
                _data.append(d)

        名称位置字典 = {
            '开始' : 'start',
            '中间' : 'middle',
            '末尾' : 'end',
        }
        名称位置 = 名称位置字典.获取(名称位置, 名称位置)

        self.opts: dict = {
            "polarIndex": 极坐标系索引,
            "type": 类型_,
            "data": 数据,
            "boundaryGap": 两边留白,
            "name": 名称,
            "nameLocation": 名称位置,
            "min": 最小值_,
            "max": 最大值_,
            "scale": 比例,
            "interval": 间隔,
            "splitLine": 分割线选项々,
            "splitArea": 分隔区域选项々,
            "axisTick": 坐标轴刻度选项々,
            "axisLine": 坐标轴线选项々,
            "axisLabel": 坐标轴标签选项々,
            "z": z,
        }


class 〇角度轴选项々(AngleAxisOpts):
    def __init__(
        self,
        极坐标系索引: Optional[int] = None,
        数据: Optional[Sequence[Union[AngleAxisItem, Numeric, dict, str]]] = None,
        起始角度: Optional[Numeric] = None,
        顺时针: bool = False,
        两边留白: Union[bool, Sequence, None] = None,
        类型_: Optional[str] = None,
        最小值_: Union[str, Numeric, None] = None,
        最大值_: Union[str, Numeric, None] = None,
        比例: bool = False,
        分段数: Numeric = 5,
        间隔: Optional[Numeric] = None,
        分割线选项々: Union[SplitLineOpts, dict, None] = None,
        坐标轴线选项々: Union[AxisLineOpts, dict, None] = None,
        坐标轴刻度选项々: Union[AxisTickOpts, dict, None] = None,
        坐标轴标签选项々: Union[LabelOpts, dict, None] = None,
        z: Optional[int] = None,
    ):
        _data = []
        if 数据:
            for d in 数据:
                if isinstance(d, AngleAxisItem):
                    d = d.opts
                _data.append(d)

        self.opts: dict = {
            "polarIndex": 极坐标系索引,
            "startAngle": 起始角度,
            "data": 数据,
            "clockwise": 顺时针,
            "boundaryGap": 两边留白,
            "type": 类型_,
            "min": 最小值_,
            "max": 最大值_,
            "scale": 比例,
            "splitNumber": 分段数,
            "interval": 间隔,
            "splitLine": 分割线选项々,
            "axisLine": 坐标轴线选项々,
            "axisTick": 坐标轴刻度选项々,
            "axisLabel": 坐标轴标签选项々,
            "z": z,
        }


class 〇极坐标系选项々(PolarOpts):
    def __init__(
        self,
        中心: Optional[Sequence] = None,
        半径: Optional[Union[Sequence, str]] = None,
        提示框选项々: TooltipOpts = None,
    ):
        self.opts: dict = {"center": 中心, "radius": 半径, "tooltip": 提示框选项々}
