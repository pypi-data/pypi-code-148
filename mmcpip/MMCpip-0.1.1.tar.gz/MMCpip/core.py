# Insert your code here. 
from os import *


print('''如果您是第一次使用这个库，想获取具体用法，请调用\'帮助()\'获取帮助''')

def 帮助():
    帮助信息 = '''升级()  升级pip   例：升级()
    安装列表()  查看所有已安装的库   例：安装列表()
    修改默认源(链接)   修改pip时的默认源（pip默认PYPI），此函数默认为清华源 例：修改默认源('http://mirrors.aliyun.com/pypi/simple/')
    安装(库,源,版本)  此函数为下载库后自动配置到Python解释器(下载后直接用)，如果你不知道具体要使用哪个版本的库，请勿填写   例：安装(MMCpip,清华源,0.1.0)
    卸载(库)   卸载指定的库  例：卸载('MMCpip')
    查看更新()  查看所有需要更新的库  例：查看更新()
    查看冲突(库)  查看所有不兼容的库   例：查看冲突()
    下载(库,路径)#这个函数暂时无法使用    下载库但不安装(下载后不能直接用) 例：下载('MMCpip','E:\\')
    生成批量下载文件()  生成包含所有库的.txt文件  例：生成批量下载文件()
    批量下载(源)#这个函数暂时无法使用  要成生成包含所有库的.txt文件，然后调用此函数(不建议使用，因为库太多了不好管理，而且你的电脑上会有很多库，占用很大)    例：批量下载(清华大学)
    搜索(库)   搜索库，因为中国大部分地区的\'pip search\'不能使用，所以这里用了第三方库pip_search   例：搜索(MMCpip)
    '''
    print(帮助信息)

def 升级():
    print(system('pip install --upgrade pip'))

def 安装列表():
    print(system('pip list'))

def 修改默认源(链接='https://pypi.tuna.tsinghua.edu.cn/simple/'):
    print(system(f'pip config set global.index - url - i {链接}'))


def 安装(库,源= '',版本= ''):
    if 版本 == '':
        pass
    else:
        版本 = ' matplotlib=='+版本

    if 源 == '':
        print(system(f'pip install {库}'))
    elif 源 == '阿里云':
        print(system(f'pip install -i http://mirrors.aliyun.com/pypi/simple/ {库}{版本}'))
    elif 源 == '中国科技大学':
        print(system(f'pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ {库}{版本}'))
    elif 源 == '豆瓣':
        print(system(f'pip install -i  http://pypi.douban.com/simple/ {库}{版本}'))
    elif 源 == '清华大学':
        print(system(f'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ {库}{版本}'))


def 卸载(库):
    print(system(f'pip uninstall {库}'))

def 查看更新():
    print(system('pip list -o'))

def 查看冲突(库 = ''):
    print(system(f'pip check {库}'))

def 信息(库):
    print(system(f'pip show -f{库}'))

#def 下载(库,路径):
    #print(system(f'pip download {库} -d {路径}'))

def 生成批量下载文件():
    print(system('pip freeze'))

#def 批量下载(源=''):
#    if 源 == '':
#        print(system(f'pip install '))
#    elif 源 == '阿里云':
#        print(system(f'pip install -i http://mirrors.aliyun.com/pypi/simple/ '))
#    elif 源 == '中国科技大学':
#        print(system(f'pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ '))
#    elif 源 == '豆瓣':
#        print(system(f'pip install -i  http://pypi.douban.com/simple/ '))
#    elif 源 == '清华大学':
#        print(system(f'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt'))

def 搜索(库):
    try:
        import pip_search
    except ImportError:
        print ('检测到您的search功能被禁用，正在自动为您下载pip_search')
        安装('pip_search','清华大学')
    print(system(f'pip_search{库}'))