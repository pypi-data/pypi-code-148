import os

def ensure_local_repo():
    repo_file = "/etc/apt/sources.list.d/robin-local.list"
    # get the current version of ubuntu 
    ubuntu_version = os.popen("lsb_release -cs").read().strip()
    # set the contents of the repo file
    contents = "deb file:///opt/robin/repo/ " + ubuntu_version + " main"

    if os.path.isfile(repo_file):
        print("Repo file exists, checking contents at " + repo_file)
        # Ensure the contents of the file match the contents of the variable
        with open(repo_file, "r") as stream:
            if stream.read() == contents:
                print("Repo file contents match")
                return True
            else:
                print("Repo file contents do not match, overwriting.")
                # Copy the current file to a backup
                os.rename(repo_file, repo_file + ".bak")
                with open(repo_file, "w") as stream:
                    stream.write(contents)
                    return True
    else:
        print("Repo file does not exist, creating it at " + repo_file)
        with open(repo_file, "w") as stream:
            stream.write(contents)
            return True