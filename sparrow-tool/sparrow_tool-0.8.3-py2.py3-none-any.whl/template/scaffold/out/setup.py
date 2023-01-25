import setuptools

setuptools.setup(
    pbr=True,
    package_data={
        "my_project": [
            '*.yaml', '*.yml', '*.json',
        ],
    },
)
