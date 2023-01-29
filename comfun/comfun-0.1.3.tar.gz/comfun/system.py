import logging
import shutil


def backup_bash_history(fpath="/home/findux/.bash_history") -> None:
    shutil.copy(fpath, fpath + "_BACKUP")


def load_bash_history(fpath="/home/findux/.bash_history") -> list[str]:
    with open(fpath, "r") as f:
        lines = f.readlines()
    logging.info(f"Loaded {len(lines)} lines.")
    return lines


def get_bash_duplicates(fpath="/home/findux/.bash_history") -> list[int]:
    """
    Gets the indeces of duplicate lines in the bash history.
    :param fpath:
    :return:
    """
    lines = load_bash_history(fpath=fpath)
    duplicates = []
    for i, line in enumerate(lines):
        if line in lines[i + 1:]:
            duplicates.append(i)
    logging.info(f"Found {len(duplicates)} duplicates")
    return duplicates


def rm_bash_duplicates(fpath="/home/findux/.bash_history"):
    """
    Removed duplicates from .bash_history
    :param fpath:
    :return:
    """
    backup_bash_history(fpath=fpath)
    duplicate_indeces = get_bash_duplicates(fpath=fpath)
    lines = load_bash_history(fpath=fpath)
    lines_to_keep = []
    for i, line in enumerate(lines):
        if i not in duplicate_indeces:
            lines_to_keep.append(line)

    with open(fpath, "w") as f:
        f.writelines(lines_to_keep)
    logging.info(f"Wrote {len(lines_to_keep)} lines.")


if __name__ == "__main__":
    loglvl = logging.DEBUG
    logformat = "[%(levelname)s]\t%(funcName)s:  %(message)s"
    logging.basicConfig(level=loglvl, format=logformat)
    # logging.disable()

    rm_bash_duplicates()
