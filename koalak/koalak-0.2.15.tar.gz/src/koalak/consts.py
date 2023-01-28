PACKAGE_NAME = "koalak"
# Name used to create the home path for other libraries "~/.koalak/<library>"
HOMEPATH_NAME = "koalak"
VERSION = "0.2.15"
OBJECT_STORAGE_KEY = "__koalak__"

# Keys inside __koalak__ attribute
KEY_ABSTRACT = "abstract"
KEY_PLUGIN_MANAGER = "plugin_manager"
KEY_ATTRIBUTES_CONSTRAINTS = "attributes_constraints"
# This key must be present in the dict generated for metadata, to know
#  that the metadata dict is made with a method and not a simple dict
KEY_METADATA_MADE_WITH_METHOD = "__koalak_metadata__"
