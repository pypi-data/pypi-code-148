import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudsnorkel.cdk-turbo-layers",
    "version": "0.0.1",
    "description": "Speed-up Lambda function deployment with dependency layers built in AWS",
    "license": "Apache-2.0",
    "url": "https://github.com/CloudSnorkel/cdk-turbo-layers.git",
    "long_description_content_type": "text/markdown",
    "author": "Amir Szekely<amir@cloudsnorkel.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/CloudSnorkel/cdk-turbo-layers.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloudsnorkel.cdk_turbo-layers",
        "cloudsnorkel.cdk_turbo-layers._jsii"
    ],
    "package_data": {
        "cloudsnorkel.cdk_turbo-layers._jsii": [
            "cdk-turbo-layers@0.0.1.jsii.tgz"
        ],
        "cloudsnorkel.cdk_turbo-layers": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.54.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.74.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
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
