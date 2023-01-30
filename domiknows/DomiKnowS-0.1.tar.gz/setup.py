from setuptools import setup, find_packages

setup(
    name='DomiKnowS',
    version='0.1',
    description='A library provides integration between Domain Knowledge and Deep Learning.',

    long_description ='The library helps specify a problem domain with a conceptual graph including declarations of edges and nodes, as well as any global logical constraints on the graph, against which neural network outputs bounded to the graph can be evaluated. This adds a relational overlay over elements in a network that relates physical concepts in applications.',
    url='https://github.com/HLR/DomiKnowS',
    author='Andrzej Uszok',
    author_email='auszok@ihmc.org',

    packages=find_packages(include=['regr', 'regr.*']),
    
    install_requires=[
       'acls>=1.0.2',
       'Owlready2>=0.30',
       'gurobipy',
       'pandas>=1.1.5',
       'torch>=1.8.1',
       'ordered-set',
       'graphviz',
       'pymongo[tls]',
       'dnspython',
       'sklearn'
    ],
    
    classifiers=[
        'Intended Audience :: Developers',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)