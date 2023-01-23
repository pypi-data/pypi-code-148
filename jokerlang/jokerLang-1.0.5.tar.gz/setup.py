import os
import setuptools

setuptools.setup(
      name='jokerLang',
      version='1.0.5',  # 版本号
      keywords='joker',
      description='Hello,welcome to my field',
      long_description=open(
          os.path.join(
              os.path.dirname(__file__),
              'README.rst')
      ).read(),
      platforms=["all"],
      author='jokerLang',
      author_email='524276169@qq.com',
      packages=setuptools.find_packages(),
      license='MIT'
      )
