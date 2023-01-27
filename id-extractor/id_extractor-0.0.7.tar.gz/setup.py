from setuptools import setup, find_packages

requirements =[
    'Pillow',
    'numpy',
    'tqdm',
    'gdown',
]

pypandoc_enabled = True
try:
    import pypandoc
    print('pandoc enabled')
    long_description = pypandoc.convert_file('README.md', 'rst')
except (IOError, ImportError, ModuleNotFoundError):
    print('WARNING: pandoc not enabled')
    long_description = open('README.md').read()
    pypandoc_enabled = False

setup(
    name="id_extractor",
    version="0.0.7",
    author="Innerverz-by.JJY",
    author_email="pensee0.0a@innerverz.com",
    description="innerverz package - id extractor",
    long_description=long_description,
    python_requires=">=3.6",
    install_requires=requirements,
    packages=find_packages()
    
    
)
