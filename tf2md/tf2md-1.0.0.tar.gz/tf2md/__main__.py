"""
This manages the CLI of the program, new commands and options all get added here.
If the program is going to grow, logic for each command should be split up,
but for now its fine.
"""

import click
from tf2md.markdown import create_output_file, create_variables_file
from tf2md.parser import open_file, parse_hcl, get_tf_file_type

@click.group()
@click.version_option("1.0.0")
def main():
    """Terraform to markdown generator"""


@main.command()
@click.argument("input_file", type=click.Path(), required=True)
def gen_docs(input_file):
    """
    This generates markdown docs for either variables.tf or outputs.tf
    """
    # Open the terraform file
    hcl_dict = open_file(input_file)
    # Determine the file type, either "variable" or "output"
    file_type = get_tf_file_type(hcl_dict)
    # Parse the file
    parsed_dict = parse_hcl(hcl_dict, file_type)
    # Depending on the file type, create a markdown file in the current dir
    if file_type == "variable":
        create_variables_file(parsed_dict, file_type)
    else:
        create_output_file(parsed_dict, file_type)
