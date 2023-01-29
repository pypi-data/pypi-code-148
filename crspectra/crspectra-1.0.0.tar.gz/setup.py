# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crspectra']

package_data = \
{'': ['*'], 'crspectra': ['data/*']}

install_requires = \
['numpy>=1.24.0,<2.0.0', 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'crspectra',
    'version': '1.0.0',
    'description': 'Database of published cosmic-ray energy spectra',
    'long_description': 'Cosmic-ray energy spectra\n=========================\n\nThis Python package provides a database of published cosmic-ray energy spectra,\nmeasured by surface detectors like *IceTop* or the *Pierre Auger Observatory*;\nsee references_. Moreover, it gives access to an `external database`_, which\nincludes electrons, positrons, anti-protons, and nuclide up to ``Z = 30`` for\nenergies below the cosmic-ray *knee*.\n\n\nInstallation\n------------\n\nThe easiest way to install this project is by using *pip*:\n\n.. code:: bash\n\n   pip install crspectra\n\n\nGetting started\n---------------\n\nThe measured cosmic-ray energy spectra can be requested via:\n\n.. code:: python\n\n   import crspectra\n\n   with crspectra.connect() as database:\n      for experiment in database:\n         spectrum = database[experiment]\n\nA structured *NumPy* array is returned containing the requested cosmic-ray\ndata. The fields are ``energy``, ``flux``, statistical ``stat`` and\nsystematical ``sys`` uncertainty on the flux, and uncertainty is upper a\nlimit ``uplim``. The energy is given in ``GeV`` and the flux is given\nin ``GeV^-1 m^-2 s^-1 sr^-1``. The uncertainties describe the lower and upper\nuncertainty relative to the flux.\n\nData from the `external database`_ can be requested via:\n\n.. code:: python\n\n   spectrum = crspectra.from_external("AMS-02")\n\nThe following plot was created using this package; see the `example`_ *Jupyter\nNotebook*:\n\n.. figure:: https://github.com/kkrings/crspectra/raw/main/example/crspectra.png\n\n\n.. _references:\n\nReferences\n----------\n\nPlease cite the following papers when using this database:\n\nAuger\n   The Pierre Auger Collaboration, Proceedings of the 35th International Cosmic\n   Ray Conference, Vol. ICRC2017, Proceedings of Science, 2017, p. 486\n\nCREAM-I/III\n   Yoon et al., The Astrophysical Journal 839.1 (2017), p. 5\n\nGAMMA\n   Ter-Antonyan, Physical Review D89.12 (2014), p. 123003\n\nHAWC\n   Alfaro et al., Physical Review D96.12 (2017), p. 12201\n\nHiRes/MIA\n   Abu-Zayyad et al., The Astrophysical Journal 557 (2001), pp. 686-699\n\nHiRes-I and HiRes-II\n   Abbasi et al., Physical Review Letters 100 (2008), p. 101101\n\nIceTop-73\n   Aartsen et al., Physical Review D88.4 (2013), p. 042004\n\nKASCADE\n   Antoni et al., Astroparticle Physics 24 (2005), pp. 1-25\n\nKASCADE-Grande\n   Apel et al., The Astrophysical Journal 36 (2012), pp. 183-194\n\nTibet-III\n   Amenomori et al., The Astrophysical Journal 678 (2008), pp. 1165-1179\n\n\nNotes\n-----\n\n   I have created this database in mid of 2017 when I started writing on my PhD\n   thesis. In case you find a publication with newer data, feel free to request\n   its addition.\n\n\n.. Links\n.. _external database:\n   http://lpsc.in2p3.fr/crdb/\n.. _example:\n   https://github.com/kkrings/crspectra/blob/main/example/crspectra.ipynb\n',
    'author': 'Kai Krings',
    'author_email': 'kai.krings@posteo.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kkrings/crspectra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
