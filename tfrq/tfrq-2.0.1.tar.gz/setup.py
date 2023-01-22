from setuptools import setup

setup(
    name='tfrq',
    version='2.0.1',
    description='A library to parallelize the execution of a function in python',
    long_description="""This library provides an easy way to parallelize the execution of a function in python using the concurrent.futures library. It allows you to run multiple instances of a function simultaneously, making your code run faster and more efficiently. It also provides a simple API for managing the process, allowing you to cancel or wait for the completion of a task. With this library, you can easily take advantage of the power of parallel processing in python.

Here's an example of how you can use the library to parallelize the execution of the `print` function:


```from tfrq import pyrallel_process```
```params = ["Hello", "World", "!"]```
```func = print```
```pyrallel_process(func=func, params=params, num_cores=3)```

This code will call the `print` function in parallel with the given parameters and use 3 cores, so it will print the given parameters in parallel.

Tfrq is an arabic word meaning "To Split", which is the purpose of this simple method, to split the work of a single function into multiple processes as easy as possible.""",
    author='Foad Abo Dahood',
    author_email='Foad.ad5491@gmail.com',
    py_modules=['tfrq'],
    install_requires=['futures==2.2.0'],
)
