import pathlib
import re
from alive_progress import alive_bar
import requests

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

def list_files(path, pattern=None, full_names=False, recursive=False):
    """list.file (like in R) function"""
    files = list(list_file_gen(path, pattern, full_names, recursive))
    files_str = [str(file) for file in files]
    files_str.sort()
    return files_str


def list_file_gen(path, pattern=None, full_names=False, recursive=False):
    """List files like in R - generator"""
    path = pathlib.Path(path)
    for file in path.iterdir():
        if file.is_file():
            if pattern is None:
                if full_names:
                    yield file
                else:
                    yield file.name
            elif pattern is not None:
                regex_cond = re.compile(pattern=pattern)
                if regex_cond.search(str(file)):
                    if full_names:
                        yield file
                    else:
                        yield file.name
        elif recursive:
            yield from list_files(file, pattern, full_names, recursive)



def getFilename(url: str) -> str:
    """ Get the filename from a given url.
    Args:
        url (str): A url to get the filename.
    Returns:
        str: The filename.
    """
    return pathlib.Path(
        re.sub(r"\?download=.*", "", url)
    ).name  # remove the download query


def downloadfile(url: str, path: pathlib.Path) -> bool:
    """ Download a file from a given url.

    Args:
        url (str): A url to download the file.
        path (pathlib.Path): A path to save the file.

    Returns:
        bool: True if the file is downloaded.
    """
    with alive_bar(dual_line=True, title="SRcheck") as bar:
        bar.text = (
            "-> Donwloading " +
            bcolors.BOLD + bcolors.OKBLUE + path.name + bcolors.ENDC + 
            " file, please wait..."
        )
        with requests.get(url) as response:
            response.raise_for_status()
            with open(path, "wb") as f:
                f.write(response.content)
        bar()
    return True

