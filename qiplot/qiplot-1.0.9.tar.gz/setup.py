from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()
setup(
    name='qiplot',
    version='1.0.9',
    description='Graphs in 1D and 2D',
    license='MIT',
    maintainer='steche',
    long_description=long_description,
    long_description_content_type='text/markdown',
    maintainer_email='schecchi@gmx.com',
    #include_package_data=True,     # If you have extra (non .py) data this should be set to True
    entry_points={'console_scripts': ['tqi=qiplot.plotdada:main', 'tqi2=qiplot.imageroi:main']},
    packages=find_packages(include=('qiplot', 'qiplot.*')),     # Where to look for the python package
    install_requires=[     # All Requirements
        'numpy',
        'pyqtgraph','PyQt5','matplotlib','h5py'
    ],
)


#
#Checklist to update version:
# 1) edit code
# 2) edit setup.py (increase version number)
# 3) cd to same level as setup.py
# 4) python -m build
# 5) twine upload dist/* --skip-existing


