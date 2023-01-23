import sys, os
import subprocess

def build(src, dst):
    print(111, src, dst)
    subprocess.run(["ls", "-l", src, dst])
    subprocess.run(["pwd"])
    print("Initializing git submodules")
    subprocess.check_call("git submodule update --init".split(" "))
    print("Retrieving git LFS objects")
    subprocess.check_call("git lfs fetch".split(" "))
    subprocess.check_call("git lfs checkout".split(" "))
    print("Compiling")
    print("#"*10, "Please Be Patient", "#"*10)
    my_env = os.environ.copy()
    my_env['MAKE_OPTS'] = '-j4'
    subprocess.check_call(["./ci/build.sh"], stdout=sys.stdout, shell=True, stderr=subprocess.STDOUT, env=my_env)
    print("Done compiling, thank you for your patience")
    #    subprocess.run("./ci/build.sh")
    #target_file = os.path.join(dst, "mypackage/myfile.txt")
    #os.makedirs(os.path.dirname(target_file), exist_ok=True)
    #download_file_to(dst)
