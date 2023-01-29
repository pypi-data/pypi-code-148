def editor_form_errors(exception, message) -> dict:
    errors = {"name": None, "text": None}
    if exception:
        if isinstance(exception, (FileNotFoundError, FileExistsError)):
            errors["name"] = message or str(exception)
        else:
            errors["text"] = message or str(exception)

    return errors
