# flake8: noqa
"""Files to be created when initialising a new project.""" ""
from __future__ import annotations

FILES = {
    "main.py": '''
"""Run the default Jade app."""
from __future__ import annotations

import flask
import jade


app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> str:
    """Render the index page."""
    return jade.build_page("/")


jade.build(app)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
    )
''',
    ".jade-config.yaml": """
# Add global variables to the context of all templates
site:
  name: My Site
""",
    "templates/blog.html": """
<!DOCTYPE html>
<html lang="en">

{% include 'include/head.html' %}

{% include 'include/header.html' %}

<body>
  {{content|safe}}
  {% include 'include/post-tiles.html' %}
</body>

</html>
""",
    "templates/default.html": """
<!DOCTYPE html>
<html lang="en">

{% include 'include/head.html' %}

{% include 'include/header.html' %}

<body>
  {{content|safe}}
</body>

</html>
""",
    "templates/include/head.html": """
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{page.title}} | {{site.name}} </title>
  <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
  <link rel="stylesheet" href="/static/main.css" />
</head>
""",
    "templates/include/header.html": """
<header>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/blog">Blog</a></li>
  </ul>
  <hr>
</header>
""",
    "templates/include/post-tiles.html": """
<div>
  <br>
  {% for p in pages.blog | sort(attribute='date', reverse=True) %}
  <a href="{{p.permalink}}">
    <h2>{{p.title}}</h2>
    <p>{{p.date}}</p>
  </a>
  {% endfor %}
</div>
""",
    "static/main.css": """
:root {
  --color-dark: rgb(36, 36, 36);
  --color-light: rgb(210, 210, 210);
  --color-code-bg: rgb(50, 50, 50);
  --color-code-text: rgb(225, 225, 225);
}

* {
  padding: 0;
  margin: 0;
  font-family: sans-serif;
}

header {
  padding: 1rem;
  margin: auto;
}

header ul {
  display: flex;
  justify-content: center;
  align-items: center;
  list-style-type: none;
  padding-bottom: 1rem;
}

header li {
  display: inline;
  margin: 0 1rem;
  padding: 0.5rem;
}

header li:hover {
  text-decoration: underline;
}

body {
  background-color: var(--color-dark);
  color: var(--color-light);
  margin: auto;
  margin-top: 3rem;
  margin-bottom: 3rem;
  max-width: 70%;
}

body img {
  max-height: 500px;
  margin: auto;
  display: block;
}

hr {
  border: 0;
  height: 1px;
  background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(255, 255, 255, 0.75), rgba(0, 0, 0, 0));
}

h1 {
  font-size: 2rem;
  font-weight: 400;
  margin: 1rem 0;
}

h2 {
  font-size: 1.5rem;
  font-weight: 400;
  margin: 1rem 0;
}

h3 {
  font-size: 1.25rem;
  font-weight: 400;
  margin: 1rem 0;
}

h4 {
  font-size: 1rem;
  font-weight: 400;
  margin: 1rem 0;
}

h5 {
  font-size: 0.75rem;
  font-weight: 400;
  margin: 1rem 0;
}

h6 {
  font-size: 0.5rem;
  font-weight: 400;
  margin: 1rem 0;
}

p {
  font-size: 1rem;
  font-weight: 400;
  margin: 1rem 0;
}

a {
  color: var(--color-light);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

ul {
  list-style-type: circle;
}

li {
  font-size: 1rem;
  font-weight: 400;
  margin: 1rem 1rem 1rem 2rem;
}

code {
  background-color: var(--color-code-bg);
  color: var(--color-code-text);
  padding: 0.25rem;
  border-radius: 0.25rem;
  font-family: monospace;
}

pre {
  background-color: var(--color-code-bg);
  color: var(--color-code-text);
  padding: 0.5rem;
  border-radius: 0.25rem;
  font-family: monospace;
}

blockquote {
  border-left: 0.25rem solid var(--color-light);
  padding: 0.5rem;
  margin: 1rem 0;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th {
  background-color: var(--color-light);
  color: var(--color-dark);
  padding: 0.5rem;
  text-align: left;
}

td {
  padding: 0.5rem;
  text-align: left;
}
""",
    "content/home.md": """
---
permalink: /
template: default
title: Welcome to Jade!
---
# Hello!

Welcome to the Jade markdown renderer.

To get started, try editing the `content/home.md` file.

At the top of this file, you will see some `frontmatter`. This is `yaml` formatted content that is passed to the builder, and the template.

While not required, the following `frontmatter` is recommended for each of your pages.

* `permalink` - Where on the site you want the page to register. Defaults to the file's path within the `content` directory, without the file extension.
* `template` - the name of the template in your `templates` directory to render the content into. Defaults to `default`.

## Reserved names

* `page` - You can access the page frontmatter in your templates through the `page` variable. For example, the title for this page would be accessed with `page.title`.

* `pages` - The `pages` variable contains all subdirectories of the `content` directory. This can be useful for things such as rendering a blog home page, with a link to each post in a directory. Note that nested directories are not currently supported.

* `site` - You can also access site parameters, such as the site name through the `site` variable in all of your templates. Any parameters that you need globally should be added to the `.jade-config.yaml` file, under the site key. Try updating the `name` key under `site` in the config file.
""",
    "content/blog.md": """
---
permalink: /blog
template: blog
title: Blog
---
# Welcome to my blog!

Read my articles below...
""",
    "content/blog/first-article.md": """
---
permalink: blog/my-first-article
template: default
title: My First Article
date: 2023-01-27
---
# My very first artcile!

I wrote some content here, and added some images...

![Puppy!](https://upload.wikimedia.org/wikipedia/commons/6/6e/Golde33443.jpg)
""",
    "content/blog/second-article.md": """
---
permalink: blog/my-second-article
template: default
title: My Second Article
date: 2023-01-28
---
# Another post!
Here is some more content...
""",
}
