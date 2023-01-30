from pyecharts.commons.utils import *

类 JS代码(JsCode):
    套路 替换(分身, 模式, 替换字符串):
        返回 分身.replace(模式, 替换字符串)

_左右位置字典 = {
    '左' : 'left',
    '中' : 'center',
    '右' : 'right',
}

_上下位置字典 = {
    '上' : 'top',
    '中' : 'middle',
    '下' : 'bottome',
}

_标签位置字典 = {
    '上' : 'top',
    '下' : 'bottome',
    '左' : 'left',
    '右' : 'right',
    '内部' : 'inside',
    '内部左侧' : 'insideLeft',
    '内部右侧' : 'insideRight',
    '内部上方' : 'insideTop',
    '内部下方' : 'insideBottom',
    '内部左上' : 'insideTopLeft',
    '内部左下' : 'insideBottomLeft',
    '内部右上' : 'insideTopRight',
    '内部右下' : 'insideBottomRight',
    '外部' : 'outside',
    '中' : 'middle',
    '中间' : 'center'
}