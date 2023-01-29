import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="ira_auth_m2m_client",
    version="0.1.0",
    author="Daryl Correa (Epicode)",
    author_email="daryl.correa@epicode.in",
    description="IraAuthM2M authenticates an application by IraAuth so that it can access APIs protected by IraAuth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/epicira/ira-auth-m2m-client",
    project_urls = {
        "Bug Tracker": "https://github.com/epicira/ira-auth-m2m-client/issues"
    },
    license="MIT",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "httpx >= 0.23.3",
        "Authlib >= 1.2.0"
    ]
)
