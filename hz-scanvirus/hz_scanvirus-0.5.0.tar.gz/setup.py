import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hz_scanvirus",  # 用自己的名替换其中的YOUR_USERNAME_
    version="0.5.0",  # 包版本号，便于维护版本
    author="tjsh",  # 作者，可以写自己的姓名
    author_email="tjsh.tan@outlook.com",  # 作者联系方式，可写自己的邮箱地址
    description="HeZhong AV Pack. Uses version 5.31 of the engine.",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://gitee.com/tjsh/hz_scanvirus",  # 自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)

