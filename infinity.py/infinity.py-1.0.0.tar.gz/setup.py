from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

requirements = [
    "requests",
    "json_minify", 
    "six"
]

setup(
    name="infinity.py",
    license='MIT',
    author="Minori",
    version="1.0.0",
    author_email="minorigithub@gmail.com",
    description="Library for Infinity",
    packages=find_packages(),
    long_description=long_description,
    install_requires=requirements,
    keywords=[
        'tda',
        'infinity',
        'infinity.py',
        'infinity-bot',
        'api',
        'python',
        'python3',
        'python3.x',
        'minori'
    ],
    python_requires='>=3.6',
)
