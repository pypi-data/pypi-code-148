app_template = """#!/usr/bin/env python3
import aws_cdk as cdk
from viburnum.deployer import AppStack
from viburnum.application import Application

# [Imports]

app = Application("{app_name}")

# [Handlers]

# [Resources]

cdk_app = cdk.App()
AppStack(cdk_app, app)

cdk_app.synth()
"""
