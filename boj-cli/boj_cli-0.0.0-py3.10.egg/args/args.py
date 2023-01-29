from pathlib import Path
import sys

def print_usage():
    print('Usage:')
    print('boj login {boj_handle} {token}')
    print('boj submit {source_path}')


def parse_args():
    if len(sys.argv) < 2:
        print_usage()
        raise SystemExit(1)
