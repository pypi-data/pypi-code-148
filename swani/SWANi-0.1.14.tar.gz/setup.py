# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 12:43:46 2022

@author: Maurilio
"""

#twine upload dist/*

from setuptools import setup, find_packages


setup(name='SWANi',
      version='0.1.14',
      description='Standardized Workflow for Advanced Neuroimaging',
      author='Maurilio Genovese',
      author_email='mauriliogenovese@gmail.com',
      #packages=['SWANi', 'SWANi.utils','SWANi.UI','SWANi.SWANiWorkflow','SWANi.SWANiSlicer'],
      packages=find_packages(
          where='src',
            include=['*'],  # alternatively: `exclude=['additional*']`
        ),
      package_dir={"": "src"},
      classifiers = [
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
      	"Operating System :: MacOS",
      	"Operating System :: POSIX :: Linux",
      ],
     license='MIT',
     install_requires = [
        "nipype",
        "Pyside6",
     	"pydicom",
     	"configparser",
     	"psutil",
         "pyshortcuts",
     	"SWANi_supplement>=0.0.4"
     ],
     python_requires=">=3.7",
     entry_points={
         'gui_scripts': [
            "SWANi = SWANi.__main__:main"
        ]
    }

    )
