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

from oslo_config import cfg


_deprecated_group = 'drivers:storage:sqlalchemy'

uri = cfg.StrOpt(
    'uri', default='sqlite:///:memory:',
    deprecated_opts=[cfg.DeprecatedOpt(
        'uri',
        group=_deprecated_group), ],
    help='An sqlalchemy URL')


GROUP_NAME = 'drivers:management_store:sqlalchemy'
ALL_OPTS = [
    uri
]


def register_opts(conf):
    conf.register_opts(ALL_OPTS, group=GROUP_NAME)


def list_opts():
    return {GROUP_NAME: ALL_OPTS}
