# Insert your code here. 
from os import system

def 所有指令():
    print('安装pip()')
    print('安装列表()')
    print('安装(库,源,版本= '')')
    print('卸载(库)')
    print('升级()')
    print('查看更新()')
    print('查看冲突')
    print('信息(库)')
    print('下载(库,路径)')
    print('生成批量下载文件()')
    print('批量下载(源='')')
    print('搜索(库):')
    print('本版本的库不支持安装pip如果您的电脑上没有pip，请自行下载')

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

def 查看冲突():
    print(system(f'pip check {库}'))

def 信息(库):
    print(system(f'pip show -f{库}'))

def 下载(库,路径):
    print(system(f'pip download {库} -d {路径}'))

def 生成批量下载文件():
    print(system('pip freeze'))
    print(system('requirements.txt'))

def 批量下载(源=''):
    if 源 == '':
        print(system(f'pip install '))
    elif 源 == '阿里云':
        print(system(f'pip install -i http://mirrors.aliyun.com/pypi/simple/ '))
    elif 源 == '中国科技大学':
        print(system(f'pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ '))
    elif 源 == '豆瓣':
        print(system(f'pip install -i  http://pypi.douban.com/simple/ '))
    elif 源 == '清华大学':
        print(system(f'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt'))

def 搜索(库):
    print(system(f'search {库}'))