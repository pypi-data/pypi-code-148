from setuptools import setup


setup(
    name="core-alwaysprep",
    description = "A small example package",
    version="0.1.0",
    author="alwaysprep",
    author_email="alwaysprep@gmail.com",
    package_dir={'src/core': '.'},
    python_requires=">=3.8",
    url="https://github.com/alwaysprep/BazelDemo",
    classifiers = [
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Flask==2.0.0',
    ],
    extras_require={
        "dev": [
            "flake8~=3.7.9",
            "pylint~=2.4.4"
        ]
    }
)
