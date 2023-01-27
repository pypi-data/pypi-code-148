from __future__ import annotations

import functools
import importlib
import os
from typing import final

import boto3

from episteme._manifests import get_manifests
from episteme._utils import dget


@final
class _Credentials():
    def __init__(self) -> None:
        self.manifests = get_manifests().fetch('credentials')
        self.instances = {}
        for name, manifest in self.manifests.items():
            self.instances[name] = _Credential(manifest)

    def fetch(self, name, default=None):
        return self.instances[name].get_value()


class _Credential:
    def __init__(self, manifest) -> None:
        kind = manifest.get('kind', None)
        if kind not in kinds:
            raise ValueError('invalid kind')

        kindClass = getattr(importlib.import_module(__name__), kind)
        self.instance = kindClass(manifest)

    def get_value(self):
        return self.instance.get_value()


class EnvironmentVariable:
    def __init__(self, manifest):
        self.manifest = manifest

    def get_value(self):
        k = self.manifest['key']
        d = self.manifest.get('default', None)
        return os.environ.get(k, d)


class AWSParameterStore:
    def __init__(self, manifest):
        self.manifest = manifest
        options = {}
        region_name = manifest.get('region', None)
        if region_name is not None:
            options['region_name'] = region_name

        profile = manifest.get('profile', None)
        if profile:
            session = boto3.session.Session(profile_name=profile)
            self.ssm = session.client('ssm', **options)
        else:
            self.ssm = boto3.client('ssm', **options)

    def get_value(self):
        k = self.manifest['key']
        response = self.ssm.get_parameter(Name=k, WithDecryption=True)
        return dget(response, 'Parameter.Value')


kinds = {
    'AWSParameterStore': AWSParameterStore,
    'EnvironmentVariable': EnvironmentVariable,
}


@functools.lru_cache(maxsize=1)
def get_credentials():
    return _Credentials()


def creds(name, default=None):
    return get_credentials().fetch(name, default=default)
