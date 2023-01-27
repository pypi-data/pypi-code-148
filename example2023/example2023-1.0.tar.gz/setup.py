from setuptools import setup

with open("README.md", "r") as file:
	readme = file.read()
setup(
	name='example2023',  # 项目名
	packages=['example2023'],  # 项目名
	version='1.0',  # 版本号
	long_description=readme,
	long_description_content_type="text/markdown",
	data_files=[("", ["README.md"])]
)
