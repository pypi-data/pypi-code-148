# # To publish into PyPi
# # On a virtual environment:
# # pip install -U wheel setuptools
# # python -m setup sdist bdist_wheel
# # check-manifest -c
# # twine upload dist/*
# #   username: __token__
# #   password: <your_token_here>

# from setuptools import setup

# with open("README.md", "r") as fh:
#     long_description = fh.read()

# setup(
#     name='datalake_utils',
#     version='2.1.1',
#     description="Manipulate data on Amazon S3 using Apache Hadoop filesystem compability",
#     packages=["datalake_utils"],
#     install_requires=['boto3','pandas','pyarrow','fsspec','s3fs'],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "Topic :: Software Development :: Libraries :: Python Modules",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent"
#     ],
#     python_requires='>=3',
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     author="Luis Roberto de Oliveira Moro",
#     author_email="luis.moro@yuca.live",
#     url="https://github.com/yuca-live/yuca-datalake-utils"
# )