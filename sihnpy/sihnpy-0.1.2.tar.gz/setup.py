# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sihnpy',
 'sihnpy.data',
 'sihnpy.data.fingerprinting',
 'sihnpy.data.pad_conp_minimal']

package_data = \
{'': ['*'],
 'sihnpy.data.fingerprinting': ['matrices_simulated_mod1/*',
                                'matrices_simulated_mod2/*'],
 'sihnpy.data.pad_conp_minimal': ['BL00/encoding/*',
                                  'BL00/rest_run1/*',
                                  'BL00/rest_run2/*',
                                  'BL00/retrieval/*',
                                  'FU12/encoding/*',
                                  'FU12/rest_run1/*',
                                  'FU12/rest_run2/*',
                                  'FU12/retrieval/*']}

install_requires = \
['numpy>=1.23.1,<2.0.0', 'pandas>=1.4.3,<2.0.0', 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'sihnpy',
    'version': '0.1.2',
    'description': 'Study of inter-individual heterogeneity of neuroimaging in Python (SIHNpy)',
    'long_description': '# `sihnpy`: *S*tudy of *I*nter-individual *H*eterogeneity of *N*euroimaging in *Py*thon\n\n![sihnpy logo](docs/images/sihnpy_logo_large_no_bg.png)\n\n**Hi! Welcome to `sihnpy`!**\n\nA critical ongoing issue in science is the lack of diversity in our study populations: some groups of individuals are often under-represented, if represented at all. This becomes particularly critical when considering health research. **How can we know that a drug tested in a specific population will work in a slightly different population? How can we know that symptoms for a given disease will present in the same way if we study a slightly different population?** \n\nThat\'s not all. Even when we take a group of individuals that are traditionally considered to be quite homogenous (let\'s say young adults), we are realizing that **their brains are actually quite different from one another**.[^Mueller_2013],[^Finn_2015] This goes hand-in-hand with the new wave of personalized medicine ideology: if everyone has different circumstances and backgrounds, shouldn\'t we personalize how we conduct research? But this is also difficult to pursue as most of the traditional statistical analyses we have are made to **compare groups** or to **observe a variable within a single group.**\n\n**This is where `sihnpy` comes in.** My goal was to provide researchers with an easy-to-use, one-stop-shop for simple methods aimed at studying inter-individual differences. During my PhD, I focused on using methods that could help us better understand these differences, or at the very least, offer more diversity in the way we can study a "traditionally" homogenous group.\n\nNeuroscientist by training, most of the tools I develop in `sihnpy` are neuroimaging-focused. That said, with a few exceptions, the tools should also be useable in other domains. Also, I am not a computer scientist, but I really love coding and I am eagerly learning as I develop `sihnpy`. If something is not working right, feel free to [open an issue](https://github.com/stong3/sihnpy/issues) to let me know or to discuss how I can improve `sihnpy`.\n\n## Authors\n- Frédéric St-Onge - MSc - PhD candidate at McGill University\n- Gabriel St-Onge - MSc\n\nIf you use `sinhpy` in your academic work (or well, any other work where you would need such a package), please consider citing the paper detailing the development of the first few modules of this package and/or citing the package (example below in APA form):\n\n- St-Onge F, Javanray M, Pichet Binette A, Strikwerda-Brown C, Remz J, Spreng RN, Shafiei G, Misic B, Vachon-Presseau E, Villeneuve S. (2023) Functional connectome fingerprinting across the lifespan. Under review.\n- St-Onge F & St-Onge G (2022). sihnpy: Study of Inter-individual Heterogeneity of Neuroimaging in Python. v[VERSION HERE], URL: https://github.com/stong3/sihnpy\n\n## Installation\n\nYou can install the most recent version of `sinhpy` using pip:\n\n```bash\n$ pip install sihnpy\n```\n\n## Usage\n\nThe package is separated in distinct modules with their own rationale, explanation, use cases and limitations. Please visit the documentation for specific information on each module. Below is a quick summary of each available module:\n\n   - Datasets: Contains a subset of the Prevent-AD Open data which can be used to test functionalities of the package\n   - Fingerprinting: Computes individual-specific signatures of variables and the related metrics\n\nWhile I try my best to simplify the concepts as much as possible, note that **an understanding of Python\'s basics is probably necessary** to run most of the modules.\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`sihnpy` was created by Frédéric St-Onge. It is licensed under the terms of the MIT license.\n\nNote that `sihnpy` is shipped with a small subset of the [Prevent-AD dataset](https://portal.conp.ca/dataset?id=projects/preventad-open-bids). These data are provided in open access through the generosity and hard work of the SToP-AD center at the Douglas Mental Health University Institute affiliated with McGill University, Montreal, Canada. Using these data to test the functionalities of the software is encouraged. However, users using the `datasets` module agree to the terms of use of the Prevent-AD dataset (see [License](license.md) for more information).\n\n## Credits\n\nThe package was developed in part from the input of members from the [VilleneuveLab](http://www.villeneuvelab.com/en/home/). Come see the awesome work we do on aging and Alzheimer\'s disease!\n\n`sihnpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter). This package was developped alongside my reading of the book *Python packages*, an open-source book written by Tomas Beuzen & Tiffany Timbers, available [here](https://py-pkgs.org/welcome).\n\nThe logo of the package used a [copyright-free image from Pixabay](https://pixabay.com/vectors/snake-animal-line-art-serpent-6158325/) created by the user StarGlade, which was modified to create `sihnpy`\'s logo.\n\nWe thank the [Prevent-AD cohort](https://douglas.research.mcgill.ca/prevent-alzheimer-program/) coordinating team from the [SToP-Alzheimer Center](https://douglas.research.mcgill.ca/stop-ad-centre/) at the [Douglas Mental Health University Institute](https://douglas.research.mcgill.ca/) affiliated with [McGill University](https://www.mcgill.ca/) as they are responsible for the data collection. Special thanks to Jennifer Tremblay-Mercier, coordinator at the SToP-Alzheimer center, and Dr. Sylvia Villeneuve, director of the SToP-Alzheimer center, for allowing the sharing of the data. Importantly, we would also like to thank the participants of the Prevent-AD cohort, without whom we would not be able to have these data.\n\nThe download of the data was made possible by the support from the [Canadian Open Neuroscience Platform (CONP)](https://conp.ca), which is currently storing the data for open access. The CONP is funded in part by [Brain Canada](https://braincanada.ca/), in partnership with [Health Canada](https://www.canada.ca/en/health-canada.html).\n\nWe also acknowledge the support received by Calcul Québec and the Digital Research Alliance of Canada (DRAC) in the development of `sihnpy`. Many of the functionalities in `sihnpy` were tested and developped on a high performance computing environment such as [Beluga](https://www.calculquebec.ca/en/communiques/beluga-a-supercomputer-for-science-2/). The preprocessing and storage of the Prevent-AD data available in `sihnpy` was also executed on Beluga.\n\nI was also financially supported by the Fonds de Recherche du Québec - Santé, the Healthy Brains for Healthy Lives initiative and Mitacs at different point during my studies and the development of this software. \n\nThe funding organizations mentioned above did not participate in the decision making process involved in the development of the software.\n\n## References\n\n[^Mueller_2013]: Mueller et al. (2013). Neuron. [10.1016/j.neuron.2012.12.028](https://doi.org/10.1016/j.neuron.2012.12.028)\n[^Finn_2015]: Finn et al. (2015). Nat Neuro. [10.1038/nn.4135](https://doi.org/10.1038/nn.4135)',
    'author': 'Frederic St-Onge',
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
