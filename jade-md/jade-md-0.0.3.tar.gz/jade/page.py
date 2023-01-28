"""Render Markdown content to HTML."""
from __future__ import annotations

import typing

import jinja2
import markdown
import yaml

import jade.path as path


class Page:
    """Represents a page of content."""

    def __init__(self, frontmatter: typing.Dict[str, str], content: str) -> Page:
        """
        Representation of a Markdown page.

        Splits the frontmatter from the content and adds the frontmatter as
        attributes to the Page object.

        Params
        ------
        frontmatter: :class:`Dict[str, str]`
            The frontmatter yaml at the top of the page.

        content: :class:`str`
            The page content as Markdown.
        """
        self.frontmatter = frontmatter
        self.content = content
        for key, value in frontmatter.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        """Return a string representation of this Page."""
        return f"Page({self.frontmatter}, {self.content})"

    @classmethod
    def from_path(cls, __path: str, /) -> Page:
        """Create a Page from the content at the given path."""
        return cls.from_markdown(cls.open_content(__path))

    @classmethod
    def from_markdown(cls, md: str) -> Page:
        """Create a Page from the given Markdown content."""
        try:
            frontmatter, content = md.split("---", 2)[1:]
            frontmatter = yaml.safe_load(frontmatter)

            return cls(frontmatter, content)
        except ValueError:
            return cls({}, md)

    @staticmethod
    def open_content(__path: str, /) -> str:
        """Open the content at the given path and return it as a string."""
        __path = path.path(__path)
        if not path.exists(__path):
            raise FileNotFoundError(f"File {__path} does not exist.")
        with open(__path) as file:
            return file.read()

    def render_content(self, **kwargs) -> str:
        """Render the content of this page to HTML."""
        html = markdown.markdown(self.content)
        return jinja2.Template(html).render(**kwargs)
