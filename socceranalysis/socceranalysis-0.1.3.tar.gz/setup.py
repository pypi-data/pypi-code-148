# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['socceranalysis']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.2.0',
 'display>=1.0.0,<2.0.0',
 'ipython>=8.8.0,<9.0.0',
 'matplotlib>=3.6.3',
 'numpy>=1.24.1',
 'openpyxl>=3.0.10',
 'pandas>=1.5.2',
 'panel>=0.14.2,<0.15.0',
 'python-semantic-release>=7.33.0,<8.0.0']

setup_kwargs = {
    'name': 'socceranalysis',
    'version': '0.1.3',
    'description': 'Doing soccer stats analysis.',
    'long_description': '[![docs](https://img.shields.io/docsrs/passing)](https://soccer-analysis-python.readthedocs.io/en/latest/)\n\n# socceranalysis\n\nsocceranalysis is a powerful Python package designed to make it easy to analyze and understand soccer statistics. With its set of functions, you can quickly obtain summary statistics for a particular team, identify outliers based on market value, rank players by goals per game and display different plots. The package is built in a way that allows user to easily customize the functions to their own interests, giving them the flexibility to analyze the data in a way that is most meaningful to them. Whether you\'re a coach, a sports journalist or an analyst, socceranalysis will help you unlock the insights hidden in your soccer data and make more informed decisions.\n\n## Functions\n\n\n1. `find_team_stat`: provides a quick and easy way to understand the descriptive statistics of a team. (https://github.com/UBC-MDS/socceranalysis_python/blob/main/src/socceranalysis/find_team_stat.py) \n\n2. `rankingplayers`:  Ranks players based on specific attributes (https://github.com/UBC-MDS/socceranalysis_python/blob/main/src/socceranalysis/playerranking.py)\n\n3. `get_outliers`: Identifes outliers using statistical methods (interquartile range or standard deviations) (https://github.com/UBC-MDS/socceranalysis_python/blob/main/src/socceranalysis/outlier_identification.py)\n\n4. `soc_viz_stats` :  Generates meaningful visualizations to help users understand and interpret the data (https://github.com/UBC-MDS/socceranalysis_python/blob/main/src/socceranalysis/viz_stats.py)\n* `soc_viz_stats_scatter` : Generate a scatter plot for two given numeric columns with a slider to control age \n* `soc_viz_stats_hist` :  Generate a histogram for one given numeric columns\n\n\n\n## Python ecosystem\nsocceranalysis can be used in conjunction with other popular Python packages such as [pandas](https://github.com/pandas-dev/pandas) and [scikit-learn](https://github.com/scikit-learn/scikit-learn) to perform more advanced data analysis and machine learning tasks. For example, users can use pandas to manipulate and clean their soccer data, and then use this package to perform specific soccer-related analysis on the cleaned data. Additionally, socceranalysis can be used in conjunction with scikit-learn for machine learning tasks on soccer data. They are designed to be a higher-level, more user-friendly and declarative interface based on [Altair](https://github.com/altair-viz/altair) for performing specific soccer-related analysis and visualization tasks. Users can perform similar visualization using [matplotlib](https://github.com/matplotlib/matplotlib). Overall, socceranalysis is a valuable addition to the Python ecosystem as it provides a specialized tool for analyzing and understanding soccer data without the need for writing complex code, this can be especially useful for users who may not have extensive experience with data analysis or visualization.\n\n\n\n## Installation\n\n```bash\n$ pip install socceranalysis\n\n# directly from test pypi\n$ pip install -i https://test.pypi.org/simple/ socceranalysis\n```\n\n## Usage\n\n\n###  find_team_stat\n```bash\nfrom socceranalysis.find_team_stat import *\ndata = pd.read_excel(\'soccer_data.xlsx\')\nfind_team_stat(data , "Manchester United", "Market_Value_Euros")\n```\n### get_outliers\n```bash \ndata = pd.read_excel(\'soccer_data.xlsx\')\nfrom  socceranalysis.outlier_identification import get_outliers\nget_outliers(data,"Wages_Euros","SD",3)\n```\n###  soc_viz_stats\n\n```bash\nfrom socceranalysis.viz_stats import *\n\n# scatter plots of two given columns\nsoc_viz_stats_scatter(\'age\',\'Goals_total\', data)\n# histogram of one given column\nsoc_viz_stats_hist(\'age\', data)\n```\n### playerranking\n```bash\nfrom socceranalysis.rankingplayers import *\ndata = pd.read_excel(\'soccer_data.xlsx\')\nrankingplayers(data, "Goals_total", "Assists_Total")\n```\n\n## Contributors\n\n|  \t Core contributor| Github.com username| \n|---------|---|\n|  Flora Ouedraogo |  @florawendy19 | \n|  Gaoxiang Wang |  @louiewang820 | \n|  Manvir Kohli | @manvirsingh96 |\n| Vincent Ho | @vincentho32 |\n\n## Contributing\n\nAuthors: Vincent Ho, Manvir Singh Kohli, Gaoxiang Wang, Flora Ouedraogo.\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`socceranalysis` was created by Gaoxiang Wang, Manvir Kohli, Vincent Ho and Flora Ouedraogo. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`socceranalysis` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Group 15 ',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/UBC-MDS/socceranalysis_python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
