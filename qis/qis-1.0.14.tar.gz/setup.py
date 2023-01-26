# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qis',
 'qis.examples',
 'qis.models',
 'qis.models.linear',
 'qis.models.stats',
 'qis.perfstats',
 'qis.plots',
 'qis.plots.derived',
 'qis.portfolio',
 'qis.portfolio.optimization',
 'qis.portfolio.reports',
 'qis.portfolio.strats',
 'qis.utils']

package_data = \
{'': ['*'], 'qis.examples': ['figures/*']}

install_requires = \
['PyYAML>=6.0',
 'SQLAlchemy>=1.4.46',
 'easydev>=0.12.0',
 'fsspec>=2022.11.0',
 'matplotlib>=3.2.2',
 'numba>=0.56.4',
 'numpy>=1.22.4',
 'pandas>=1.5.2',
 'psycopg2>=2.9.5',
 'pyarrow>=10.0.1',
 'scipy>=1.10',
 'seaborn>=0.12.2',
 'statsmodels>=0.13.5',
 'tabulate>=0.9.0',
 'yfinance>0.1.38']

setup_kwargs = {
    'name': 'qis',
    'version': '1.0.14',
    'description': 'Implementation of visualisation and reporting analytics for Quantitative Investment Strategies',
    'long_description': '\n<strong>QIS: Quantitative Investment Strategies</strong>\n\nThe package implements analytics for visualisation of financial data, performance\nreporting, analysis of quantitative strategies. \n\n# Table of contents\n1. [Installation](#installation)\n2. [Analytics](#analytics)\n3. [Disclaimer](#disclaimer)    \n4. [Contributions](#contributions)\n5. [Examples](#examples)\n   1. [Visualization of price data](#price)\n6. [ToDos](#todos)\n\n## **Installation** <a name="installation"></a>\n```python \npip install qis\n```\n```python \npip install --upgrade qis\n```\n\nCore dependencies:\n    python = ">=3.8,<3.11",\n    numba = ">=0.56.4",\n    numpy = ">=1.22.4",\n    scipy = ">=1.10",\n    statsmodels = ">=0.13.5",\n    pandas = ">=1.5.2",\n    matplotlib = ">=3.2.2",\n    seaborn = ">=0.12.2",\n    yfinance >= 0.1.38 (optional for getting test price data).\n\n## **Analytics** <a name="analytics"></a>\n\nThe QIS package is split into 5 main modules with the \ndependecy path increasing sequentially as follows.\n\n1. ```qis.utils``` is module containing low level utilities for operations with pandas, numpy, and datetimes.\n\n2. ```qis.perfstats``` is module for computing performance statistics and performance attribution including returns, volatilities, etc.\n\n3. ```qis.plots``` is module for plotting and visualization apis.\n\n4. ```qis.models``` is module containing statistical models including filtering and regressions.\n\n5. ```qis.portfolio``` is high level module for analysis, simulation, backtesting, and reporting of quant strategies.\n\n```qis.examples``` contains scripts with illustrations of QIS analytics.\n\n## **Disclaimer** <a name="disclaimer"></a>\n\nQIS package is distributed FREE & WITHOUT ANY WARRANTY under the GNU GENERAL PUBLIC LICENSE.\n\nSee the [LICENSE.txt](https://github.com/ArturSepp/QuantInvestStrats/blob/master/LICENSE.txt) in the release for details.\n\nPlease report any bugs or suggestions by opening an [issue](https://github.com/ArturSepp/QuantInvestStrats/issues).\n\n## **Contributions** <a name="contributions"></a>\nIf you are interested in extending and improving QIS analytics, \nplease consider contributing to the library.\n\nI have found it is a good practice to isolate general purpose and low level analytics and visualizations, which can be outsourced and shared, while keeping \nthe focus on developing high level commercial applications.\n\nThere are a number of requirements:\n\n- The code is [Pep 8 compliant](https://peps.python.org/pep-0008/)\n\n- Reliance on common Python data types including numpy arrays, pandas, and dataclasses.\n\n- Transparent naming of functions and data types with enough comments. Type annotations of functions and arguments is a must.\n\n- Each submodule has a unit test for core functions and a localised entry point to core functions.\n\n- Avoid "super" pythonic constructions. Readability is the priority.\n\n## **Examples** <a name="examples"></a>\n\n### Visualization of price data <a name="price"></a>\n\nThe script is located in ```qis.examples.performances```\n\n```python \nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport yfinance as yf\nimport qis\nfrom qis import PerfStat\n\n# define tickers and fetch price data\ntickers = [\'SPY\', \'QQQ\', \'EEM\', \'TLT\', \'IEF\', \'LQD\', \'HYG\', \'GLD\']\nprices = yf.download(tickers, start=None, end=None)[\'Adj Close\'][tickers].dropna()\n\n# plotting price data with minimum usage\nfig = qis.plot_prices(prices=prices)\n```\n![image info](qis/examples/figures/perf1.PNG)\n```python \n# 2-axis plot with drawdowns using sns styles\nwith sns.axes_style("darkgrid"):\n    fig, axs = plt.subplots(2, 1, figsize=(10, 7))\n    qis.plot_prices_with_dd(prices=prices, axs=axs)\n```\n![image info](qis/examples/figures/perf2.PNG)\n```python \n# plot risk-adjusted performance table with excess Sharpe ratio\nust_3m_rate = yf.download(\'^IRX\', start=None, end=None)[\'Adj Close\'].dropna() / 100.0\n# set parameters for computing performance stats including returns vols and regressions\nperf_params = qis.PerfParams(freq=\'M\', freq_reg=\'Q\', rates_data=ust_3m_rate)\nfig = qis.plot_ra_perf_table(prices=prices,\n                             perf_columns=[PerfStat.TOTAL_RETURN, PerfStat.PA_RETURN, PerfStat.VOL, PerfStat.SHARPE,\n                                           PerfStat.SHARPE_EXCESS, PerfStat.MAX_DD, PerfStat.MAX_DD_VOL,\n                                           PerfStat.SKEWNESS, PerfStat.KURTOSIS],\n                             title=f"Risk-adjusted performance: {qis.get_time_period_label(prices, date_separator=\'-\')}",\n                             perf_params=perf_params)\n```\n![image info](qis/examples/figures/perf3.PNG)\n\n## **ToDos and Contributions** <a name="todos"></a>\n\n1. Enhanced documentation and readme examples.\n\n2. Docstrings for key functions.\n\n3. Reporting analytics and factsheets generation enhancing to matplotlib.\n\n',
    'author': 'Artur Sepp',
    'author_email': 'artursepp@gmail.com',
    'maintainer': 'Artur Sepp',
    'maintainer_email': 'artursepp@gmail.com',
    'url': 'https://github.com/ArturSepp/QuantInvestStrats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
