import os
import sys

import lidarutils.conda_utils as conda_utils

##########################################################################


def find_program_in_env(program):
    """recherche d'un programme dans l'environement"""

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


##########################################################################


def find_program_in_dir(program, dir_path):
    """recherche d'un programme dans un dossier"""

    # recherche dans le dossier courant
    prog = os.path.join(dir_path, program)
    if os.path.exists(prog) and os.path.isfile(prog):
        return prog

    # recherche dans le dossier courant/bin
    prog = os.path.join(dir_path, "bin/" + program)
    if os.path.exists(prog) and os.path.isfile(prog):
        return prog

    # recherche dans le dossier courant/script
    prog = os.path.join(dir_path, "Scripts/" + program)
    if os.path.exists(prog) and os.path.isfile(prog):
        return prog

    # recherche dans le dossier courant/MacOS
    prog = os.path.join(dir_path, "MacOS/" + program)
    if os.path.exists(prog) and os.path.isfile(prog):
        return prog

    return None


##########################################################################


def find_program_in_curent(program):
    """recherche d'un programme dans le dossier courant"""

    # dossier où est le fichier de lancement du script
    dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    return find_program_in_dir(program, dir_path)


##########################################################################


def find_program_in_conda(program):
    """recherche d'un programme dans l'environement conda"""

    path_conda = conda_utils.get_conda_active_path()
    if path_conda is None:
        return None

    # recherche dans l'environnement conda Library (Windows)
    prog = os.path.join(path_conda, "Library\\bin\\" + program)
    if os.path.exists(prog):
        return prog

    # recherche dans l'environnement conda bin (Linux)
    prog = os.path.join(path_conda, "bin/" + program)
    if os.path.exists(prog) and os.path.isfile(prog):
        return prog

    # recherche dans l'environnement conda script
    prog = os.path.join(path_conda, "Scripts/" + program)
    if os.path.exists(prog) and os.path.isfile(prog):
        return prog

    return None


##########################################################################


def find_program(program):
    """recherche d'un programme (environnement + installation)"""

    prog = find_program_in_env(program)
    if prog is not None:
        return prog

    prog = find_program_in_curent(program)
    if prog is not None:
        return prog

    prog = find_program_in_conda(program)
    if prog is not None:
        return prog

    return None
