类 匚渲染类型:
    画布="canvas"
    SVG="svg"


类 匚文件类型:
    SVG: str = "svg"
    PNG: str = "png"
    JPEG: str = "jpeg"
    HTML: str = "html"


类 匚记号类型:
    矩形: str = "rect"
    圆角矩形: str = "roundRect"
    三角形: str = "triangle"
    菱形: str = "diamond"
    箭头: str = "arrow"


类 匚图表类型:
    柱状图: str = "bar"
    三维柱状图: str = "bar3D"
    箱形图: str = "boxplot"
    涟漪特效散点图: str = "effectScatter"
    漏斗图: str = "funnel"
    仪表盘: str = "gauge"
    地理坐标: str = "geo"
    关系图: str = "graph"
    热力图: str = "heatmap"
    K线图: str = "candlestick"
    折线图: str = "line"
    三维折线图: str = "line3D"
    路径图: str = "lines"
    三维路径图: str = "lines3D"
    水球图: str = "liquidFill"
    地图: str = "map"
    三维地图: str = "map3D"
    平行坐标系: str = "parallel"
    象形柱状图: str = "pictorialBar"
    饼图: str = "pie"
    极坐标系: str = "polar"
    雷达图: str = "radar"
    桑基图: str = "sankey"
    散点图: str = "scatter"
    三维散点图: str = "scatter3D"
    旭日图: str = "sunburst"
    主题河流图: str = "themeRiver"
    树图: str = "tree"
    矩形树图: str = "treemap"
    词云: str = "wordCloud"
    自定义: str = "custom"


类 匚主题类型:
    内置主题々 = ["light", "dark", "white"]
    浅色 = "light"
    深色 = "dark"
    白色 = "white"
    粉笔: str = "chalk"
    厄索斯: str = "essos"
    信息图: str = "infographic"
    马卡龙: str = "macarons"
    紫色激情: str = "purple-passion"
    吉普赛人: str = "roma"
    浪漫: str = "romantic"
    亮彩: str = "shine"
    复古: str = "vintage"
    瓦尔登湖: str = "walden"
    日落国度: str = "westeros"
    仙境: str = "wonderland"
    鬼节: str = "halloween"


类 匚地理图类型:
    散点图: str = "scatter"
    涟漪特效散点图: str = "effectScatter"
    热力图: str = "heatmap"
    折线图: str = "lines"


类 匚百度地图参数:
    # BMap Control location
    锚点_左上 = 0
    锚点_右上 = 1
    锚点_左下 = 2
    锚点_右下 = 3

    # BMap Navigation Control Type
    导航控制_大 = 0
    导航控制_小 = 1
    导航控制_平移 = 2
    导航控制_缩放 = 3

    # BMap Maptype Control Type
    地图类型_水平 = 0
    地图类型_下拉 = 1
    地图类型_地图 = 2


类 匚笔记本类型:
    JUPYTER_NOTEBOOK = "jupyter_notebook"
    JUPYTER_LAB = "jupyter_lab"
    NTERACT = "nteract"
    ZEPPELIN = "zeppelin"


类 匚在线主机:
    默认主机 = "https://assets.pyecharts.org/assets/"
    笔记本主机 = "http://localhost:8888/nbextensions/assets/"


类 匚警告控制:
    显示警告 = True


# 类 匚当前配置: 

# 汉化常量（字符串等）的新方式
# 若使用枚举对象，要获得字符串，须取其成员的值，稍显麻烦
类 匚标记类型:
    最大值 = 'max'
    最小值 = 'min'
    平均值 = 'average'

类 匚坐标轴类型:
    数值 = 'value'
    类目 = 'category'
    时间 = 'time'
    对数 = 'log'

类 匚朝向:
    水平 = 'horizontal'
    竖直 = 'vertical'