import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "pwrdrvr.microapps.cdk",
    "version": "0.3.5.a4",
    "description": "MicroApps framework, by PwrDrvr LLC, delivered as an AWS CDK construct that provides the DynamoDB, Router service, Deploy service, API Gateway, and CloudFront distribution.",
    "license": "MIT",
    "url": "https://github.com/pwrdrvr/microapps-core",
    "long_description_content_type": "text/markdown",
    "author": "PwrDrvr LLC<harold@pwrdrvr.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pwrdrvr/microapps-core"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "pwrdrvr.microapps.cdk",
        "pwrdrvr.microapps.cdk._jsii"
    ],
    "package_data": {
        "pwrdrvr.microapps.cdk._jsii": [
            "microapps-cdk@0.3.5-alpha.4.jsii.tgz"
        ],
        "pwrdrvr.microapps.cdk": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.24.1, <3.0.0",
        "aws-cdk.aws-apigatewayv2-alpha>=2.24.1.a0, <3.0.0",
        "aws-cdk.aws-apigatewayv2-authorizers-alpha>=2.24.1.a0, <3.0.0",
        "aws-cdk.aws-apigatewayv2-integrations-alpha>=2.24.1.a0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.59.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
