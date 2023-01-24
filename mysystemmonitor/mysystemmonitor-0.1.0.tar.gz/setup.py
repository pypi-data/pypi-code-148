from setuptools import setup


setup(name='mysystemmonitor',
version='0.1.0',
description="""A library to monitoring system.""",
long_description="""
# System Monitor
A library to monitoring system.
# Install
```
pip3 install mysystemmonitor
```
# Using
## In another script
```python
from mysystemmonitor import mysystemmonitor

#  mysystemmonitor(interval=2, nosystemload=False, nomemoryusage=False, nodiskusage=False)
monitor = mysystemmonitor()

print(monitor.system_load())
print(monitor.memory_usage())
print(monitor.disk_usage())

#or you can use monitoring

monitor.run()

```
## In command line
```console
mysystemmonitor run
```

parameters:
```console
mysystemmonitor run --interval 1 --nosystemload False --nomemoryusage False --nodiskusage False
```
""",
long_description_content_type='text/markdown',
url='https://github.com/onuratakan/mysystemmonitor',
author='Onur Atakan ULUSOY',
author_email='atadogan06@gmail.com',
license='MIT',
packages=["mysystemmonitor"],
package_dir={'':'src'},
install_requires=[
    "tqdm==4.64.1",
    "fire==0.5.0",
    "psutil==5.9.4"
],
entry_points = {
    'console_scripts': ['mysystemmonitor=mysystemmonitor.mysystemmonitor:main'],
},
python_requires=">= 3",
zip_safe=False)