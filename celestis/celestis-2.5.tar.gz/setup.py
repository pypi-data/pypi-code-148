from setuptools import setup

setup(
    name="celestis",
    version="2.5",
    description="A simple backend framework built using python",
    author="Aryaan Hegde",
    author_email="aryhegde@gmail.com",
    packages=["celestis.controller", "celestis.model", "celestis.view"],
    package_dir={"celestis.controller": "controller", "celestis.view": "view", "celestis.model": "model"},
    py_modules=["command", "create_files", "exceptions", "templates", "request", "database", "crud", "auth"],
    include_package_data=True,
    install_requires=['requests', 'click', "PyJWT"],
    entry_points={
        "console_scripts": [
            "celestis=command:celestis"
        ]
    }
)
