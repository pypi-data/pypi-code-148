from setuptools import setup, find_packages

setup(
    name='WhileObjects',
    version='0.3',
    packages=find_packages(include=['WhileObjects.py']),
    url='https://github.com/James-Sorrow/ObjectWhileLoop',
    license='MIT',
    author='James Sadler',
    author_email='james.sorrow2023@gmail.com',
    description='A basic interface for implementing Object Oriented While Loops',
    install_requires=[],
    long_description="""## OBJECT ORIENTED WHILE LOOPS (WhileObjects)

Interface for the While class to subclass and make your own Object Oriented While Loops

## DESCRIPTION

While objects are are a new data structure in which we retain reference to our loop indefinitely,
you can pick up the iteration where you left off much later in the script, or instantiate a new loop and not even run it at first

## Installation

`pip install WhileObjects`

## Usage

 i: The current iteration value
 first: The starting value of the loop
 end: The end value of the loop
 op: The operater used to do comparison if the loop should continue
 increment: The value by which the loop should increment/decrement
 calc: The calculated value of the current iteration

 The class While has the following methods:
    isFinished: Returns False if there are still iterations left to be done.
    start: Runs the full loop. The user should implement their calculation in a subclass.
    step: Steps through one iteration of the loop. The user should implement their calculation in a subclass.
    clear: Clears the stored work unit/other data.""",
    long_description_content_type='text/markdown',
)
