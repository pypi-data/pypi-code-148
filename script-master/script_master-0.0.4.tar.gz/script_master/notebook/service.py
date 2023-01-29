def get_notebook_name_from_filename(filename) -> str:
    return filename.rsplit(".", 1)[0]
