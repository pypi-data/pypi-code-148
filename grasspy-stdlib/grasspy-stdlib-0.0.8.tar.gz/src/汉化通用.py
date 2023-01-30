'''汉化通用函数'''
导入 正则

套路 _关键词参数中转英(中文关键词, 关键词字典, 值字典=空):
    '''将关键词参数 (**关键词参数/**kwags 之类) 中的汉化键/值转换回英文键/值'''
    英文关键词 = {}
    如果 值字典 是 空:
        取 键, 值 于 中文关键词.项々():
            英文关键词[关键词字典.获取(键, 键)] = 值
    否则:
        取 键, 值 于 中文关键词.项々():
            如果 是实例(值, 字符串型):
                英文关键词[关键词字典.获取(键, 键)] = 值字典.获取(值, 值)
            否则:
                英文关键词[关键词字典.获取(键, 键)] = 值
    返回 英文关键词

套路 _星号参数中转英(参数, 参数字典):
    '''将星号参数 (*参数/*args) 中的中文转换回英文'''
    如果 参数:
        参数列表 = []
        取 元素 于 参数:
            元素 = 参数字典.获取(元素, 元素)
            参数列表.追加(元素)
        参数 = 元组型(参数列表)
    返回 参数

套路 _类属性翻译(**中英属性):
    """将汉化类的中文属性名翻译回原来的英文属性名.
    不适用于属性值会动态改变的情况.
    """
    套路 包装盒(某类):
        取 中文属性, 英文属性 于 中英属性.项々():
            如果 有属性(某类, 中文属性):
                设属性(某类, 英文属性, 某类.__dict__[中文属性])
                # 删属性(某类, 中文属性)
        返回 某类
    返回 包装盒

套路 _反向注入(中文类名, 英文类名):
    """将汉化类中的汉化属性(包括方法)反向注入到相应的英文类中.
    这是猴子补丁汉化法的改进版, 有助于保持模块的优雅.
    """
    属性列表 = dir(中文类名)
    取 属性名 于 属性列表:
        如果 非 属性名.开头是('__') 且 正则.搜索('[\u4e00-\u9fa5]', 属性名):
            设属性(英文类名, 属性名, 取属性(中文类名, 属性名))

