# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vpt',
 'vpt.app',
 'vpt.compile_tile_segmentation',
 'vpt.convert_geometry',
 'vpt.convert_geometry.converters',
 'vpt.convert_to_ome',
 'vpt.derive_cell_metadata',
 'vpt.filesystem',
 'vpt.partition_transcripts',
 'vpt.prepare_segmentation',
 'vpt.run_segmentation',
 'vpt.run_segmentation_on_tile',
 'vpt.segmentation',
 'vpt.segmentation.cellpose',
 'vpt.segmentation.filters',
 'vpt.segmentation.stardist',
 'vpt.segmentation.utils',
 'vpt.segmentation.watershed',
 'vpt.sum_signals',
 'vpt.update_vzg',
 'vpt.update_vzg.assemble',
 'vpt.update_vzg.polygons',
 'vpt.utils',
 'vpt.utils.seg_json_generator']

package_data = \
{'': ['*'], 'vpt.utils.seg_json_generator': ['templates/*']}

install_requires = \
['boto3==1.17',
 'cellpose==1.0.2',
 'dask==2022.9.0',
 'distributed==2022.9.0',
 'fsspec==2021.10.0',
 'gcsfs==2021.10.0',
 'geojson==2.5.0',
 'geopandas==0.12.1',
 'h5py==3.7.0',
 'numpy==1.22.4',
 'opencv-python-headless==4.6.0.66',
 'pandas==1.4.3',
 'pyarrow==8.0.0',
 'pyclustering==0.10.1.2',
 'python-dotenv==0.20.0',
 'pyvips==2.2.1',
 'rasterio==1.3.0',
 's3fs==2021.10.0',
 'scikit-image==0.19.3',
 'scipy==1.8.1',
 'shapely==2.0',
 'stardist==0.8.3',
 'tensorflow==2.9.1']

entry_points = \
{'console_scripts': ['vpt = vpt.vizgen_postprocess:entry_point']}

