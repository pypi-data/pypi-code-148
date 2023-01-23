import setuptools

long_description:str = open('README.md').read()

setuptools.setup (
    include_package_data=True,
    name='runfalcon-pipeline-integration',
    version='1.0.2',
    description='Runfalcon tools to integrate with pipelines',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url='https://git-codecommit.zone.amazonaws.com/v1/repos/runfalcon-pipeline-integration-py-package',
    author='Raul A. de Villa C.',
    author_email='r@runfalcon.com',
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    install_requires=['requests', 'urllib3'],
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
    license_files=('LICENCE',)
)