import argparse

def configure_argparse():
    parser = argparse.ArgumentParser(description='argument parses for upload script.')
    parser.add_argument("--type", type=str, help="radar type")
    parser.add_argument("--version", type=str, help="version name")
    # parser.add_argument("--filepath", type=str, help="file path")
    return parser