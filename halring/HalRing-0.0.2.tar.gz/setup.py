from setuptools import setup, find_packages
setup(
    name="HalRing",
    version="0.0.2",
    #url='https://www.python.org',
    license="MIT Licence",
    author="peixiaodong",
    author_email="pxd7th@vip.qq.com",
    url="",
    packages=find_packages(exclude=["unittest"]),
    install_requires=['jira']

)