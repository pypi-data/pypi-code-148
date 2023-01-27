from setuptools import setup, find_packages


requirements =[
    'Pillow',
    'numpy',
    'tqdm',
    'gdown',
]

setup(
    name="id_extractor",
    version="0.0.6",
    author="Innerverz-by.JJY",
    author_email="pensee0.0a@innerverz.com",
    description="innerverz package - id extractor",
    python_requires=">=3.6",
    install_requires=requirements,
    packages=find_packages()
    
    
)
