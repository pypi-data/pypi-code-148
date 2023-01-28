# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpbc_vyfa_sf']

package_data = \
{'': ['*']}

install_requires = \
['PyVISA>=1.12.0,<2.0.0']

setup_kwargs = {
    'name': 'mpbc-vyfa-sf',
    'version': '0.2.0',
    'description': 'Python interface for a MPB VYFA amplifier',
    'long_description': '# MPBC-VYFA-SF\n Python interface for a MPB Communications VYFA-SF Series amplifier\n\n# Methods and attributes of the `MPBAmplifier` class\n\n* `enable_laser()`  \n  start laser emission\n* `disable_laser()`  \n  disable laser emission\n* `get_faults()`  \n  get all faults of the amplifier\n* `get_alarms()`  \n  get all alarms of the amplifier\n* `enter_test_environment()`  \n  enter the test environment of the amplifier, required to change the SHG temperature setpoint\n* `save_all()`  \n  save settings to non-volatile memory\n* `model`  \n  amplifier model\n* `serial`  \n  serial number\n* `enabled`  \n  boolean for laser emision status\n* `state`\n* `laser_state`  \n  Current state of the laser; e.g. `BOOSTER_ON`, `OFF` etc. see `enums.py` for more.\n* `mode`\n* `seed_current`  \n  mA\n* `preamp_current`  \n  mA\n* `booster_current`  \n  mA\n* `booster_current_setpoint`  \n  get and set the booster current setpoint\n* `shg_temperature`  \n  C\n* `shg_temperature setpoint`  \n  get and set the shg temperature setpoint in C\n* `seed_power`  \n  mW\n* `output_power`  \n  mW\n* `output_power_setpoint`  \n  if `power_stabilization` is enabled (set to `True`) this gets and sets the output power setpoint in mW\n* `power_stabilization`  \n  enable or disable (`True` or `False`) the output power stabilization. Only settable when emission is disabled.\n\n# Example\n```Python\nfrom mpbc_vyfa_sf import MPBAmplifier\n\namp = MPBAmplifier(com_port = "COM4")\n\n# get the current laser state\namp.laser_state\n\n# get the seed power\namp.seed_power\n\n# enable the laser\namp.enable_laser()\n\n# get the output power\namp.output_power\n\n# disable the laser\namp.disable_laser()\n```\n',
    'author': 'ograsdijk',
    'author_email': 'o.grasdijk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ograsdijk/MPBC-VYFA-SF',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
