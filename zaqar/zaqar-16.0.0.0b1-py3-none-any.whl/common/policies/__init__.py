# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import itertools

from zaqar.common.policies import base
from zaqar.common.policies import claims
from zaqar.common.policies import flavors
from zaqar.common.policies import health
from zaqar.common.policies import messages
from zaqar.common.policies import pools
from zaqar.common.policies import queues
from zaqar.common.policies import subscription
from zaqar.common.policies import topics


def list_rules():
    return itertools.chain(
        base.list_rules(),
        claims.list_rules(),
        flavors.list_rules(),
        health.list_rules(),
        messages.list_rules(),
        pools.list_rules(),
        queues.list_rules(),
        subscription.list_rules(),
        topics.list_rules(),
    )
