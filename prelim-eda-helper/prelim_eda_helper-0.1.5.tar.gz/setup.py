# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['prelim_eda_helper']

package_data = \
{'': ['*']}

install_requires = \
['altair-data-server>=0.4.1,<0.5.0',
 'altair>=4.2.0',
 'numpy>=1.24.1,<2.0.0',
 'palmerpenguins>=0.1.4,<0.2.0',
 'pandas>=1.5.2,<2.0.0',
 'python-semantic-release>=7.33.0,<8.0.0',
 'scipy>=1.10.0,<2.0.0',
 'statistics>=1.0.3.5,<2.0.0.0',
 'tabulate>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'prelim-eda-helper',
    'version': '0.1.5',
    'description': 'A preliminary EDA helper.',
    'long_description': "# prelim_eda_helper\n\nThis package is a preliminary exploratory data analysis (EDA) tool to make useful feature EDA plots and provide relevant information to simplify an otherwise tedious EDA step of any data science project. Specifically this package allows users to target any two features, whether they are numeric or categorical, and create visualization plots supplemented with useful summary and test statistics.\n\nThis package provides a streamlined and easy to use solution for basic EDA tasks that would otherwise require significant amount of coding to achieve. Similar packages can be found published on [PyPi](https://pypi.org/search/?q=eda&page=1) such as the following:\n\n- [eda-viz](https://github.com/ajaymaity/eda-viz)\n- [QuickDA](https://github.com/sid-the-coder/QuickDA)\n\n`prelim_eda_helper` enables user to write quick visualization queries. At the same time, as we understand visually strong effects on graphs are not necessarily statistically meaningful, `prelim_eda_helper` is designed to combine graphic visualizations with preliminary statistical test results. We aim to create a helper package to really help researchers to get a quick sense of how our data look like, without making charts and doing tests separately in earlier stages of projects. We believe the combination of graphical and statistical output is what makes `prelim_eda_helper` a unique yet handy helper package.\n\nTo achive this goal, `prelim_eda_helper` creates charts with the visualization library [`altair`](https://altair-viz.github.io/) and conducts statistical tests with ['scipy'](https://scipy.org/).\n\n## Usage\n\n### Installation\n\n```bash\n$ pip install prelim_eda_helper\n```\n\n### `initialize_helper`\n\nEnables plotting data sets with more than 5000 rows.\n\n```py\ninitialize_helper()\n```\n\n### `num_dist_by_cat`\n\nCreates a pair of plots showing the distribution of the numeric variable when grouped by the categorical variable. Output includes a histogram and boxplot. In addition, basic test statistics will be provided for user reference.\n\n```py\nfrom prelim_eda_helper import num_dist_by_cat\nnum_dist_by_cat(num = 'x', cat = 'group', data = data, title_hist = 'Distribution of X', title_boxplot = 'X Seperated by Group', lab_num = 'X', lab_cat = 'Group', num_on_x = True, stat = True)\n```\n\n### `num_dist_scatter`\n\nCreates a scatter plot given two numerical variables. The plot can provide regression trendline and include confidence interval bands. Spearman and Pearson's correlation will also be returned to aid the user to determining feature relationship.\n\n```py\nfrom prelim_eda_helper import num_dist_scatter\nnum_dist_scatter(num1 = 'x', num2 = 'y', data = data, title = 'Scatter plot with X and Y', stat = False, trend = None)\n```\n\n### `cat_dist_heatmap`\n\nCreates concatenated charts showing the heatmap of two categorical variables and a barchart for occurrance of these variables.\n\n```py\nfrom prelim_eda_helper import cat_dist_heatmap\ncat_dist_heatmap(cat_1 = 'group1', cat_2 = 'group2', data = data, title = 'How are Group1 and Group2 distributed?', lab_1 = 'group1', lab_2 = 'group2', heatmap = True, barchart = True)\n```\n\n### `num_dist_summary`\n\nCreates a distribution plot of the given numeric variable and provides a statistical summary of the feature. In addition, the correlation values of the variable with other numeric features will be provided based on a given threshold.\n\n```py\nfrom prelim_eda_helper import num_dist_summary\nnum_dist_summary(num = 'x', data = data, title = 'Distribution of X', lab = 'X', thresh_corr = 0.0, stat = True )\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`prelim_eda_helper` was created by Mehwish Nabi, Morris Chan, Xinry LU, Austin Shih. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`prelim_eda_helper` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'Mehwish, Man Fung Morris CHAN, Xinru LU, Austin SHIH',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
