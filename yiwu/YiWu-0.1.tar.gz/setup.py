import setuptools
 
f = open("README.md", "r", encoding="utf-8")
long_description = f.read()
f.close()

#for formal
setuptools.setup(
    name="YiWu",
    version="0.1",
    author="Yijie Xia",  
    author_email="yijiexia@pku.edu.cn", 
    description="A Python AI package for chess",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
#        'Development Status :: 5 - Production/Stable',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
