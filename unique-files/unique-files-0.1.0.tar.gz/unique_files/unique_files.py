from os import getcwd, listdir
from os.path import abspath, isfile, join


def get_files(directory):
    directory_objects = listdir(directory)
    work_dir = abspath(getcwd())
    target_dir = join(work_dir, directory)

    filenames = filter(
        lambda name: isfile(join(target_dir, name)),
        directory_objects,
    )
    return list(filenames)


def unique_files(dir1, dir2):
    dir_files1 = get_files(dir1)
    dir_files2 = get_files(dir2)
    unique_filenames = sorted(set(dir_files1 + dir_files2))
    return '\n'.join(unique_filenames)