类 匚颜色:
    爱丽丝蓝 = 'aliceblue'
    古董白 = 'antiquewhite'
    湖绿 = 'aqua'
    碧绿 = 'aquamarine'
    青白色 = 'azure'
    米色 = 'beige'
    陶坯黄 = 'bisque'
    黑色 = 'black'
    杏仁白 = 'blanchedalmond'
    蓝色 = 'blue'
    蓝紫色 = 'blueviolet'
    褐色 = 'brown'
    硬木褐 = 'burlywood'
    军服蓝 = 'cadetblue'
    查特酒绿 = 'chartreuse'
    巧克力色 = 'chocolate'
    珊瑚红 = 'coral'
    矢车菊蓝 = 'cornflowerblue'
    玉米穗黄 = 'cornsilk'
    绯红 = 'crimson'
    青色 = 'cyan'
    深蓝 = 'darkblue'
    深青 = 'darkcyan'
    深金菊黄 = 'darkgoldenrod'
    暗灰 = 'darkgray'
    深绿 = 'darkgreen'
    深卡其色 = 'darkkhaki'
    深品红 = 'darkmagenta'
    深橄榄绿 = 'darkolivegreen'
    深橙 = 'darkorange'
    深洋兰紫 = 'darkorchid'
    深红 = 'darkred'
    深鲑红 = 'darksalmon'
    深海藻绿 = 'darkseagreen'
    深岩蓝 = 'darkslateblue'
    深岩灰 = 'darkslategray'
    深松石绿 = 'darkturquoise'
    深紫 = 'darkviolet'
    深粉 = 'deeppink'
    深天蓝 = 'deepskyblue'
    昏灰 = 'dimgray'
    道奇蓝 = 'dodgerblue'
    火砖红 = 'firebrick'
    花卉白 = 'floralwhite'
    森林绿 = 'forestgreen'
    紫红 = 'fuchsia'
    庚氏灰 = 'gainsboro'
    幽灵白 = 'ghostwhite'
    金色 = 'gold'
    金菊黄 = 'goldenrod'
    灰色 = 'gray'
    调和绿 = 'green'
    黄绿色 = 'greenyellow'
    蜜瓜绿 = 'honeydew'
    艳粉 = 'hotpink'
    印度红 = 'indianred'
    靛蓝 = 'indigo'
    象牙白 = 'ivory'
    卡其色 = 'khaki'
    薰衣草紫 = 'lavender'
    薰衣草红 = 'lavenderblush'
    草坪绿 = 'lawngreen'
    柠檬绸黄 = 'lemonchiffon'
    浅蓝 = 'lightblue'
    浅珊瑚红 = 'lightcoral'
    浅青 = 'lightcyan'
    浅金菊黄 = 'lightgoldenrodyellow'
    浅金菊黄 = 'lightgoldenrod'
    亮灰 = 'lightgray'
    浅绿 = 'lightgreen'
    浅粉 = 'lightpink'
    浅鲑红 = 'lightsalmon'
    浅海藻绿 = 'lightseagreen'
    浅天蓝 = 'lightskyblue'
    浅岩灰 = 'lightslategray'
    浅钢青 = 'lightsteelblue'
    浅黄 = 'lightyellow'
    绿色 = 'lime'
    青柠绿 = 'limegreen'
    亚麻色 = 'linen'
    洋红 = 'magenta'
    栗色 = 'maroon'
    中碧绿 = 'mediumaquamarine'
    中蓝 = 'mediumblue'
    中洋兰紫 = 'mediumorchid'
    中紫 = 'mediumpurple'
    中海藻绿 = 'mediumseagreen'
    中岩蓝 = 'mediumslateblue'
    中嫩绿 = 'mediumspringgreen'
    中松石绿 = 'mediumturquoise'
    中紫红 = 'mediumvioletred'
    午夜蓝 = 'midnightblue'
    薄荷乳白 = 'mintcream'
    雾玫瑰红 = 'mistyrose'
    鹿皮色 = 'moccasin'
    土著白 = 'navajowhite'
    藏青 = 'navy'
    旧蕾丝白 = 'oldlace'
    橄榄色 = 'olive'
    橄榄绿 = 'olivedrab'
    橙色 = 'orange'
    橘红 = 'orangered'
    洋兰紫 = 'orchid'
    白金菊黄 = 'palegoldenrod'
    白绿色 = 'palegreen'
    白松石绿 = 'paleturquoise'
    白紫红 = 'palevioletred'
    番木瓜橙 = 'papayawhip'
    粉扑桃色 = 'peachpuff'
    秘鲁红 = 'peru'
    粉色 = 'pink'
    李紫 = 'plum'
    粉末蓝 = 'powderblue'
    紫色 = 'purple'
    红色 = 'red'
    瑞贝卡紫 = 'rebeccapurple'
    玫瑰褐 = 'rosybrown'
    品蓝 = 'royalblue'
    鞍褐 = 'saddlebrown'
    鲑红 = 'salmon'
    沙褐 = 'sandybrown'
    海藻绿 = 'seagreen'
    贝壳白 = 'seashell'
    土黄赭 = 'sienna'
    银色 = 'silver'
    天蓝 = 'skyblue'
    岩蓝 = 'slateblue'
    岩灰 = 'slategray'
    雪白 = 'snow'
    春绿 = 'springgreen'
    钢青 = 'steelblue'
    日晒褐 = 'tan'
    鸭翅绿 = 'teal'
    蓟紫 = 'thistle'
    番茄红 = 'tomato'
    松石绿 = 'turquoise'
    紫罗兰色 = 'violet'
    麦色 = 'wheat'
    白色 = 'white'
    烟雾白 = 'whitesmoke'
    黄色 = 'yellow'
    暗黄绿色 = 'yellowgreen'
    当前颜色 = 'currentcolor'
    透明 = 'transparent'

