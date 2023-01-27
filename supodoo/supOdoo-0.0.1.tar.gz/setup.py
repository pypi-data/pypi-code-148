#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

lib_name = "odoo"

setup(
    name="supOdoo",
    version="0.0.1",
    description="simple cli tool for Suplyd devs to run local Odoo setup without hassel",
    url="https://github.com/saurabhjainwal-suplyd/suplyd-odoo-cli-runner",
    author="saurabhjainwal",
    author_email="saurabh@suplyd.app",
    license="MIT",
    scripts=["./sup-odoo/dockerComGen.py"],
    packages=find_packages(),
    package_dir={"%s" % lib_name: "odoo"},
    include_package_data=True,
    install_requires=["Command", "typer"],
    python_requires=">=3.7",
)
