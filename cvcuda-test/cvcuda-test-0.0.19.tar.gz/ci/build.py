import sys, os
import subprocess

def build(setuptools_kwargs):
    print(setuptools_kwargs)
    build_dir = "build-rel"#os.path.join(".", "build-rel")
    os.makedirs(build_dir)

    print("Initializing git submodules")
    subprocess.check_call("git submodule update --init".split(" "))

    print("Retrieving git LFS objects")
    subprocess.check_call("git lfs fetch".split(" "))
    subprocess.check_call("git lfs checkout".split(" "))

    print("Building to", build_dir)
    print("#"*10, "Please Be Patient", "#"*10)
    my_env = os.environ.copy()

    my_env['MAKE_OPTS'] = '-j4'
    subprocess.check_call(
        ["./ci/build.sh", "release", os.path.join("build-rel")],
        stdout=sys.stdout,
        stderr=subprocess.STDOUT,
        env=my_env,
        shell=True)
    #    subprocess.run("./ci/build.sh")
    #target_file = os.path.join(dst, "mypackage/myfile.txt")
    #os.makedirs(os.path.dirname(target_file), exist_ok=True)
    #os.makedirs(os.path.dirname(target_file), exist_ok=True)
    #download_file_to(dst)
