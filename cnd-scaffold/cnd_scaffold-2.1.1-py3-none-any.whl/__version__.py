import pkg_resources


path = pkg_resources.resource_filename("cnd_scaffold", "VERSION")
__version__ = open(path).read()
