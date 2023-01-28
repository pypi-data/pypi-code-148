"""
https://packaging.python.org/tutorials/packaging-projects/
https://www.markdownguide.org/cheat-sheet/
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="muzadash", # Replace with your own username
    version="0.0.3",
    author="Fikri Muzadi",
    author_email="fikrimuzadi@gmail.com",
    description="This package will get the lates Dashboard Monitoring Indonesia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Insan-Nusantara-Tecnology/latest-indonesia-earthquake",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
	    'beautifulsoup4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],

    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    python_requires='>=3.6',
)