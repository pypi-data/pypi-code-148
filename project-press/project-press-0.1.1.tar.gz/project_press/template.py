import atexit
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

TEMPLATE_NAME = "project-press.yml"


def get_file(template_dir):
    return os.path.join(template_dir, TEMPLATE_NAME)


def get_data(template):
    template_dir = fetch(template)
    template_file = get_file(template_dir)

    with open(template_file, encoding="UTF-8") as fd:
        return yaml.safe_load(fd)


def git_clone(url):
    # Create a temporary folder to be deleted at exit
    tmpdir = tempfile.mkdtemp(prefix="project-press")

    def remove_tmpdir():
        shutil.rmtree(tmpdir)

    atexit.register(remove_tmpdir)

    # Clone the repository
    git = shutil.which("git")
    subprocess.run([git, "clone", url, "repository"], cwd=tmpdir, check=True)

    template_dir = os.path.join(tmpdir, "repository")
    if os.path.isfile(get_file(template_dir)):
        return template_dir
    return None


def fetch(template_dir):
    # If it exists locally, just return it
    if os.path.isdir(template_dir):
        if os.path.isfile(get_file(template_dir)):
            return template_dir

    retval = git_clone(template_dir)
    if retval:
        return retval

    sys.exit(f'error: no template "{TEMPLATE_NAME}" could be found in path "{template_dir}"')
