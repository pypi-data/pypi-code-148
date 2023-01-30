import importlib
import logging
import os
import sys

logger = logging.getLogger(__name__)


class ImportClassFailed(RuntimeError):
    pass


# -------------------------------------------------------------------------------
def import_class(filename_classname):
    """
    Deprecated.
    """
    return import_filename_classname(filename_classname)


# -------------------------------------------------------------------------------
def import_filename_classname(filename_classname):

    parts = filename_classname.split("::")
    if len(parts) != 2:
        raise RuntimeError(f"{filename_classname} is not of form filename::classname")

    filename = parts[0]
    classname = parts[1]

    return import_classname_from_filename(classname, filename)


# -------------------------------------------------------------------------------
def import_classname_from_filename(classname, filename):

    if not os.path.exists(filename):
        raise ImportClassFailed(f"could not find python file {filename}")

    # Define a module from the python file.
    try:
        module_name = os.path.splitext(os.path.basename(filename))[1][1:]
        spec = importlib.util.spec_from_file_location(module_name, filename)
    except Exception as exception:
        raise ImportClassFailed(
            f"could not get python spec from {filename}: {str(exception)}"
        )

    # Load the module.
    try:
        module = importlib.util.module_from_spec(spec)
    except Exception as exception:
        raise ImportClassFailed(
            f"could not get python module from spec in {filename}: {str(exception)}"
        )

    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exception:
        raise ImportClassFailed(
            f"could not exec python module from spec in {filename}: {str(exception)}"
        )

    # for key, item in module.__dict__.items():
    #     if key == "__builtins__":
    #         continue
    #     description = describe(f"{filename}[{key}]", item)
    #     logger.info(description)

    # Get the class object from the module we just loaded.
    # TODO: Allow class importer to discover a classname within the file.

    if not hasattr(module, classname):
        raise ImportClassFailed(f"could not find class {classname} in {filename}")

    class_object = getattr(module, classname)

    return class_object


# -------------------------------------------------------------------------------
def import_module_classname(module_classname):
    """
    Deprecated.
    """

    return import_modulename_classname(module_classname)


# -------------------------------------------------------------------------------
def import_modulename_classname(module_classname):

    parts = module_classname.split("::")
    if len(parts) != 2:
        raise RuntimeError(f"{module_classname} is not of form modulename::classname")

    modulename = parts[0]
    classname = parts[1]

    return import_classname_from_modulename(classname, modulename)


# -------------------------------------------------------------------------------
def import_classname_from_modulename(classname, modulename):

    # Load the module.
    try:
        module = importlib.import_module(modulename)
    except Exception as exception:
        raise ImportClassFailed(
            f"could not get python module from {modulename}: {str(exception)}"
        )

    # Get the class object from the module we just loaded.
    # TODO: Allow class importer to discover a classname within the module.

    if not hasattr(module, classname):
        raise ImportClassFailed(
            f"could not find class {classname} in module {modulename}"
        )

    class_object = getattr(module, classname)

    return class_object
