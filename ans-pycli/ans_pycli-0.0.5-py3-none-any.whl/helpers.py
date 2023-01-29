def no_action(): print("No action")


def default(*values, _type=None):
    """ Return the first value that is not None and is of the correct type """
    check_type = _type is not None

    def typecheck(val):
        if not check_type:
            return True
        if _type is callable:
            return callable(val)
        return isinstance(val, _type)

    for value in values:
        type_ok = typecheck(value)
        not_none = value is not None

        if type_ok and not_none:
            return value

    return None


def get_val(obj, name: str, *defaults, _type=None):
    """ Get the value of an attribute of an object.
    - If the attribute is not None and is of the correct type, return it
    - Otherwise, return the first default value that is not None
    - All values are checked for type if _type is not None
    - If no default value is found, return None
    """
    val = getattr(obj, name)
    return default(val, *defaults, _type=_type)


def set_val(obj, name: str, *defaults, _type=None):
    """ Set and return the value of an attribute of an object.
    - if the value is not None and is of the correct type, set it
    - Otherwise, set the first default value that is not None
    - All values are checked for type if _type is not None
    - If no default value is found or values is not of correct type, return None
    """
    val = get_val(obj, name, *defaults, _type=_type)

    if val is not None:
        setattr(obj, name, val)
        return val

    return None
