import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "meili_ros_lib",
    version = "0.0.1",
    author = "nuriafe",
    author_email = "nuria@meilirobots.com",
    description = "library combining common functions of meili agent ros1 and ros2",
    url = "https://gitlab.com/meilirobots/ros/meili_ros_lib",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)
