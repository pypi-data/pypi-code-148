"""This parses HCL files"""
import hcl2
def open_file(file: str) -> dict:
    """
    Opens the terraform file and loads it as a dict
    """
    with open(file, encoding="utf8") as tf_file:
        return hcl2.load(tf_file)


def get_tf_file_type(hcl_dict: dict) -> str:
    """
    Read a HCL dict and determine if its a variable file or a outputs file
    """
    file_types = ["variable", "output"]
    for item in hcl_dict:
        file_type = item
    if file_type not in file_types:
        raise ValueError("Invalid file type. Expected one of: %s" % file_types)
    return file_type


def parse_hcl(hcl_dict: dict, file_type: str) -> "list[dict]":
    """
    Parses the HCL dict given to the function.
    If output file type, will get the name and description
    """

    # Create an empty list to store the final dicts
    final_list = []

    for item in hcl_dict[file_type]:
        # Create a dict to store the info
        temp_dict = {}
        name = list(item.keys())[0]
        temp_dict["name"] = name
        # We can only guarantee that a variable has a name.
        # Not every entry has a default type
        try:
            description = item[name]["description"]
        except KeyError:
            description = None
        temp_dict["description"] = description

        # If we are working with a variable file type, there are more fields to extract
        if file_type == "variable":
            # Not every entry has a  type
            try:
                var_type = item[name]["type"]
            except KeyError:
                var_type = None
            temp_dict["type"] = var_type

            # Not every entry has a default
            try:
                var_default = item[name]["default"]
            except KeyError:
                var_default = None
            temp_dict["default"] = var_default

            # If the variable can be nullable return that, else it cannot be nullable
            try:
                nullable = item[name]["nullable"]
                nullable = True
            except KeyError:
                nullable = False
            temp_dict["nullable"] = nullable

        # Append the dict to the list
        final_list.append(temp_dict)
    return final_list
