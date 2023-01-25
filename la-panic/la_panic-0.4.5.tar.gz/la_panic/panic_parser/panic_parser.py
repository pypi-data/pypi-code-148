import json

import click

from la_panic.panic_parser.kernel_panic import KernelPanic


@click.group()
def cli():
    """ apps cli """
    pass


@cli.group()
def parser():
    pass


@parser.command('parse', cls=click.Command)
@click.argument('panic_file', type=click.File("rt"),
                default="/Users/yanivhasbani/Downloads/panic-full-2022-12-29-094306.000 (1).ips")
def parse(panic_file):
    metadata = json.loads(panic_file.readline())
    panic = KernelPanic(metadata, panic_file.read(), panic_file.name)

    print(f"{panic}\n")
