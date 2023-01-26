from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.17'
DESCRIPTION = "Many useful groupby / itertools functions"

# Setting up
setup(
    name="group_and_iter_everything",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/group_and_iter_everything',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['check_if_nan', 'ctypes_window_info', 'divide_region_into_rectangles', 'flatten_any_dict_iterable_or_whatsoever', 'flatten_everything', 'intersection_grouper', 'isiter', 'locate_pixelcolor', 'numexpr', 'numpy', 'rect_intersection', 'regex', 'tolerant_isinstance', 'xxhash'],
    keywords=['itertools', 'groupby'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['check_if_nan', 'ctypes_window_info', 'divide_region_into_rectangles', 'flatten_any_dict_iterable_or_whatsoever', 'flatten_everything', 'intersection_grouper', 'isiter', 'locate_pixelcolor', 'numexpr', 'numpy', 'rect_intersection', 'regex', 'tolerant_isinstance', 'xxhash'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*