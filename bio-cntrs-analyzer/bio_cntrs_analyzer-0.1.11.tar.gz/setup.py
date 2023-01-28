# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bcanalyzer',
 'bcanalyzer.common',
 'bcanalyzer.gui.controllers',
 'bcanalyzer.gui.models',
 'bcanalyzer.gui.views',
 'bcanalyzer.gui.widgets',
 'bcanalyzer.image_processing']

package_data = \
{'': ['*'], 'bcanalyzer': ['gui/resources/*']}

install_requires = \
['PyQt5',
 'appdirs',
 'filetype',
 'numpy>=1.19.0,<2.0.0',
 'opencv-python-headless',
 'opencv-python>=4.5,<5.0',
 'pandas',
 'scipy',
 'sdd-segmentation']

entry_points = \
{'console_scripts': ['bcanalyzer = bcanalyzer.app:main']}

setup_kwargs = {
    'name': 'bio-cntrs-analyzer',
    'version': '0.1.11',
    'description': 'The semi-automatic segmentation and quantification of patchy areas in various biomedical images based on the assessment of their local edge densities.',
    'long_description': '# BCAnalyzer: Segmentation of patchy areas in biomedical images based on local edge density estimation\n\n## Installation\n\n### Download executable from release page\n \nWe provide a builded windows executable file for every release. You can find the latest whl or exe file on the [release page](https://gitlab.com/digiratory/biomedimaging/bcanalyzer/-/releases). Also, you can find all versions of windows execution files in the [archive](https://drive.digiratory.ru/d/s/nCQF5QKnlOoLyvoogzIMazY5YAOZDDmy/hY8ac89PJtnKtduC6w9CEkRtLVVRmZ4_-qbCgo_pvPwk).\n\n\n### Installation from binaries\n\n```bash\npip install -U bio-cntrs-analyzer\n```\n### Build exe from source\n\nFrom venv:\n\n```bash\npip install cx_Freeze\npython setup.py build\n```\n\n## User manual\n\nFor starting appliation evualate in command line (terminal) the next command:\n\n```bash\nbcanalyzer\n```\n\n![UserManualFigure](https://gitlab.com/digiratory/biomedimaging/bcanalyzer/-/raw/main/images/UserManualFigure.PNG) \n\nSoftware user interface outline: (A) list of images submitted for the analysis; (B) segmentation algorithm options, including (C) color channel import options; (D) selected image with on-the-fly visualization of the segmentation results; (E) segmentation algorithm controls for the online adjustment of its sensitivity and resolution; (F) file export menu.\n\nThe typical algorithm of user interaction with the software is as follows:\n\n* Selected images are imported by their drag-and-drop onto the program window. The image list appears in **A**.\n* Global algorithm options can be adjusted in **B** and color channels for the analysis selected in **C**.  \n* The image selected in the list **A** is displayed in the panel **D** with immediate visualization of the segmentation results (using default parameters during the first run).\n* Next the algorithm parameters (sensitivity and resolution) can be adjusted manually in **E**, given that the automated threshold option is disabled, although one can also apply the automated threshold selection for the first approach and then disable it in order to proceed with manual fine tuning. Segmentation results are visualized on-the-fly for direct user control. Of note, global options and color channel selection can be readjusted at this stage as well. Following necessary adjustments, the chosen algorithm parameters can be applied either to the entire imported image set, or solely to the currently analyzed image, with corresponding controls available in **E**.\n* Once the algorithm parameters are adjusted either for a single or for a few representative image(s), further processing and export can be performed as a fully automated procedure for the entire image set using file export options in **F**. Export options include visualizations of segmentation results, either as binary masks or as marked-up images similar to those appearing on the screen during the analysis, or both of them, as well as a *.csv table with summary statistics.\n\n# Dataset\n\nLink to downloading dataset:\n\nhttps://drive.digiratory.ru/d/s/mrbRyk4HyFbOIEANc6DhQGxhCFNgq3xI/Jqbcbsq_eE5Cf8-bnJaM3dXL6RI1v7d7-d74AOY4RLgk\n\nIf something goes wrong, please, write to amsinitca[at]etu.ru\n\n# Troubleshooting\n\n## qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.\n\n### Problem\n\n```bash\nqt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.\nThis application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.\nAvailable platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.\nAborted (core dumped)\n```\n\n### Solution\n\n```bash\nsudo apt-get install libxcb-xinerama0\n```\n\n# Citation\n\nIf you find this project useful, please cite:\n\n```bib\n@article{SINITCA2023104189,\n    title = {Segmentation of patchy areas in biomedical images based on local edge density estimation},\n    journal = {Biomedical Signal Processing and Control},\n    volume = {79},\n    pages = {104189},\n    year = {2023},\n    issn = {1746-8094},\n    doi = {https://doi.org/10.1016/j.bspc.2022.104189},\n    url = {https://www.sciencedirect.com/science/article/pii/S1746809422006437},\n    author = {Aleksandr M. Sinitca and Airat R. Kayumov and Pavel V. Zelenikhin and Andrey G. Porfiriev and Dmitrii I. Kaplun and Mikhail I. Bogachev},\n}\n```\n\n',
    'author': 'Aleksandr Sinitca',
    'author_email': 'amsinitca@etu.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/digiratory/biomedimaging/bcanalyzer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
