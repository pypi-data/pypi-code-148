from typing import Optional


def is_module_importable(
    lib: str,
    raise_exception: bool = False,
    pip_name: Optional[bool] = None,
    message_type="function",
) -> bool:
    """
    Return True if Lib can be imported, False if not when raise_exception is False,
    otherwise raises Exception when not importable.
    :param lib: import name of module to test
    :param raise_exception: Should raise exception or not
    :param pip_name: If raise exception this is required. Part of the error message for install instruction
    :param message_type: Either 'function' or 'module' which will change the style of error message
    :return: True if importable, False if not when raise_exception is False,
    otherwise raises Exception when not importable.
    """
    try:
        __import__(lib)
        return True
    except:
        if raise_exception:
            if message_type == "function":
                raise ImportError(
                    f"You need {lib} for this function. Please run pip install {pip_name}"
                )
            elif message_type == "module":
                raise ImportError(
                    f"You need {lib} for this module. Please run pip install {pip_name}"
                )
            else:
                raise Exception(
                    f"Invalid value for message_type={message_type} should be either function or module"
                )

        return False
