# Copyright (c) 2013 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools

from zaqarclient import errors


def version(min_version, max_version=None):
    min_version = float(min_version)
    max_version = max_version and float(max_version)

    error_msg = ('Method %(name)s is supported from version %(min)s '
                 'to %(max)s')

    def method(meth):
        @functools.wraps(meth)
        def wrapper(self, *args, **kwargs):
            if (self.api_version < min_version or
                    (max_version and self.api_version > max_version)):
                msg = error_msg % dict(name=str(meth),
                                       min=min_version,
                                       max=max_version or 'latest')
                raise errors.UnsupportedVersion(msg)
            return meth(self, *args, **kwargs)
        return wrapper
    return method


def lazy_property(write=False, delete=True):
    """Creates a lazy property.

    :param write: Whether this property is "writable"
    :param delete: Whether this property can be deleted.
    """

    def wrapper(fn):
        attr_name = '_lazy_' + fn.__name__

        def getter(self):
            if not hasattr(self, attr_name):
                setattr(self, attr_name, fn(self))
            return getattr(self, attr_name)

        def setter(self, value):
            setattr(self, attr_name, value)

        def deleter(self):
            delattr(self, attr_name)

        return property(fget=getter,
                        fset=write and setter,
                        fdel=delete and deleter,
                        doc=fn.__doc__)
    return wrapper
