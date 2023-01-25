from setuptools import setup


# Metadata goes in pyproject.toml. These are here for GitHub's dependency graph.
setup(
    name="quart-sqlalchemy",
    install_requires=["quart~=0.18.3", "SQLAlchemy~=1.4.46", "anyio~=3.3.4"],
)
