from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
     name='blur-detector',
     version='0.0.5',
     author="utkarsh-deshmukh",
     author_email="utkarsh.deshmukh@gmail.com",
     description="Uses discrete cosine transform coefficients at multiple scales and uses max pooling on the high frequency coefficients to get the sharp areas in an image.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Utkarsh-Deshmukh/Spatially-Varying-Blur-Detection-python",
     download_url="https://github.com/Utkarsh-Deshmukh/Spatially-Varying-Blur-Detection-python/archive/refs/heads/main.zip",
     install_requires=['numpy', 'opencv-python', 'scipy', 'scikit-image'],
     license='BSD 2-Clause "Simplified" License',
     keywords='Spatially Varying Blur Detection',
     packages=find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: BSD License",
         "Operating System :: OS Independent",
     ],
 )