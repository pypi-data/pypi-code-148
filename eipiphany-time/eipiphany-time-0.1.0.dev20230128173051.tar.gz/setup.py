import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

with open('requirements-install.txt') as f:
  for req in f.read().splitlines():
    requirements.append(req)

setuptools.setup(
  name="eipiphany-time",
  version="0.1.0.dev20230128173051",
  description="Simple Multiprocessing EIP Framework For Python: Time Components",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ci-cmg/eipiphany",
  package_dir={'': 'src'},
  packages=setuptools.find_packages('src'),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.9',
  install_requires=[req for req in requirements if req[:2] != "# "]
)