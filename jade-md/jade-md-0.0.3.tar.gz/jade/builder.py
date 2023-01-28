"""Return routes for each page in the content directory."""
from __future__ import annotations

import pathlib
from typing import Dict
from typing import List
from typing import Union

import flask

from jade.config import get_config
from jade.page import Page

PATHS = {}


def build(app: flask.Flask) -> None:
    """
    Build all md pages in the content directory or subdirectories.

    Params
    ------
    app: :class:`Flask`
        The Flask app to add the routes to.
    """
    files = pathlib.Path("content").rglob("*.md")

    for file in files:
        page = Page.from_path(file)
        route = _build_url(page, file)

        PATHS[route] = page

        full_route = f"{route}<path:path>"

        try:
            app.route(full_route, methods=["GET"])(build_page)
        except AssertionError:
            pass


def build_page(path: str) -> str:
    """
    Build a page from the content at the given path.

    Params
    ------
    path: :class:`str`
        The path to the content.

    Returns
    -------
    :class:`str` - The rendered HTML.
    """
    if path == "/":
        path = ""
    page = PATHS.get(f"/{path}")

    if page is None:
        flask.abort(404)

    return flask.render_template(
        f"{page.frontmatter.get('template', 'default')}.html",
        content=page.render_content(),
        page=page.frontmatter,
        **_get_files(),
        **get_config(),
    )


def _build_url(page: Page, file: pathlib.Path) -> str:
    """
    Build a URL for the given page.

    Params
    ------
    page: :class:`Page`
        The page to build the URL for.
    file: :class:`pathlib.Path`
        The path to the file.

    Returns
    -------
    :class:`str` - The URL.
    """
    route_name = str(file).split("content")[1].replace(".md", "")
    route = page.frontmatter.get("permalink", route_name)

    if not route.startswith("/"):
        return f"/{route}"
    return route


def _get_files() -> Dict[str, Union[Dict[str, List[Page]], List[Page]]]:
    """
    Get all the files in the content directory.

    Returns
    -------
    :class:`Dict[str, Union[Dict[str, List[Page]], List[Page]]]` - A list of dicts in
    the format {file: Page(file)}
    """
    paths = pathlib.Path("content").rglob("*.md")
    pages = {"pages": {}}

    for path in paths:
        if path.is_file():
            pass

        directory = path.parent

        if directory.name not in pages["pages"]:
            pages["pages"][directory.name] = []

            for file in directory.iterdir():
                if file.is_file():
                    page = Page.from_path(file)
                    pages["pages"][directory.name].append(page)

    return pages
