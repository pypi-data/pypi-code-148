from setuptools import setup, find_packages

print(find_packages())

requires = [
    'redis == 4.4.2'
]


setup(
    name="simplededup",
    version="0.1.2",
    packages=find_packages(),
    description="提供多种简单爬虫url去重",
    author="phimes",
    author_email="phimes@163.com",
)