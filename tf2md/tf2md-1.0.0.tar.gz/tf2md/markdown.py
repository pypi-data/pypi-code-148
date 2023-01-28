"""
This takes in parsed terraform files and creates markdown files based on the
contents
"""
from mdutils.mdutils import MdUtils


def create_output_file(outputs: "list[dict]", output_file: str = "Outputs"):
    """
    Creates a markdown file containing all the terraform outputs
    """
    md_file = MdUtils(
        file_name=f"{output_file}.md", title=f"Terraform Module {output_file}"
    )
    md_file.new_paragraph("This is a auto generated file by running `tf2md`.")
    md_file.new_header(level=1, title=output_file)
    table_data = ["Name", "Description"]
    for output in outputs:
        name = output["name"]
        description = output["description"]
        table_data.extend([f"`{name}`", description])
    rows = len(table_data) / 2
    md_file.new_table(columns=2, rows=int(rows), text=table_data, text_align="center")
    md_file.create_md_file()


def create_variables_file(variables: "list[dict]", variable_file: str = "Variables"):
    """
    Creates a markdown file containing all the terraform variables
    """
    md_file = MdUtils(
        file_name=f"{variable_file}.md", title=f"Terraform Module {variable_file}"
    )
    md_file.new_paragraph("This is a auto generated file by running `tf2md`.")
    md_file.new_header(level=1, title=f"Required {variable_file}")
    table_data = ["Name", "Description", "Type", "Nullable", "Required?"]
    # Work out the colum length
    columns = len(table_data)
    rows = 1
    for variable in variables:
        name = variable["name"]
        description = variable["description"]
        nullable = variable["nullable"]
        # Clean up the var type
        var_type = variable["type"]
        if var_type:
            var_type = tf_var_type_cleaner(var_type)
        default = variable["default"]
        # If the variable has no default its required to be set
        if not default:
            table_data.extend(
                [f"`{name}`", description, f"`{var_type}`", nullable, True]
            )
            rows += 1
    md_file.new_table(
        columns=columns, rows=int(rows), text=table_data, text_align="center"
    )
    md_file.new_line()
    md_file.new_header(level=1, title=f"{variable_file}")

    table_data = ["Name", "Description", "Type", "Nullable", "Default"]
    # Work out the colum length
    columns = len(table_data)
    rows = 1
    for variable in variables:
        name = variable["name"]
        description = variable["description"]
        nullable = variable["nullable"]
        # Clean up the var type
        var_type = variable["type"]
        if var_type:
            var_type = tf_var_type_cleaner(var_type)
        default = variable["default"]
        # If the variable has no default its required to be set
        if default:
            table_data.extend(
                [f"`{name}`", description, f"`{var_type}`", nullable, default]
            )
            rows += 1
    md_file.new_table(
        columns=columns, rows=int(rows), text=table_data, text_align="center"
    )
    md_file.create_md_file()


def tf_var_type_cleaner(var_type: str) -> str:
    """
    This is a helper function that strips the extra chars that gets added to
    the type defintions
    """
    var_type = var_type.replace("$", "")
    var_type = var_type.replace("{", "")
    var_type = var_type.replace("}", "")
    return var_type
