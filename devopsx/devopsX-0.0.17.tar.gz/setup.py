from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='devopsX',  # Required
    version='0.0.17',  # Required
    author="Paulo Sérgio dos Santos Júnior",
    author_email="paulossjunior@gmail.com",
    description="DevOps é um produto da Microsoft que fornece controle de versão, relatórios, gerenciamento de requisitos, gerenciamento de projetos, compilações automatizadas, gerenciamento de laboratório, recursos de gerenciamento de testes e versões.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/integration_seon/libs/application/tfs",
    packages=find_packages(),
    
    install_requires=[
        'azure-devops',
        'requestx',
        'factory-boy'
    ],

    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    setup_requires=['wheel'],
    
)


