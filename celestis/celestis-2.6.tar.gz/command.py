import click
from create_files import create_project_files
import sqlite3
from celestis.model import database

@click.command()
@click.argument("subcommand", required=True)
def celestis(subcommand):
    if subcommand=="start-project":
        project_name = str(input("What is your project name?"))
        create_project_files(project_name)
    elif subcommand == "create-db":
        conn = sqlite3.connect("db.sqlite3")
        conn.close()
        click.echo("The database file has been created")
    elif subcommand == "update-db":
        database.read_db(os.getcwd())
        click.echo("Database has been updated!")

