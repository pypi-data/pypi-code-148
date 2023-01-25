from setuptools import setup, find_packages

setup(name="messanger_project_server_parts",
      version="0.0.1",
      description="messanger_project_server_parts",
      author="Alex Bodrov",
      author_email="alexvbodrov@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