setup_kwargs = {
    'name': 'vpt',
    'version': '1.0.1',
    'description': 'Command line tool for highly parallelized processing of Vizgen data',
    'long_description': '[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n![PyPI](https://img.shields.io/pypi/v/vpt)\n[![Coverage Status](https://coveralls.io/repos/github/Vizgen/vizgen-postprocessing/badge.svg?branch=develop&t=EsWr25)](https://coveralls.io/github/Vizgen/vizgen-postprocessing?branch=develop)\n\n# Vizgen Post-processing Tool\n\nThe Vizgen Post-processing Tool (VPT) enables users to reprocess and refine the single-cell results of MERSCOPE experiments. \nVPT is a command line tool that emphasizes scalable, reproducible analysis, and can be run on a workstation, a cluster, or \nbe deployed in a cloud computing environment.\n\n\n## Features\n- Perform cell segmentation\n    - Reproduce standard Vizgen segmentation options\n    - Perform reproducible custom segmentation\n- Import cell segmentation from other tools\n    - Supports geojson and hdf5 formats\n- Regenerate single cell data with new segmentation\n    - Cell by gene matrix\n    - Cell spatial metadata\n    - Image intensity in each cell\n    - Update MERSCOPE Vizualizer file (vzg)\n- Image format conversion\n    - Convert large tiff files to single or multi-channel Pyramidal OME-TIFF files\n- Nextflow compatible, example pipeline provided\n\n\n## Installation\n\nInstall the tool through your choice of \n- [pip](https://pip.pypa.io/en/stable/getting-started/)\n- [Docker](https://docs.docker.com/desktop/extensions-sdk/quickstart/)\n- [poetry](https://python-poetry.org/)\n\nTo access in-utility help documentation run the process below in the installed environment.\n```bash\n  vpt --help\n```\n    \n## Usage\n\nVPT accepts two types of inputs to specify how to run segmentation:\n- Command line parameters\n    - relate to where to find the input data and are expected to vary with each experiment\n- Segmentation algorithm .json file parameters\n    - describes a series of steps to perform on the input data\n\nUsing the same segmentation algorithm on a series of experiments ensures that they are processed identically and reproducibly.\n\nIn addition to the user guide, several working segmentation algorithm .json files are provided that can serve either as a \nrobust segmentation definition or as a template for a custom workflow.\n\n## Quick start commands:\n\n\nrun-segmentation    \u200b\n- Top-level interface for vpt which invokes the segmentation functionality of the tool.\u200b\n\nprepare-segmentation\u200b\n - Generates a segmentation specification json file to be used for cell segmentation tasks. \u200b\n\nrun-segmentation-on-tile\u200b\n - Executes the segmentation algorithm on a specific tile of the mosaic images.\u200b\n\ncompile-tile-segmentation\u200b\n- Combines the per-tile segmentation outputs into a single, internally-consistent parquet file containing all of the \nsegmentation boundaries found in the experiment.\u200b\n\nderive-entity-metadata\u200b\n- Uses the segmentation boundaries to calculate the geometric attributes of each Entity\u200b\n\npartition-transcripts\u200b\n- Uses the segmentation boundaries to determine which Entity, if any, contains each detected transcript.\u200b\n\nsum-signals\u200b\n- Uses the segmentation boundaries to find the intensity of each mosaic image in each Entity.\u200b\n\nupdate-vzg\u200b\n- Updates an existing .vzg file with new segmentation boundaries and the corresponding expression matrix.\u200b\n\nconvert-geometry\u200b\n- Converts Entity boundaries produced by a different tool into a vpt compatible parquet file.\u200b\n\nconvert-to-ome\u200b\n- Transforms the large 16-bit mosaic tiff images produced by the MERSCOPE into a OME pyramidal tiff.\u200b\n\nconvert-to-rgb-ome\u200b\n- Converts up to three flat tiff images into rgb OME-tiff pyramidal images.\u200b\n\nFor more detail on commands and arguments, please see the user guide.\n\n## Documentation\n\n[User Guide](https://vizgen.github.io/vizgen-postprocessing/)\n\n## Feedback\n\nIf you encounter issues or bugs, let us know by [submitting an issue!](https://github.com/Vizgen/vizgen-postprocessing/issues)\nPlease include:\n\n- A quick issue summary\n- Steps that caused it to occur\n- The exception generated by the code, if applicable\n- Specific lines of code, if indicated in the error message\n\n\nIf you have any other feedback or issues, please reach out to your regional Vizgen field application scientist and CC: Vizgen \nTech Support at techsupport@vizgen.com.\n\nPlease include VPT in your subject line along with the above information in the body.\n\n## Contributing & Code of Conduct\n\nWe welcome code contributions! Please refer to the [contribution guide](CONTRIBUTING.md) before getting started.\n\n## Authors\n\n- [Vizgen](https://vizgen.com/)\n\n![Logo](https://vizgen.com/wp-content/uploads/2022/12/Vizgen-Logo_Vizgen-BlackColor-.png)\n\n## License\n\n   Copyright 2022 Vizgen, Inc. All Rights Reserved\n   \n   Licensed under the Apache License, Version 2.0 (the "License");\n   you may not use this file except in compliance with the License.\n   You may obtain a copy of the License at\n\n       http://www.apache.org/licenses/LICENSE-2.0\n\n   Unless required by applicable law or agreed to in writing, software\n   distributed under the License is distributed on an "AS IS" BASIS,\n   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n   See the License for the specific language governing permissions and\n   limitations under the License.\n',
    'author': 'Vizgen',
    'author_email': 'techsupport@vizgen.com',
    'maintainer': 'Timothy Wiggin',
    'maintainer_email': 'timothy.wiggin@vizgen.com',
    'url': 'https://github.com/Vizgen/vizgen-postprocessing',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
