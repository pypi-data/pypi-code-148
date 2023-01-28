from setuptools import setup, find_packages

setup(
    name='spj_grader',
    version='0.3.3',
    license='MIT',
    description = '101-Code Grader',   
    author="Somchai P.",
    author_email='somchai.p@chula.ac.th',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords=['spj_grader', 'grader'],
    install_requires=[
          'black',
          'diff_match_patch',
          'editdistance',
          'numpy',
    ],

)
