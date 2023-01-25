import rich_click as click
import asyncio
from arkitekt.cli.run import run_module
from arkitekt.cli.scan import scan_module
from arkitekt.cli.dev import dev_module
from arkitekt.cli.deploy import generate_deployment
from arkitekt.cli.init import Manifest, load_manifest, write_manifest
import subprocess
from rich.console import Console
from rich.progress import Progress, TextColumn
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
import os




console = Console()

logo = """
            _    _ _       _    _   
  __ _ _ __| | _(_) |_ ___| | _| |_ 
 / _` | '__| |/ / | __/ _ \ |/ / __|
| (_| | |  |   <| | ||  __/   <| |_ 
 \__,_|_|  |_|\_\_|\__\___|_|\_\\__|
                                                                   
"""

welcome = """
Welcome to Arkitekt. Arkitekt is a framework for building beautiful and fast (serverless) APIs around
your python code.
To get started, we need some information about your app. You can always change this later.
"""


template_app = """
from arkitekt import register

@register
def test_func(a: int, b: float) -> int:
    return int(a+b)


"""




click.rich_click.HEADER_TEXT = logo
click.rich_click.ERRORS_EPILOGUE = "To find out more, visit [link=https://jhnnsrs.github.io/doks]https://jhnnsrs.github.io/doks[/link]"
click.rich_click.USE_RICH_MARKUP = True


@click.group()
@click.pass_context
def cli(ctx):
    """Arkitekt is a framework for building beautiful and fast (serverless) APIs around
    your python code. 
    It is build on top of Rekuest and is designed to be easy to use."""
    pass

@cli.command()
@click.option('--builder', help='The builder used to construct the app', type=click.Choice(["arkitekt.builders.easy", "arkitekt.builders.advanced"]), default="arkitekt.builders.easy")
def run(builder):
    """Runs the arkitekt app"""
    manifest = load_manifest()
    if not manifest:
        raise click.ClickException("No manifest found. Please run `arkitekt init` first before deploying an arkitekt app.")

    asyncio.run(run_module(manifest.identifier, manifest.version, manifest.entrypoint, builder=builder))


@cli.command()
@click.option('--builder', help='The builder used to construct the app', type=click.Choice(["arkitekt.builders.easy", "arkitekt.builders.advanced"]), default="arkitekt.builders.easy")
def dev(builder):
    """Runs the arkitekt app"""
    manifest = load_manifest()
    if not manifest:
        raise click.ClickException("No manifest found. Please run `arkitekt init` first before deploying an arkitekt app.")

    asyncio.run(dev_module(manifest.identifier, manifest.version, manifest.entrypoint, builder=builder))


@cli.command()
@click.option('--app', prompt='The module path', help='The module path', default="app")
def scan(app):
    """Scans your arkitekt app for leaking variables"""
    variables = scan_module(app)

    if not variables:
        click.echo("No dangerous variables found. You are good to go!")
        return

    for key, value in variables.items():
        click.echo(f"{key}: {value}")

@cli.group()
def deploy():
    """ Deploys the arkitekt app to a specific platform (like port)"""
    pass





def search_username_in_docker_info(docker_info: str):
    for line in docker_info.splitlines():
        if "Username" in line:
            return line.split(":")[1].strip()


@deploy.command()
@click.option('--version', help='The version of your app')
@click.option('--dockerfile', help='The dockerfile to use')
@click.option('--nopush', help='Skip push')
@click.option('--tag', help='The tag to use')
def port(version, dockerfile, nopush, tag):
    """Deploys the arkitekt app to port"""

    manifest = load_manifest()
    if not manifest:
        raise click.ClickException("No manifest found. Please run `arkitekt init` first before deploying an arkitekt app.")


    md = Panel("Deploying to Port", subtitle="This may take a while...", subtitle_align="right")
    console.print(md)
    version = version or manifest.version
    identifier = manifest.identifier
    entrypoint = manifest.entrypoint

    if version == "dev":
        raise click.ClickException("You cannot deploy a dev version. Please change the version in your manifest. Or use the --version flag.")

    with console.status("Searching username"):
        docker_info = subprocess.check_output(["docker", "info"]).decode("utf-8")
        username = search_username_in_docker_info(docker_info)
        if not username:
            raise click.ClickException("Could not find username in docker info. Have you logged in? Try 'docker login'")


    tag = tag or click.prompt("The tag to use", default=f"{username}/{manifest.identifier}:{version}")        
    deployed = {}

    md = Panel("Building Docker Container")
    console.print(md)

    docker_run = subprocess.run(["docker", "build", "-t", tag, "-f", dockerfile or "Dockerfile", "."])
    if docker_run.returncode != 0:
        raise click.ClickException("Could not build docker container")

    if not nopush:
        md = Panel("Pushing Docker Container")
        console.print(md)
        docker_run = subprocess.run(["docker", "push", tag])
        if docker_run.returncode != 0:
            raise click.ClickException("Could not push docker container")



    deployed["docker"] = tag

    generate_deployment(identifier, version, entrypoint, deployed, deployer="arkitekt.deployers.port.dockerbuild")



@cli.command()
@click.option('--identifier', help='The identifier of your app')
@click.option('--version', help='The version of your app')
@click.option('--entrypoint', help='The version of your app')
@click.option('--author', help='The author of your app')
@click.option('--builder', help='The builder used to construct the app')
def init(identifier, version, author, entrypoint, builder):
    """Initializes the arkitekt app"""

    md = Panel(logo + welcome, title="Welcome to Arkitekt", title_align="center")
    console.print(md)

    oldmanifest = load_manifest()

    if oldmanifest:
        if not click.confirm('Do you want to overwrite your old configuration'):
            return

    manifest = Manifest(
            identifier=identifier or click.prompt("Your apps identifier", default=getattr(oldmanifest, "identifier", os.path.basename(os.getcwd()))),
            version=version or click.prompt("The apps version", default=getattr(oldmanifest, "version", "dev")),
            entrypoint=entrypoint or click.prompt("The module path", default=getattr(oldmanifest, "entrypoint", "app")),
            author=author or click.prompt("The apps author", default=getattr(oldmanifest, "author", "john doe")),
            builder=builder or click.prompt("The builder to use", default=getattr(oldmanifest, "builder", "arkitekt.builders.easy"))
        )


    if not os.path.exists(f"{entrypoint}.py"):
        if click.confirm('Entrypoint does not exists. Do you want to generate a python file?'):
            with open(f"{entrypoint}.py", "w") as f:
                f.write(template_app)


    write_manifest(manifest)


if __name__ == '__main__':
    cli()
   