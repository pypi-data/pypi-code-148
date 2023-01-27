
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name="tokopedia_wrapper",
  version="0.4",
  description="Library that wrap tokopedia.com graphql api using requests",
  long_description=README,
  long_description_content_type="text/markdown",
  author="Hariz Sufyan Munawar",
  author_email="contact@munawariz.dev",
  license="Apache License",
  packages=["tokopedia_wrapper"],
  zip_safe=False,
)