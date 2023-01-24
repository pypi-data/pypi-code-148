import argparse
from logpandas.core import parse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filepath")
    parser.add_argument("output_filepath")
    args = parser.parse_args()

    assert args.output_filepath.endswith(".csv") \
        or args.output_filepath.endswith(".csv.gz"), \
        "Output filepath not supported"

    df = parse(args.input_filepath)
    df.to_csv(args.output_filepath, index=False)
