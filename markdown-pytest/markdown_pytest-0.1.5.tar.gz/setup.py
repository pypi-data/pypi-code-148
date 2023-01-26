# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['markdown_pytest']
entry_points = \
{'pytest11': ['markdown-pytest = markdown_pytest']}

setup_kwargs = {
    'name': 'markdown-pytest',
    'version': '0.1.5',
    'description': 'A simple module to test your documentation examples with pytest',
    'long_description': 'markdown-pytest\n===============\n\nA simple module to test your documentation examples with pytest.\n\nMarkdown:\n\n```markdown\n    ```python\n    assert True\n    ```\n```\n\nWill be shown as:\n\n```python\nassert True\n```\n\nYou can use the special value `__name__` to check to separate the run example \nand the test code.\n\nMarkdown:\n\n```markdown\n    ```python\n    if __name__ == \'__main__\':\n        exit(0)\n    if __name__ == \'markdown-pytest\':\n        assert True\n    ```\n```\n\nWill be shown as:\n\n```python\nif __name__ == \'__main__\':\n    exit(0)\nif __name__ == \'markdown-pytest\':\n    assert True\n```\n\nCode after the `# noqa` comment will not be executed.\n\n```markdown\n    ```python\n    # noqa\n    from universe import antigravity, WrongPlanet\n\n    try:\n        antigravity()\n    except WrongPlanet:\n        print("You are on the wrong planet.")\n        exit(1)\n    ```\n```\n\nWill be shown as:\n\n```python\n# noqa\nfrom universe import antigravity, WrongPlanet\n\ntry:\n    antigravity()\nexcept WrongPlanet:\n    print("You are on the wrong planet.")\n    exit(1)\n```\n\nThis README.md file might be tested like this:\n\n```bash\n$ poetry run pytest -sxv README.md                                                                                                                                    17:20:29 \ue0b2\ue0a0master\n=============== test session starts ===============\nplugins: md-0.1.0\ncollected 3 items\n\nREADME.md::line[16-17] PASSED\nREADME.md::line[36-40] PASSED\nREADME.md::line[60-68] PASSED\n```\n',
    'author': 'Dmitry Orlov',
    'author_email': 'me@mosquito.su',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mosquito/markdown-pytest',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
