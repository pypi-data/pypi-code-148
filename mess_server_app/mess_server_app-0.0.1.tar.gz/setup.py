from setuptools import setup, find_packages

setup(name="mess_server_app",
      version="0.0.1",
      description="mess_server_app",
      author="KosarevDV",
      author_email="dlinnii21@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
