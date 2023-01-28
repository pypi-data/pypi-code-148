import sys
import platform

def pyversion(fullpython=False, fullversion=False, tags=False, date=False, compiler=False, implementation=False, revision=False):
    if fullpython:
        return f'python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} {sys.version_info.releaselevel} {platform.python_build()[0]} {platform.python_build()[1]} {platform.python_compiler()} {platform.python_implementation()} {platform.python_revision()}'
    if fullversion:
        return f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
    if tags:
        return platform.python_build()[0]
    if date:
        return platform.python_build()[1]
    if compiler:
        return platform.python_compiler()
    if implementation:
        return platform.python_implementation()
    if revision:
        return platform.python_revision()
    return f'{sys.version_info.major}.{sys.version_info.minor}'

def osversion(fullos=False, fullversion=False, type=False, cuser=False, processor=False):
    if fullos:
        return f'{platform.node()} {platform.platform()} {platform.machine()} {platform.architecture()[0]} {platform.processor()}'
    if fullversion:
        return f'{platform.system()} {platform.version()}'
    if type:
        return platform.architecture()[0]
    if cuser:
        return platform.node()
    if processor:
        return platform.processor()

    return platform.release()