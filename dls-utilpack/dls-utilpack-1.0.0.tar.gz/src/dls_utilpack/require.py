import os


# ----------------------------------------------------------------------------------------
def require(name, dict, keyword):
    if keyword not in dict:
        raise RuntimeError("%s does not contain keyword %s" % (name, keyword))
    return dict[keyword]


# ----------------------------------------------------------------------------------------
def require_environment(name):
    value = os.environ.get(name)

    if value is None:
        raise RuntimeError(f"environment variable {name} is not set")

    return value
