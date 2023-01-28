from setuptools import find_packages, setup
with open("README.md", 'r') as f:
    long_description = f.read()


setup(
    name="fib_py_example",
    version="0.1.1",
    author="David zhang",
    author_email="spartazhangzhang@gmail.com",
    description="Calculates a Fibonacci number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spartazhangzhang/python-fib",

    install_requires=[],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",

        "Programming Language :: Python :: 3",

        "Operating System :: OS Independent",

    ],
    python_requires='>=3.10',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'fib-number = fib_py_example.cmd.fib_numb:fib_numb',
    ],

},
)