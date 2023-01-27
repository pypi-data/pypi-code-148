from setuptools import setup

with open("README.md", "r") as file:
	readme = file.read()

setup(
	name='easy_m3u8',  # 项目名
	packages=['easy_m3u8'],  # 项目名
	version='1.2',  # 版本号
	install_requires=[  # 依赖列表
		"requests",
		"pycryptodome"
	],
	long_description=readme,
	long_description_content_type="text/markdown",
	data_files=[("", ["README.md"])]
)
