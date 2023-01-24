import argparse
from os import getcwd
from os.path import abspath, join

from unique_files import unique_files


def entrypoint():
    """Parse args."""
    parser = argparse.ArgumentParser(
        description='Returns a list of unique files from two directories',
    )
    parser.add_argument('first_dir', type=str)
    parser.add_argument('second_dir', type=str)

    args = parser.parse_args()
    dir1 = args.first_dir
    dir2 = args.second_dir

    current_dir = abspath(getcwd())

    path2dir1 = join(current_dir, dir1)
    path2dir2 = join(current_dir, dir2)

    print(unique_files(path2dir1, path2dir2))


def main():
    """Run all others in this files."""
    entrypoint()


if __name__ == '__main__':
    main()
