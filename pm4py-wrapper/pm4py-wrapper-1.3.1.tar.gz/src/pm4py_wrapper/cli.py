from pathlib import Path

import click

from pm4py_wrapper.wrapper import convert_xes_to_csv, convert_csv_to_xes


@click.group()
@click.option('-i', '--input_log', default=None, required=True, type=Path, help='Path to the input event log.')
@click.option('-o', '--output_dir', default=Path('.'), type=Path, help='Path to the output directory.')
def main(input_log, output_dir):
    # This is a main group which includes other commands specified below.
    pass


@main.command()
@click.pass_context
def xes_to_csv(ctx):
    log_path: Path = ctx.parent.params['input_log']
    output_dir: Path = ctx.parent.params['output_dir']
    output_path = output_dir / log_path.with_suffix('.csv').name
    output_dir.mkdir(parents=True, exist_ok=True)
    convert_xes_to_csv(log_path, output_path)


@main.command()
@click.pass_context
def csv_to_xes(ctx):
    log_path: Path = ctx.parent.params['input_log']
    output_dir: Path = ctx.parent.params['output_dir']
    output_path = output_dir / log_path.with_suffix('.xes').name
    output_dir.mkdir(parents=True, exist_ok=True)
    convert_csv_to_xes(log_path, output_path)


if __name__ == '__main__':
    main()
