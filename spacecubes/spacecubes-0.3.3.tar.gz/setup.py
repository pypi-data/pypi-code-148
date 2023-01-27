# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacecubes', 'spacecubes.io_devices']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24,<2.0', 'pyquaternion>=0.9.9,<0.10.0']

extras_require = \
{'all': ['opencv-python>=4.7,<5.0'], 'opencv': ['opencv-python>=4.7,<5.0']}

setup_kwargs = {
    'name': 'spacecubes',
    'version': '0.3.3',
    'description': 'Simple rendering of three-dimensional NumPy arrays',
    'long_description': "\n# spacecubes\n*Now listen you Royal Highness, take only what you need to survive!*\n\n\n## Overview\n`spacecubes` is a simple voxel renderer for three-dimensional NumPy arrays. It is made to be easy to use and allowing fast visualization. It is not made to produce good looking images or be feature rich.\n\n## Demo\n![Alt Text](https://media.giphy.com/media/1XADnkAnPnnw2YyCAg/giphy.gif)\n\nBelow is how the Windows 95 screensaver-esque demo was created using spacecubes ([examples/windows_screensaver](examples/windows_screensaver.py)).\n```python\nimport numpy as np\nfrom spacecubes import Camera\nfrom spacecubes.io_devices import OpenCV\n\nworld = np.zeros((50, 50, 100))\ncolor_mask = np.random.randint(0, 1000, size=world.shape)\nrandom_mask = np.random.random(size=world.shape)\nworld[random_mask < 0.001] = color_mask[random_mask < 0.001]\ncolors = {i: np.random.random(3) * 255 for i in range(1, 1000)}\ndevice = OpenCV(colors, resolution=(1080, 1920))\ncamera = Camera(x=25, y=25, z=0)\ncamera.look_at(x=25, y=25, z=100)\nwhile True:\n    if camera.position[-1] > 1:\n        camera.move_xyz(z=-1)\n        world = np.roll(world, -1, axis=-1)\n    camera.move(forward=0.1)\n    device.render(world, camera)\n```\n\n## Examples\nRendering a single voxel (cube) in OpenCV and flying the camera around it can be done by running:\n```python\nimport numpy as np\nfrom spacecubes import Camera\nfrom spacecubes.io_devices import OpenCV\n\nworld = np.ones((1, 1, 1))\ncamera = Camera(x=-1, y=-1, z=-1)\ncolors = {1: (0, 255, 0)}\ndevice = OpenCV(colors, resolution=(1080, 1920))\nwhile True:\n    camera.move(up=0.01, right=0.01)\n    camera.look_at(x=0, y=0, z=0)\n    device.render(world, camera)\n```\n\nOther examples with more a fleshed out description can be found in the [examples](examples) directory.\n\n## Features\nAny NumPy array with 3 dimensions can be rendered. All non-zero values in the array are considered voxels, while elements with value 0 will be treated as empty space.\n\n### IO Devices\nAn IO Device in spacecubes is what (optionally) [handles user input](examples/interactive_camera.py) and definitely handles image frame output. The output can be done e.g., through visualization or raw dump. The IO Device needs to know what colors to map each value in the numpy array with, which is what the `colors` argument does. The available io_devices are specified below along with how they are used:\n```python\nfrom spacecubes.io_devices import OpenCV, Raw, Terminal\nfrom spacecubes import Camera\nimport numpy as np\nworld = np.ones((1,1,1))\ncamera = Camera()\n\n# Output the frame using OpenCV imshow\nopencv_device = OpenCV(colors={i: (0, 255, 0) for i in range(1, 100)}, resolution=(1080, 1920))\nopencv_device.render(world, camera)\n\n# Returns the frame as an numpy array\nraw_device = Raw(colors={i: (0, 255, 0) for i in range(1, 100)}, resolution=(1080, 1920))\nframe = raw_device.render(world, camera)\n\n# Outputs the frame directly in the terminal using ncurses\nterminal_device = Terminal(colors={i: 5 for i in range(1, 100)})\nterminal_device.render(world, camera)\n```\n\nTo render the output on the IO device, `device.render(world, camera)` is used, where world is a 3D NumPy array and Camera is..\n\n### Camera\nCamera is the object that handles the virtual camera which specifies the perspective through which the image is rendered. It supports some functions\nrelated to moving, rotating and looking at world locations:\n```python\nfrom spacecubes import Camera\n\n# Initialize a camera along with some world position\ncamera = Camera(x=1, y=2, z=3)\n\n# Move the camera 1 unit back from the camera's perspective\ncamera.move(up=0, forward=-1, right=0)\n\n# Move the camera -1 unit along the world y-axis\ncamera.move_xyz(x=0, y=-1, z=0)\n\n# Move the camera to a specified world position (0, 5, 0)\ncamera.move_to_xyz(x=0, y=5, z=0)\n\n# The camera can be rotated manually through yaw, pitch and roll given in radians\ncamera.rotate(yaw=-3.14/2, pitch=0, roll=0)\n\n# Make the camera look at a specified world location (3, 5, 2)\ncamera.look_at(x=3, y=5, z=2)\n\n# If camera.look_at is too snappy, the same can be done but interpolated.\n# This is done by supplying an amount, which is a fraction between\n# 0 and 1 that specifies where in the interpolation between the current camera\n# pose and the target camera pose that the camera should look\nfor interp_amount in range(100):\n    camera.look_at_interpolated(x=3, y=5, z=2, amount=interp_amount / 100)\n    device.render(world, camera)\n```\n\n## Installation\nspacecubes is available on PyPI: \n`pip install spacecubes[all]`\n\n`all` refers to optional modules needed for `io_devices`, such as OpenCV. Without the `all` tag, only the `io_devices` that rely\non standard packages, such as ncurses, or no packages in the case of the Raw `io_device`, can be used.\n\nPyPI tags: \n`spacecubes`\n`spacecubes[opencv]`\n`spacecubes[all]`\n\n\n### Dependencies:\n- numpy\n- pyquaternion\n- opencv-python (optional)\n\n",
    'author': 'Johan Modin',
    'author_email': 'johan.modin92@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/johanmodin/spacecubes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
