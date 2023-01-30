from setuptools import setup, Extension
from distutils.ccompiler import new_compiler
from platform import processor
from sys import platform
from sysconfig import get_config_var
from os import environ, path
import subprocess
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# debug by setting DISTUTILS_DEBUG env var in shell to anything

assert platform == "darwin"

encoding = 'UTF-8'

def get_macos_target(lib_dirs, lib_name):
    default = get_config_var('MACOSX_DEPLOYMENT_TARGET')
    compiler = new_compiler()
    lib_file = compiler.find_library_file(lib_dirs,lib_name)
    try:
        output = subprocess.check_output('vtool -show-build {}'.format(lib_file), shell=True)
        return next((l for l in output.splitlines() if b'minos' in l), default).split().pop().decode(encoding,errors='ignore')
    except subprocess.CalledProcessError:
        return default

def homebrew_prefix(inpath, package):
    if processor() == 'arm':
        hb_path = "/opt/homebrew"
    else:
        hb_path = "/usr/local"
    if path.exists(path.join(hb_path,inpath)):
        return path.join(hb_path, inpath)
    else:
        return path.join(hb_path, "opt", package, inpath)

def macports_prefix(inpath):
    return path.join("/opt/local/", inpath)

def platform_prefix(inpath, package):
    if path.exists("/opt/local/bin/port"):
        return macports_prefix(inpath)
    elif path.exists("/opt/homebrew/bin/brew") or path.exists("/usr/local/bin/brew"):
        return homebrew_prefix(inpath, package)
    else:
        return (environ.get("PREFIX") or "/").join(inpath)

def pkgconfig(package):
    kw = {}
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    try:
        output = subprocess.check_output('pkg-config --cflags --libs {}'.format(package),shell=True)
        for token in output.strip().split():
            kw.setdefault(flag_map.get(token[:2].decode(encoding,errors='ignore')), []).append(token[2:].decode(encoding))
    finally:
        return kw

try:
    dev_path = subprocess.check_output('xcode-select -p',shell=True).strip().decode(encoding,errors='ignore')
except:
    raise Exception('''You must have either the CLT or Xcode installed to build extensions.
You can install the CLT with `xcode-select --install`, which is much smaller than the full Xcode.
''')

package_name = 'getargv'
kw = pkgconfig(package_name)
kw['include_dirs'].append(platform_prefix('include', package_name))
kw['include_dirs'].append('{}/Library/Frameworks/Python3.framework/Headers'.format(dev_path))
kw['library_dirs'].append(platform_prefix('lib', package_name))
kw['libraries'].append(package_name)

environ["MACOSX_DEPLOYMENT_TARGET"] = get_macos_target(kw['library_dirs'],package_name)

with open("pyproject.toml", mode="rb") as fp:
    project = tomllib.load(fp)['project']
    config = project.copy()
    for k in project.keys():
        if k == 'authors':
            author = config[k][0]
            config['author'] = author['name']
            config['author_email'] = author['email']
            del config[k]
        if k == 'urls':
            config['url'] = config[k]['Homepage']
            del config[k]
        if k == 'license':
            with open(config[k]['file'], mode="r", encoding="utf-8") as l:
                config[k] = l.read().splitlines().pop()
        if k in ['readme', 'requires-python']:
            del config[k]

if __name__ == "__main__":
    setup(
        ext_modules = [ Extension( package_name+".getargv", sources = ['src/getargv/getargvmodule.c'], **kw) ],
        **config
    )
