# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ml4gw', 'ml4gw.dataloading', 'ml4gw.transforms', 'ml4gw.utils']

package_data = \
{'': ['*']}

install_requires = \
['bilby>=1.1,<2.0',
 'gwpy>=2.1,<3.0',
 'torch>=1.10,<2.0',
 'torchtyping>=0.1,<0.2']

setup_kwargs = {
    'name': 'ml4gw',
    'version': '0.1.1',
    'description': 'Tools for training torch models on gravitational wave data',
    'long_description': '# ML4GW\n\nTorch utilities for training neural networks in gravitational wave physics applications.\n\n## Installation\n### Pip installation\nYou can install `ml4gw` with pip:\n\n```console\npip install ml4gw\n```\n\nTo build with a specific version of PyTorch/CUDA, please see the PyTorch installation instructions [here](https://pytorch.org/get-started/previous-versions/) to see how to specify the desired torch version and `--extra-index-url` flag. For example, to install with torch 1.12 and CUDA 11.6 support, you would run\n\n```console\npip install ml4gw torch==1.12.0 --extra-index-url=https://download.pytorch.org/whl/cu116\n```\n\n### Poetry installation\n`ml4gw` is also fully compatible with use in Poetry, with your `pyproject.toml` set up like\n\n```toml\n[tool.poetry.dependencies]\npython = "^3.8"  # python versions 3.8-3.10 are supported\nml4gw = "^0.1.0"\n```\n\nTo build against a specific PyTorch/CUDA combination, consult the PyTorch installation documentation above and specify the `extra-index-url` via the `tool.poetry.source` table in your `pyproject.toml`. For example, to build against CUDA 11.6, you would do something like:\n\n```toml\n[tool.poetry.dependencies]\npython = "^3.8"\nml4gw = "^0.1.0"\ntorch = {version = "^1.12", source = "torch"}\n\n[[tool.poetry.source]]\nname = "torch"\nurl = "https://download.pytorch.org/whl/cu116"\nsecondary = true\ndefault = false\n```\n\n## Use cases\nThis library provided utilities for both data iteration and transformation via dataloaders defined in `ml4gw/dataloading` and transform layers exposed in `ml4gw/transforms`. Lower level functions and utilies are defined at the top level of the library and in the `utils` library.\n\nFor example, to train a simple autoencoder using a cost function in frequency space, you might do something like:\n\n```python\nimport numpy as np\nimport torch\nfrom ml4gw.dataloading import InMemoryDataset\nfrom ml4gw.transforms import SpectralDensity\n\nSAMPLE_RATE = 2048\nNUM_IFOS = 2\nDATA_LENGTH = 128\nKERNEL_LENGTH = 4\nDEVICE = "cuda"  # or "cpu", wherever you want to run\n\nBATCH_SIZE = 32\nLEARNING_RATE = 1e-3\nNUM_EPOCHS = 10\n\ndummy_data = np.random.randn(NUM_IFOS, DATA_LENGTH * SAMPLE_RATE)\n\n# this will create a dataloader that iterates through your\n# timeseries data sampling 4s long windows of data randomly\n# and non-coincidentally: i.e. the background from each IFO\n# will be sampled independently\ndataset = InMemoryDataset(\n    dummy_data,\n    kernel_size=KERNEL_LENGTH * SAMPLE_RATE,\n    batch_size=BATCH_SIZE,\n    batches_per_epoch=50,\n    coincident=False,\n    shuffle=True,\n    device=DEVICE  # this will move your dataset to GPU up-front if "cuda"\n)\n\n\nnn = torch.nn.Sequential(\n    torch.nn.Conv1d(\n        in_channels=2,\n        out_channels=8,\n        kernel_size=7\n    ),\n    torch.nn.ConvTranspose1d(\n        in_channels=8,\n        out_channels=2,\n        kernel_size=7\n    )\n).to(DEVICE)\n\noptimizer = torch.optim.Adam(nn.parameters(), lr=LEARNING_RATE)\n\nspectral_density = SpectralDensity(SAMPLE_RATE, fftlength=2).to(DEVICE)\n\ndef loss_function(X, y):\n    """\n    MSE in frequency domain. Obviously this doesn\'t\n    give you much on its own, but you can imagine doing\n    something like masking to just the bins you care about.\n    """\n    X = spectral_density(X)\n    y = spectral_density(y)\n    return ((X - y)**2).mean()\n\n\nfor i in range(NUM_EPOCHS):\n    epoch_loss = 0\n    for X in dataset:\n        optimizer.zero_grad(set_to_none=True)\n        assert X.shape == (32, NUM_IFOS, KERNEL_LENGTH * SAMPLE_RATE)\n        y = nn(X)\n\n        loss = loss_function(X, y)\n        loss.backward()\n        optimizer.step()\n\n        epoch_loss += loss.item()\n    epoch_loss /= len(dataset)\n    print(f"Epoch {i + 1}/{NUM_EPOCHS} Loss: {epoch_loss:0.3e}")\n```\n\n## Development\nAs this library is still very much a work in progress, we anticipate that novel use cases will encounter errors stemming from a lack of robustness.\nWe encourage users who encounter these difficulties to file issues on GitHub, and we\'ll be happy to offer support to extend our coverage to new or improved functionality.\nWe also strongly encourage ML users in the GW physics space to try their hand at working on these issues and joining on as collaborators!\nFor more information about how to get involved, feel free to reach out to [ml4gw@ligo.mit.edu](mailto:ml4gw@ligo.mit.edu) .\nBy bringing in new users with new use cases, we hope to develop this library into a truly general-purpose tool which makes DL more accessible for gravitational wave physicists everywhere.\n',
    'author': 'Alec Gunny',
    'author_email': 'alec.gunny@ligo.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
