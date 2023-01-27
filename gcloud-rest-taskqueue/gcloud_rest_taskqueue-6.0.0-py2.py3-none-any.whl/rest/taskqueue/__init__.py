"""
This library implements various methods for working with the Google Taskqueue
APIs.

## Installation

```console
$ pip install --upgrade gcloud-rest-taskqueue
```

## Usage

We're still working on documentation -- for now, you can use the
[smoke tests][smoke-tests] as an example.

## Emulators

For testing purposes, you may want to use `gcloud-rest-taskqueue` along with a
local emulator. Setting the `$CLOUDTASKS_EMULATOR_HOST` environment variable to
the address of your emulator should be enough to do the trick.

[smoke-tests]:
https://github.com/talkiq/gcloud-rest/tree/master/taskqueue/tests/integration
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from pkg_resources import get_distribution
__version__ = get_distribution('gcloud-rest-taskqueue').version

from gcloud.rest.taskqueue.queue import PushQueue
from gcloud.rest.taskqueue.queue import SCOPES


__all__ = [
    'PushQueue',
    'SCOPES',
    '__version__',
]
