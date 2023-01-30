
from setuptools import setup, find_packages  
  
setup(  
    name = 'KeyWeighted',  
    version = '0.0.1',
    description = 'add option arg key to some lib',  
    license = 'MIT License',  
    install_requires = [],  
    packages = ['KeyWeighted'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'HellOwhatAs',  
    author_email = 'xjq701229@outlook.com',
    url = 'https://github.com/HellOwhatAs/KeyWeighted',
    # packages = find_packages(include=("*"),),  
)  

