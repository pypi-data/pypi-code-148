from setuptools import setup

setup(name='yolov3-minimal',
      version='0.1.5',
      url='https://github.com/diyoon3080/yolov3-minimal',
      author='Do Il Yoon',
      author_email='diyoon@mz.co.kr ',
      python_requires='>=3.7',
      install_requires=['numpy', 'tensorflow', 'opencv-python-headless'],
      packages=['yolov3_minimal'])