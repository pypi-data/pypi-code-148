from setuptools import setup

setup(
	name='easy_m3u8',  # 项目名
	version='1.1',  # 版本号
	packages=['easy_m3u8'],  # 包括在安装包内的Python包
	install_requires=[  # 依赖列表
		"requests",
		"pycryptodome"
	]
)
