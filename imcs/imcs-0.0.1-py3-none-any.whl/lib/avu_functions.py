import sys

from .shell import shell
import locale
import jsonavu

class AVU:
    def __init__(self, a="", v="", u=""):
        self.a = a
        self.v = v
        self.u = u

    def __repr__(self):
        return f"a: {self.a}, v: {self.v}, u: {self.u}"

    def __str__(self):
        return f"a: {self.a}, v: {self.v}, u: {self.u}"

def populate_avu(irods_object, avu, resource_type, ignore):
    """
    performs an
    'imeta add -<resource_type> <irods_object> <avu>' call

    expects:
      @input irods_object - irods collection (directory) or data object (file)
      @input avu          - an avu triplet (dict)
      @resource_type      - the type of the irods_object (C (collection) or d (data object))
    """

    call = "imeta add -{type} {collection} '{avu[a]}' '{avu[v]}' '{avu[u]}'".format(
        type=resource_type, collection=irods_object, avu=avu
    )
    out, err, return_code = shell(call, return_errorcode=True)
    if return_code == 4:
        if ignore:
            pass
        else:
            print(f"WARNING: AVU triplet already exists: {avu}", file=sys.stderr)
    elif return_code:
        print(f"call failed, call was: {call}", file=sys.stderr)
        print(f"Message was: '{out}'", file.sys.stderr)
        print(f"Error code was '{return_code}', stderr: '{err}'", file=sys.stderr)
    return return_code, out, err


def remove_avu(irods_object, avu, resource_type):
    """
    performs an
    'imeta rm -<resource_type> <irods_object> <avu>' call

    expects:
      @input irods_object - irods collection (directory) or data object (file)
      @input avu          - an avu triplet (dict)
      @resource_type      - the type of the irods_object (C (collection) or d (data object))
    """
    call = "imeta rm -{type} {collection} '{avu[a]}' '{avu[v]}' '{avu[u]}'".format(
        type=resource_type, collection=irods_object, avu=avu
    )
    out, err, return_code = shell(call, return_errorcode=True)


def get_all_metada(obj, type):
    call = "imeta ls -{type} {obj}".format(type=type, obj=obj)
    out, err, code = shell(call)
    out = out.splitlines()

    out.pop(0)

    avu_obj, new_line = consume_avu(out)
    avus = []
    if avu_obj is None:
        return avus
    avus.append(avu_obj)
    while new_line:
        avu_obj, new_line = consume_avu(out)
        avus.append(avu_obj)
    return avus


def consume_avu(out):
    avu_obj = {}
    line = out.pop(0).split(": ")
    if line[0].rstrip() == "None":
        return None, None
    avu_obj['a'] = (
       line[1].rstrip()
    )
    avu_obj['v'] = (
        out.pop(0).split(": ")[1].rstrip()
    )
    u = out.pop(0).split(": ")[1].rstrip()
    avu_obj['u'] = u if u != "" else "root_0_s"
    new_line = len(out)
    if new_line:
        out.pop(0)
    return avu_obj, new_line


