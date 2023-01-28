# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['visionai',
 'visionai.cli',
 'visionai.config',
 'visionai.models',
 'visionai.tests',
 'visionai.util']

package_data = \
{'': ['*'], 'visionai': ['models-repo/*']}

install_requires = \
['coloredlogs>=15.0.1,<16.0.0',
 'opencv-python>=4.6.0,<5.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pytest>=7.2.1,<8.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'requests>=2.28.2,<3.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'torch>=1.11.0,<2.0.0',
 'torchvision>=0.12.0,<0.13.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['visionai = visionai.main:app']}

setup_kwargs = {
    'name': 'visionai',
    'version': '0.1.11',
    'description': 'Vision AI toolkit',
    'long_description': '# VisionAI\n\nDocumentation for VisionAI toolkit.\n\n## Overview\n\n**VisionAI** provides a set of command line utilities for you to manage different Vision AI scenarios that have been pre-developed and pre-tested. **VisionAI** focuses on workplace health and safety models - and majority of the models you see here have been developed with that in mind.\n\nThese are *production-ready* model trained from open-source and academic datasets. We are continuously working on new scenarios - and our current scenario repo consists of over 60 scenarios that are listed [here](scenarios/index.md). They are developed with the intent of being easy-to-use for business. The framework also supports a whole bunch of [custom scenarios](TODO/custom-scenarios.md).\n\n## Install **VisionAI**\n\nInstall **VisionAI** application through `PyPI`. There are other options available for install - including a Docker container option. These are detailed in [installation](TODO/install.md) section.\n\n```console\n$ pip install visionai\n---> 100%\nSuccessfully installed visionai\n\n✨ You are all set to use visionai toolkit ✨\n```\n\n## Deploy to **Azure**\n\nDeploy a fully configured and tested solution directly from Azure Marketplace. **VisionAI** runs computer vision models, most of which run orders of magnitude faster if executed on a GPU machine. Our Azure Marketplace offer **VisionAI Community Edition** is available through Azure Marketplace [here](https://azure.microsoft.com) (TODO). The community edition deploys a fully configured Virtual Machine with the recommended hardware and software options. Get more details [here](azure/installation.md).\n\n![Deploy to Azure](https://aka.ms/deploytoazurebutton)\n\n- TODO: Point to ARM template that needs to be deployed (using these [instructions](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/deploy-to-azure-button) and here is an example [JSON file](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.storage/storage-account-create/azuredeploy.json)).\n\n## List available **Scenarios**\n\n**VisionAI** is organized in terms of scenarios. Consider each scenario as being a business use-case, that is solved by a combination of Machine Learning models and an inference algorithm. For example *Warn me when max occupancy of this area exceeds 80 people* is a business scenario, where as the *People detection* is an ML model.\n\n**VisionAI** supports 60 scenarios currently and more are being added continuously. Our current focus is on Workplace Safety scenarios. Please [contact us](contact.md) if a scenario you need is not present in our repo and we will look into it.\n\n```console\n$ visionai scenarios list\n\n------------------------------------------------\nPrivacy Suite\nblur-faces\nblur-text\n\nFire safety\nearly-smoke-and-fire-detection\nsmoking-and-vaping-detection\n\nPersonnel safety\nppe-detection\npfas-system-detection\nrailings-detection\n\nSuspicious activity\nshipping-activity-detection\nagressive-behaivior\n\n\nCompliance Policies\nmax-occupancy\n\nEquipment\nrust-and-corrosion-detection\n\nIR Camera\ntemperature-monitoring\n------------------------------------------------\n\n✨ More scenarios are added regularly ✨\n```\n\n\n## Get details for a **Scenario**\n\nYou can get details about a scenario using `visionai scenario details` command. Specify the scenario you want additional details for. The details of a scenario include the dataset size, model accuracy metrics,\n\n```console\n$ visionai scenario --name early-smoke-and-fire-detection details\n\n------------------------------------------------\nCategory: Fire safety\nScenario: early-smoke-and-fire-detection\nThis scenario has been trained on open-source datasets consisting of 126,293 images. The datasets images are primarily outdoors (70%), but do contain a good number of indoor images (30%). There is a ~50-50% mix of day vs night images. You can find more details about this scenario at visionify.ai/early-smoke-and-fire-detection.\n\n\nModel: smoke-and-fire-detection-1.0.1.pt\nModel size: 127MB\nModel type: Object Detection\nFramework: PyTorch\n\nModel performance:\nDataset size: 126,293 images\nAccuracy: 94.1%\nRecall: 93%\nF1-Score: 93.5%\n\nEvents:\nsmoke-detected  | Immediate\nfire-detected   | Immediate\n\nEvent examples:\n{\n    "scenario": "smoke-and-fire-detection",\n    "event_name": "smoke-detected",\n    "event_details": {\n        "camera": "camera-01",\n        "date": "2023-01-04 11:05:02",\n        "confidence": 0.92\n    }\n}\n------------------------------------------------\n\n```\n\n## Run a **Scenario**\n\nUse `visionai run` command to run a scenario. In its simplest sense, you can run a single scenario on your web-cam. In a more complex use-case, you can specify a pipeline of scenarios, configure notification logic for each scenario, timings for each scenario etc.\n\n```console\n$ visionai run --scenario early-smoke-and-fire-detection --camera OFFICE-01\n\nStarting early-smoke-and-fire-detection\n...\n\n```\n\n## Next **steps**\n\nCongratulations! You have successfully run the first scenario. Now go through [Tutorials](tutorials/index.md) to learn about how to run multiple scnearios, how to configure each scenario for the events you need, how to set up the dependencies etc.\n\nOr you can also go through our [scenarios](scenarios/index.md) page to explore the different scenarios available and their model details. If you have a need for a scenario to be implemented, do not hesitate to submit a [request](https://github.com/visionify/visionai/issues).\n\n',
    'author': 'Harsh Murari',
    'author_email': 'hmurari@visionify.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
