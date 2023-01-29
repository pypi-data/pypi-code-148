from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Use Pandas to find and interact with handles, windows, and elements"

# Setting up
setup(
    name="pdwinauto",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/pdwinauto',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['a_cv_imwrite_imread_plus', 'a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_automate_win32', 'a_pandas_ex_horizontal_explode', 'a_pandas_ex_loc_no_exceptions', 'comtypes', 'ctypes_window_info', 'ctypes_windows', 'files_folders_with_timestamp', 'flatten_everything', 'flexible_partial', 'kthread_sleep', 'mousekey', 'mss', 'numpy', 'pandas', 'PrettyColorPrinter', 'six'],
    keywords=['automation', 'pandas', 'pyautogui', 'pywinauto'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['a_cv_imwrite_imread_plus', 'a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_automate_win32', 'a_pandas_ex_horizontal_explode', 'a_pandas_ex_loc_no_exceptions', 'comtypes', 'ctypes_window_info', 'ctypes_windows', 'files_folders_with_timestamp', 'flatten_everything', 'flexible_partial', 'kthread_sleep', 'mousekey', 'mss', 'numpy', 'pandas', 'PrettyColorPrinter', 'six'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*