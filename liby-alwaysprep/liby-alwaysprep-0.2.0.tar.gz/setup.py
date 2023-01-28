from setuptools import setup


setup(
    name="liby-alwaysprep",
    description = "A small example package",
    version="0.2.0",
    author="alwaysprep",
    author_email="alwaysprep@gmail.com",
    package_dir={'src/liby': '.'},
    python_requires=">=3.8",
    url="https://github.com/alwaysprep/BazelDemo",
    classifiers = [
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'core-alwaysprep==0.1.0'
    ],
    extras_require={
        "dev": [
            "flake8~=3.7.9",
            "pylint~=2.4.4"
        ]
    }
)
