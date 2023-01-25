# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['proper_forms', 'proper_forms.fields', 'proper_forms.ftypes']

package_data = \
{'': ['*']}

install_requires = \
['dnspython>=1.15',
 'email-validator>=1.1',
 'idna>=2.8',
 'markupsafe>=1.1',
 'python-slugify>=3.0']

setup_kwargs = {
    'name': 'proper-forms',
    'version': '0.7',
    'description': 'A proper flexible Python form library',
    'long_description': '![Proper Forms](header.png)\n\nProper Forms is a flexible form library to make far easier to create beautiful, semantically rich, syntactically awesome, readily stylable and wonderfully accessible HTML forms in your Python web application.\n\n**Documentation**: https://proper-forms.scaletti.dev\n\n\n```bash\npip install proper-forms\n```\n\n## How Proper Forms is different\n\n- A field isn\'t tied to a specific HTML tag, so can be presentend in multiple ways. Even the same form can be used in different contexts and have different widgets and styles on each. A set of options as checkboxes, a select multiple, or a comma-separated input? You got it. A date as a calendar or as three selects? No problem.\n\n- Many commonly used built-in validators, and you can also write simple functions to use as custom ones.\n\n- Any field can accept multiple values; as a list or as a comma-separated text.\n\n- All error messages are customizable. The tone of the messages must be able to change or to be translated.\n\n- Incredible easy to integrate with any ORM (object-relational mapper). Why should you need *another* library to do that?\n\n\n## Just show me how it looks\n\n```python\nfrom proper_forms import Form, Email, Text\n\n\nclass CommentForm(Form):\n    email = Email(required=True, check_dns=True)\n    message = Text(\n    \tLongerThan(5, "Please write a longer message"),\n    \trequired=True\n    )\n\n\ndef comment():\n    form = CommentForm(request.POST)\n    if request.method == "POST" and form.validate():\n    \tdata = form.save()\n        ...\n    return render_template("comment.html", form=form)\n\n```\n',
    'author': 'Juan-Pablo Scaletti',
    'author_email': 'juanpablo@jpscaletti.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://proper-forms.scaletti.dev/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
