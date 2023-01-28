# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinr']

package_data = \
{'': ['*'], 'pinr': ['templates/*']}

install_requires = \
['colormath>=3.0.0,<4.0.0',
 'dicom2nifti>=2.4.7,<3.0.0',
 'fhir-resources[all]>=6.5.0,<7.0.0',
 'highdicom>=0.20.0,<0.21.0',
 'nibabel>=5.0.0,<6.0.0',
 'nilearn>=0.10.0,<0.11.0',
 'pandas>=1.5.2,<2.0.0',
 'pydicom>=2.3.1,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pinr = pinr.__main__:app']}

setup_kwargs = {
    'name': 'pinr',
    'version': '0.1.1',
    'description': 'Python tools for Interoperable Neuromorphometry Reporting',
    'long_description': '# Python tools for Interoperable Neuromorphometry Reporting\nPython tools for Interoperable Neuromorphometry Reporting (`pinr`) allows for the creation of DICOM Structured Reporting Documents and FHIR Diagnostic Report resources from a T1w image processed by the [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) neuroimaging software suite.\n\nCurrently, only [`aseg.mgz`](http://surfer.nmr.mgh.harvard.edu/fswiki/SubcorticalSegmentation/) and `aseg.stats`  are supported and documented. Future versions may support other FreeSurfer segmentations and parcellations (such as thickness and volumes of different cortical regions).\n\nDICOM conversion uses the [highdicom](https://github.com/ImagingDataCommons/highdicom) package, and FHIR JSON files are created with [fhir.resources](https://github.com/nazrulworld/fhir.resources/tree/main).\n\nFor each label in the segmentation, a DICOM TID 300 "Measurement" object is created, and each Measurement is contained in a TID 1411 "Volumetric ROI Measurements and Qualitative Evaluations" object. The set of all labels are contained in a "Imaging  Measurement Report" object.\n\nFHIR output is in the form of a `DiagnosticReport` Resource, consisting of `Observation` Resources for each measurement. Specifically, each DICOM TID 300 object is mapped to a "Imaging Measurement" `Observation`, and each "Imaging Measurement" is contained within a "Imaging Measurement Group" `Observation` (analogous to a TID 1411 DICOM object). The "Imaging Measurement Groups" are contained within the `DiagnosticReport`.\n\nThe mapping of DICOM SR to FHIR Resource follows the work of the HL7 Imaging Interegration Work Group. Details are provided [here](https://github.com/HL7/dicom-sr), with architecture information provided within this [Implementation Guide](https://build.fhir.org/ig/HL7/dicom-sr/architecture.html).\n\nDICOM Segmentation images created by `pinr` are vieweable within [3D Slicer](https://www.slicer.org/) with the [QuantitativeReporting Extension](https://github.com/QIICR/QuantitativeReporting) installed:\n\n![3D Slicer: DICOM Seg](assets/slicer_dcm_seg.png)\n\n## Installation\n`pinr` has no external dependencies apart from Python >= 3.8.\nRun the following command for installation:\n```\npip install pinr\n```\n\n## Usage\n`pinr` provides both a Python and Command Line Interface (CLI)\n\n### CLI\nAn example command to produce all output is shown here:\n```\npinr \\\n  -i /path/to/file.dcm \\\n  -s /path/to/mri/aseg.mgz \\\n  -m /path/to/aseg.stats \\\n  --dcm-seg /path/to/aseg.seg.dcm \\\n  --dcm-sr /path/to/aseg.sr.dcm \\\n  --fhir /path/to/aseg.fhir.json \\\n```\n\nRun `pinr --help` for more options and information!\n\n# Python Library\n`pinr` exposes a class called `FreeSurferSeg`, which stores volumetric data and measurements.\n\n\nTo initiate:\n```python\nt1w_dicom_file = "/path/to/file.dcm"\naseg_file = "/path/to/mri/aseg.mgz"\naseg_stats_file = "/path/to/aseg.stats"\n# Choose where to save output files\ndicom_seg_output_file = "/path/to/aseg.seg.dcm"\ndicom_sr_output_file = "/path/to/aseg.sr.dcm"\nfhir_output_file = "/path/to/aseg.fhir.json"\n\naseg = FreeSurferSeg(\n    t1w_dicom_file=t1w_dicom_file,\n    aseg_file=aseg_file,\n    aseg_stats_file=aseg_stats_file,\n    dicom_seg_output_file=dicom_seg_output_file,\n    dicom_sr_output_file=dicom_sr_output_file,\n    fhir_output_file=fhir_output_file,\n)\n```\nData is stored as properties of the object, and is written to the given file name if one is provided.\n\n```python\nseg = aseg.seg\nsr = aseg.sr\nfhir = aseg.fhir\n```\n\n## Testing\nExample data is provided.\nAfter installation, clone the repo and cd into it.\nThe following command will produce outputs using the provided input files.\nThese can be compared against the existing output files\n```\npinr \\\n  -i ./tests/data/input/dicom/MR.1.3.12.2.1107.5.2.0.45074.2016081016110642184700287 \\\n  -s ./tests/data/input/aseg.mgz \\\n  -m ./tests/data/input/aseg.stats \\\n  --dcm-seg ./tests/data/output/aseg_new.seg.dcm \\\n  --dcm-sr ./tests/data/output/aseg_new.sr.dcm \\\n  --fhir ./tests/data/output/aseg_new.fhir.json\n```\n\n## Roadmap\n- Improve testing and add CI (in progress)\n- Incorporate feedback regarding architecture decisions of DICOM and FHIR outputs\n- Formal validation of outputs\n\n----\nWork here was supported by the National Institute Of Biomedical Imaging And Bioengineering of the National Institutes of Health under Award Number R43EB030910.\n',
    'author': 'CorticoMetrics',
    'author_email': 'ltirrell@corticometrics.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/pinr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
