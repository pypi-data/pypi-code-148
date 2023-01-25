# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qtgql',
 'qtgql.codegen',
 'qtgql.codegen.py',
 'qtgql.codegen.py.templates',
 'qtgql.ext',
 'qtgql.gqltransport',
 'qtgql.itemsystem']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.4.1', 'attrs>=22.2.0,<23.0.0', 'nothing>=0.0.3,<0.0.4']

entry_points = \
{'console_scripts': ['qtgql = qtgql.codegen.cli:entrypoint']}

setup_kwargs = {
    'name': 'qtgql',
    'version': '0.101.0',
    'description': 'Qt framework for building graphql driven QML applications',
    'long_description': '# qtgql\n## Qt framework for building graphql driven QML applications\n![PyPI - Downloads](https://img.shields.io/pypi/dm/qtgql)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/qtgql?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/qtgql?style=for-the-badge)\n![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/nrbnlulu/qtgql/tests.yml?label=tests&style=for-the-badge)\n\n### Disclaimer\nThis project is currently under development and **it is not** production ready,\nYou can play-around and tell us what is wrong / missing / awesome :smile:.\n### Intro\nQt-QML IMO is a big game changer\n- you get native performance\n- UI code is very clear and declarative\n- Easy to customize\n- Easy to learn\n\nOne of the big disadvantages in Qt-QML is that Qt-C++ API is very repititive and hard to maintain\nfor data-driven applications.\n\nalthough it is tempting to just use `relay` or other `JS` graphql lib\nthere is a point where you would suffer from performance issues (:roll_eyes:  react-native).\n\n### Solutions I had so far\nTo overcome Qt\'s "great" API I wrote [qtgql](https://github.com/nrbnlulu/qtgql) Initially it was just meant for API hacks\ni.e\n```py\n# instead of\n@Slot(argumeants=(str, int, str), result=str)\ndef some_slot(self, a, b, c):\n    return "foo"\n\n# gets return type from annotations\nfrom qtgql import slot\n\n@slot\ndef some_slot(self, a: str, b: int, c: list[str]) -> str:\n    return "foo"\n```\n\nAlso I have made generic models so that you won\'t have to define `roles` `data` `update` manage signals emission and\nso much boilerplate code yourself.\n\nyou would just declare your model like this\n```py\nfrom qtgql.itemsystem.schema import Schema\nfrom qtgql.itemsystem import role, GenericModel, get_base_type\nBaseType = get_base_type()\nclass Worm(BaseType):\n    name: str = role()\n    family: str = role()\n    size: int = role()\n\n\nclass Apple(BaseType):\n    size: int = role()\n    owner: str = role()\n    color: str = role()\n    worms: GenericModel[Worm] = role(default=None)\n\n\n\napple_model: GenericModel[Apple] = Apple.Model(schema=schema)\napple_model.initialize_data(data)  # dict with the correct fields\n```\n\n\n### GraphQL support\nAs I have proggresed with the codebase I realized that I can do better and possibly mimic some\nfeatures of graphql relay at the cost of making this project more opinionated.\nSo I decided to rename it to `qtgql` (previouslly cuter :cat: ).\nSome of the current features:\n - Qt-native graphql-transport-ws network manager (supports subscriptions).\n - generic models that get created from dictionaries (with update, pop, insert implemeanted by default)\n - property classes that are accessible from QML, with dataclasses  syntax (using attrs)\n\n### Future vision\n- Code generation from schema inspection\nIdeally every graphql type would be a `QObject` with `Property` for each field.\n- possibly generate C++ bindings from schema inspection\n- Query only what defined by the user (similar to how relay does this)\n- Auto mutations\n- Subscriptions\n\n\n\n### Example Usage (no codegen):\nThe following example shows how qtgql can be used to query a graphql service.\n*models.py*\n\n```python\nfrom qtgql.itemsystem import role, define_roles\n\n\n@define_roles\nclass Worm:\n    name: str = role()\n    family: str = role()\n    size: int = role()\n\n\n@define_roles\nclass Apple:\n    size: int = role()\n    owner: str = role()\n    color: str = role()\n    # nested models are also supported!\n    worms: Worm = role(default=None)\n```\nqtgql will create for you `QAbstractListModel` to be used in QML you only need to\ndefine your models with `define_roles`.\nqtgql initializes the data with a dict, in this case coming from graphql service.\n\n*main.py*\n\n```python\nimport glob\nimport os\nimport sys\nfrom pathlib import Path\n\nfrom qtpy.QtQml import QQmlApplicationEngine\nfrom qtpy.QtCore import QObject, Signal\nfrom qtpy import QtCore, QtGui, QtQml, QtQuick\n\nfrom qtgql import slot\nfrom qtgql.gqltransport.client import HandlerProto, GqlClientMessage, GqlWsTransportClient\nfrom qtgql.itemsystem import GenericModel\nfrom tests.test_sample_ui.models import Apple\n\n\nclass EntryPoint(QObject):\n    class AppleHandler(HandlerProto):\n        message = GqlClientMessage.from_query(\n            """\n            query MyQuery {\n              apples {\n                color\n                owner\n                size\n                worms {\n                  family\n                  name\n                  size\n                }\n              }\n            }\n            """\n        )\n\n        def __init__(self, app: \'EntryPoint\'):\n            self.app = app\n\n        def on_data(self, message: dict) -> None:\n            self.app.apple_model.initialize_data(message[\'apples\'])\n\n        def on_error(self, message: dict) -> None:\n            print(message)\n\n        def on_completed(self, message: dict) -> None:\n            print(message)\n\n    def __init__(self, parent=None):\n        super().__init__(parent)\n        main_qml = Path(__file__).parent / \'qml\' / \'main.qml\'\n        QtGui.QFontDatabase.addApplicationFont(str(main_qml.parent / \'materialdesignicons-webfont.ttf\'))\n        self.qml_engine = QQmlApplicationEngine()\n        self.gql_client = GqlWsTransportClient(url=\'ws://localhost:8080/graphql\')\n        self.apple_query_handler = self.AppleHandler(self)\n        self.gql_client.query(self.apple_query_handler)\n        self.apple_model: GenericModel[Apple] = Apple.Model()\n        QtQml.qmlRegisterSingletonInstance(EntryPoint, "com.props", 1, 0, "EntryPoint", self)  # type: ignore\n        # for some reason the app won\'t initialize without this event processing here.\n        QtCore.QEventLoop().processEvents(QtCore.QEventLoop.ProcessEventsFlag.AllEvents, 1000)\n        self.qml_engine.load(str(main_qml.resolve()))\n\n    @QtCore.Property(QtCore.QObject, constant=True)\n    def appleModel(self) -> GenericModel[Apple]:\n        return self.apple_model\n\n\ndef main():\n    app = QtGui.QGuiApplication(sys.argv)\n    ep = EntryPoint()  # noqa: F841, this collected by the gc otherwise.\n    ret = app.exec()\n    sys.exit(ret)\n\n\nif __name__ == "__main__":\n    main()\n```\n\n![Example](assets/qtgql.gif)\n',
    'author': 'Nir',
    'author_email': '88795475+nrbnlulu@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
