# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_stack_inspector']

package_data = \
{'': ['*']}

install_requires = \
['Django>3.2']

setup_kwargs = {
    'name': 'django-stack-inspector',
    'version': '1.0.0',
    'description': 'Inspect the current Python call stack to determine if the Django app is just starting up or already running.',
    'long_description': '# Django Stack Inspector\n\nThe Django Stack Inspector package is useful to inspect the current call stack of a Django application and determine if it is starting up or already running.\n\nIt is likely that the 99% of applications do not have a need for this, but in specific niche scenarios it can be very useful. For example, when implementing a model manager that limits queries to items owned by a specific tenant by overriding the `get_queryset()` method filtered using data stored in a `ContextVar` or thread-local set by a request middleware. It may be desired that if queries are executed without the `ContextVar` being appropriately set (e.g. queries via asynchronous background workers or via admin commands) then the `get_queryset()` method fails-closed by throwing an exception warning the user that the required context is not set. However, this fail-closed behaviour breaks the management commands for migrations by throwing the exception. \n\n## Installation\n\n`pip install django_stack_inspector`\n\n## Usage\n\nAn example of how to use when creating a custom model manager to restrict queries to specific tenants.\n\n\n```python\nfrom django_stack_inspector import StackInspector\n\ndef get_queryset(self):\n    """\n    Override the default queryset behaviour to enforce a filter dependent on the tenant context\n    The queryset will fail-closed if a query is ran without a context, either by returning no results in the\n    queryset or by raising an exception.\n    """\n    try:\n        ctx = get_request_context()\n    except RequestContextNotSet as exc:\n        # Context not set so fail-closed\n        if StackInspector().is_app_startup():\n            # Silence exception and return empty queryset as app starting (i.e. is a management command)\n            return super().get_queryset().none()\n        # Raise exception to alert developer\n        raise exc\n\n    # Perform filtering\n    return super().get_queryset().filter(tenant=ctx.tenant)\n```\n\n',
    'author': 'Adam McKay',
    'author_email': 'adam@beepboop.digital',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Beep-Boop-Digital/django-stack-inspector',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
