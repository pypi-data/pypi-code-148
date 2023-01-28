# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mercedestrenz', 'mercedestrenz.datasets', 'mercedestrenz.models']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.2.0,<5.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scikit-learn>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'mercedestrenz',
    'version': '0.2.2',
    'description': 'A package to inspect and analyze used Mercedes Benz car prices.',
    'long_description': '# mercedestrenz\n\nThis python package is for inspecting and analyzing used Mercedes Benz car prices. The package helps users to get simple answers on how to choose the used Mercedes Benz car in the market. The package also includes useful visualization tool and trained model to serve buyers and sellers.\n\n## Collaborators\n\nKelly Wu, Morris Zhao, Spencer Gerlach, Ty Andrews\n\n## Python ecosystem\n\nOur package is unique, it provides an easy way to investigate used Mercedes Benz car prices. It provide people a big picture about the market. The package relies on a real market data set to plot, filter and predict. It also gives advice to buyers and sellers when they try to make a decision.\n\n## Functions\n\nThe package contains the following functions:\n1. `load_sample_mercedes_listings`: Retrieves a data frame that contains sample data of used Mercedez Benz vehicles.\n2. `plot_mercedes_price`: Plot a density plot of a Mercedes-Benz model to see where the current vehicle\'s price falls for that same model in the market.\n3. `listing_search`: Retrieves the top listings that are within the budget range specified by the user.\n4. `predict_mercedes_price`: Predicts the price in USD of a Mercedes-Benz given the year, model, odometer reading, condition and paint color.\n\n## Package dataset\n\nThe package contains a static dataset for Craiglist used-car listings that were previously web scraped. Several key attributes about the used-car are available in the dataset, such as vehicle prices, models, car conditions, odometer readings, VINs, regions and transmission. The package\'s dataset was adapted from verison 10 of the raw dataset created by [AustinReese](https://github.com/AustinReese/UsedVehicleSearch).\n\n## Installation\n\n```bash\n$ pip install mercedestrenz\n```\n\n## Usage\n\nBelow is a basic example of how to use each of the four functions included in this package.\n\n```\n# Load all required package functions\nfrom mercedestrenz.data import load_sample_mercedes_listings, listing_search\nfrom mercedestrenz.modelling import train_mercedes_price_prediction_model\nfrom mercedestrenz.modelling import predict_mercedes_price\n\n# Load the sample mercedes listings data into a dataframe\ndata = load_sample_mercedes_listings()\n\n# Return the top listings that are within a budget range specified by the user. Returns a pandas dataframe of results.\nlisting_search(data, budget=[2000, 20000], model = "any", sort_feature = "odometer_mi", ascending = True)\n\n# Plot a price distribution of specific mercedes models, and see where an input price falls in the distribution.\nplot_mercedes_price(model=\'s-class\', price=80000, market_df=data))\n\n# Predict the price (in USD) of a Mercedes-Benz given the year, model, condition, paint color, and odometer reading.\npredict_mercedes_price("e-class", 2015, 55_000, "fair", "silver")\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`mercedestrenz` was created by Kelly Wu, Morris Zhao, Spencer Gerlach, Ty Andrews. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`mercedestrenz` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Ty Andrews',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
