# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_protector', 'graphene_protector.django']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core>=3']

extras_require = \
{'optional': ['graphene>=3',
              'graphene-django>=3',
              'strawberry-graphql>=0.92',
              'strawberry-graphql-django']}

setup_kwargs = {
    'name': 'graphene-protector',
    'version': '0.10.0',
    'description': 'Protects graphene, graphql or strawberry against malicious queries',
    'long_description': '# What does this project solve?\n\nIt provides protection against malicious grapqhl requests (resource exhaustion).\nDespite its name it can be used with graphql (pure), graphene, strawberry.\nIt is implemented via a custom ValidationRule,\nsupports error reporting and early bail out strategies as well as limits for single fields\n\n# Installation\n\n```sh\npip install graphene-protector\n```\n\n# Integration\n\n## Django\n\nThis adds to django the following setting:\n\n-   GRAPHENE_PROTECTOR_DEPTH_LIMIT: max depth\n-   GRAPHENE_PROTECTOR_SELECTIONS_LIMIT: max selections\n-   GRAPHENE_PROTECTOR_COMPLEXITY_LIMIT: max (depth \\* selections)\n-   GRAPHENE_PROTECTOR_PATH_INGORE_PATTERN: ignore fields in calculation (but still traverse them)\n\nIntegrate with:\n\ngraphene:\n\n```python 3\n# schema.py\n# replace normal Schema import with:\nfrom graphene_protector.django.graphene import Schema\nschema = Schema(query=Query, mutation=Mutation)\n```\n\nand add in django settings to GRAPHENE\n\n```python 3\n\nGRAPHENE = {\n    ...\n    "SCHEMA": "path.to.schema",\n}\n```\n\nor strawberry:\n\n```python 3\n# schema.py\n# replace normal Schema import with:\nfrom graphene_protector.django.strawberry import Schema\nschema = Schema(query=Query, mutation=Mutation)\n```\n\nmanual way (note: import from django for including defaults from settings)\n\n```python 3\nfrom graphene_protector.django.graphene import Schema\n# or\n# from graphene_protector.django.strawberry import Schema\nschema = Schema(query=Query)\nresult = schema.execute(query_string)\n```\n\nmanual way with custom default Limits\n\n```python 3\nfrom graphene_protector import Limits\nfrom graphene_protector.django.graphene import Schema\n# or\n# from graphene_protector.django.strawberry import Schema\nschema = graphene.Schema(query=Query, limits=Limits(complexity=None))\nresult = schema.execute(\n    query_string\n)\n\n```\n\n## Graphene & Strawberry\n\nlimits keyword with Limits object is supported.\n\n```python 3\nfrom graphene_protector import Limits\nfrom graphene_protector.graphene import Schema\n# or\n# from graphene_protector.strawberry import Schema\nschema = Schema(query=Query, limits=Limits(depth=20, selections=None, complexity=100))\nresult = schema.execute(query_string)\n```\n\n## pure graphql\n\n```python 3\n\nfrom graphene_protector import LimitsValidationRule\nfrom graphql.type.schema import Schema\nschema = Schema(\n    query=Query,\n)\nquery_ast = parse("{ hello }")\nself.assertFalse(validate(schema, query_ast, [LimitsValidationRule]))\n\n```\n\nor with custom defaults\n\n```python 3\n\nfrom graphene_protector import Limits, LimitsValidationRule\nfrom graphql.type.schema import Schema\n\nclass CustomLimitsValidationRule(LimitsValidationRule):\n    default_limits = Limits(depth=20, selections=None, complexity=100)\n\nschema = Schema(\n    query=Query,\n)\nquery_ast = parse("{ hello }")\nself.assertFalse(validate(schema, query_ast, [LimitsValidationRule]))\n\n```\n\nstrawberry extension variant\n\n```python 3\nfrom graphene_protector import Limits\nfrom graphene_protector.strawberry import CustomGrapheneProtector\nfrom strawberry import Schema\nschema = Schema(query=Query, extensions=[CustomGrapheneProtector(Limits(depth=20, selections=None, complexity=100))])\nresult = schema.execute(query_string)\n```\n\nor with custom defaults via Mixin\n\n```python 3\n\nfrom graphene_protector import Limits, SchemaMixin, LimitsValidationRule\nfrom graphql.type.schema import Schema\n\nclass CustomSchema(SchemaMixin, Schema):\n    protector_default_limits = Limits(depth=20, selections=None, complexity=100)\n\nschema = CustomSchema(\n    query=Query,\n)\nquery_ast = parse("{ hello }")\nself.assertFalse(validate(schema, query_ast, [LimitsValidationRule]))\n\n```\n\nstrawberry variant with mixin\n\n```python 3\nfrom graphene_protector import Limits, SchemaMixin, default_path_ignore_pattern\nfrom strawberry import Schema\n\nclass CustomSchema(SchemaMixin, Schema):\n    protector_default_limits = Limits(depth=20, selections=None, complexity=100)\n    protector_path_ignore_pattern = default_path_ignore_pattern\n\nschema = CustomSchema(query=Query)\nresult = schema.execute(query_string)\n```\n\nNote: for the mixin method all variables are prefixed in schema with `protector_`. Internally the `get_protector_` methods are used and mapped on the validation context\n\n## Limits\n\nA Limits object has following attributes:\n\n-   depth: max depth (default: 20, None disables feature)\n-   selections: max selections (default: None, None disables feature)\n-   complexity: max (depth subtree \\* selections subtree) (default: 100, None disables feature)\n\nthey overwrite django settings if specified.\n\n## decorating single fields\n\nSometimes single fields should have different limits:\n\n```python\n    person1 = Limits(depth=10)(graphene.Field(Person))\n```\n\nLimits are inherited for unspecified parameters\n\n## one-time disable limit checks\n\nto disable checks for one operation use check_limits=False (works for:\nexecute, execute_async (if available), subscribe (if available)):\n\n```python 3\nfrom graphene_protector import Limits\nfrom graphene_protector.graphene import Schema\nschema = Schema(query=Query, limits=Limits(depth=20, selections=None, complexity=100))\nresult = schema.execute(query_string, check_limits=False)\n```\n\n# Path ignoring\n\nThis is a feature for ignoring some path parts in calculation but still traversing them.\nIt is useful for e.g. relay which inflates the depth significant and can cause problems with complexity\nCurrently it is set to `edges/node$` which reduces the depth of connections by one\n\nOther examples are:\n\n-   `node$|id$` for ignoring id fields in selection/complexity count and reducing the depth by 1 when seeing a node field\n-   `page_info|pageInfo` for ignoring page info in calculation (Note: you need only one)\n\n# Development\n\nI am open for new ideas.\nIf you want some new or better algorithms integrated just make a PR\n\n# related projects:\n\n-   secure-graphene: lacks django integration, some features and has a not so easy findable name.\n    But I accept: it is the "not invented here"-syndrome\n\n# TODO\n\n-   test path_ignore_pattern\n-   keep an eye on the performance impact of the new path regex checking\n',
    'author': 'alex',
    'author_email': 'devkral@web.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/devkral/graphene-protector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
