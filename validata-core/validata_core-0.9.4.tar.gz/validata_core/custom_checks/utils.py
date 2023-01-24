from frictionless import errors


def build_check_error(custom_check_code: str, note: str):
    custom_note = f"{custom_check_code!r}: {note}"
    return errors.CheckError(note=custom_note)


def ignore_custom_check_for_empty_cell(func):
    def wrapped_function(*args, **kwargs):
        cell_value = args[1][args[0].get("column")]
        # Empty cell, don't check!
        if not cell_value:
            return []
        return func(*args, **kwargs)
    return wrapped_function


def valued(val):
    return not (val is None)


def ignore_custom_check_on_multiple_columns_for_empty_cell(func):
    def wrapped_function(*args, **kwargs):
        cell_values = [args[1][col] for col in args[0].get_all_columns()]
        if not all(valued(cell_value) for cell_value in cell_values):
            return []
        return func(*args, **kwargs)
    return wrapped_function
