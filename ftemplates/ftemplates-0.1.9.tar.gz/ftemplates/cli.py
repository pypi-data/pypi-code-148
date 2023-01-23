"""
Author: smv7
Date: 2022/03/29
Description: CLI application that creates files based on templates."""


import os
from datetime import datetime
from pathlib import Path

import click


TEMP_DIR_PATH = Path(__file__).parent / "available_templates"


@click.group()
def ftemp():
    click.echo('')


@ftemp.command()
@click.option('--new-file', is_flag=True, default=True, help='(Default) Create new file using an existing template.')
@click.option('--new-template', is_flag=True, default=None, help='Create a new template.')
@click.option('--override', is_flag=True, default=None, help='Override file with same name created with template.')
@click.argument('file_to_use', required=True)
@click.argument('file_to_create', required=True)
def create(new_file, new_template, override, file_to_use, file_to_create):
    """Creates a new template or a new file using an existing template."""

    # If the "--new-template" flag is used, the program checks if already exist a file with the name given by the
    # argument. If not exist, creates the new template in the "templates" folder of this project.
    if new_template:
        # Check if the file that'll be used to create the new template exists.
        if Path(file_to_use).exists():
            with open(file_to_use, 'r') as file4template:
                # Create template file if doesn't exists or override it if specified.
                template_exists: bool = TEMP_DIR_PATH.joinpath(file_to_create).exists()
                if (template_exists and override) or not template_exists:
                    click.echo(f'Creating new template "{file_to_create}"...\n')
                    with TEMP_DIR_PATH.joinpath(file_to_create).open("w" if override else "x") as template_to_create:
                        for line in file4template:
                            template_to_create.write(line) 
                    click.echo(f'\t"{file_to_create}" successfully created.')
                    click.echo(f'\t"{file_to_create}" is now available to use as template for new files.')
                else:
                    click.echo(f'A template with name "{file_to_create}" already exist.')
                    click.echo(f'If you want to override it use "--override" option.')
                    return None
        else:
            click.echo(f'The file to use "{file_to_use}" do not exist.')
            return None
        
    # If "--new-file" flag is used (or none is set), the program creates a new file in the path given by the argument
    # passed (default is current directory) using a template from the "templates" folder as second argument.
    elif new_file:
        # Create file if doesn't exists or override it if specified.
        if TEMP_DIR_PATH.joinpath(file_to_use).exists():
            with TEMP_DIR_PATH.joinpath(file_to_use).open("rt") as template4file:
                # Check if new file to be created with template already exist. The new file is created if don't exist or if
                # exist but the "--override" option is set. "file_to_create" can be a path too.
                file_exists = Path(file_to_create).exists()
                if (file_exists and override) or not file_exists:
                    with Path(file_to_create).open("w" if override else "x") as f:
                        click.echo((f'{"Overriding" if override else "Creating new file"} "{file_to_create}" with '
                                     f'template "{file_to_use}"...\n'))
                        for line in template4file:
                            f.write(line)
                        click.echo(f'\t"{file_to_create}" successfully created.')
                else:
                    click.echo(f'A file with name "{file_to_create}" already exist.')
                    click.echo(f'If you want to override it use "--override" option.')
                    return None
        else:
            click.echo("The template file doesn't exists.")
            return None
                    
    click.echo('\nAll operations successfully executed.')
    return None


@ftemp.command()
def list():
    """Lists the existing templates."""

    click.echo(f'Listing {TEMP_DIR_PATH.as_posix()}...\n')
    templates = tuple(TEMP_DIR_PATH.iterdir())
    if len(templates) > 0:
        click.echo("TEMPLATES:\n")
        for template in templates:
            click.echo(f"\t- {template.name}")
        click.echo('')
    else:
        click.echo("You've no templates yet.\n")
        click.echo("Use \"create\" subcommand to make some.")
        
    return None
    
