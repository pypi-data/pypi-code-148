import json
import os
import sys


def get_pwd(): return os.path.dirname(os.path.abspath(__file__))


def resolve_path(path):

    path = os.path.expandvars(path)

    if not os.path.isabs(path):
        pwd = get_pwd()
        path = os.path.join(pwd, path)

    return os.path.normpath(path)


# pyfieモジュールのトップレベルに動的に属性を追加するための機構
_g_toplevel_target = __name__


def _set_toplevel_target(module_name):
    global _g_toplevel_target
    _g_toplevel_target = module_name


def _set_toplevel(obj, name):
    sys.modules[_g_toplevel_target].__dict__[name] = obj


def _get_toplevel(name):
    return sys.modules[_g_toplevel_target].__dict__.get(name, None)


def _is_toplevel(name):
    return name in sys.modules[_g_toplevel_target].__dict__


def _del_toplevel(name):
    if _is_toplevel(name):
        del sys.modules[_g_toplevel_target].__dict__[name]


def normstr(s):
    if isinstance(s, str):
        return s
    if isinstance(s, bytes):
        return s.decode('utf-8')

    return ""


def get_dict_value_recursive(dic, key_list, default=None):
    for key in key_list:
        if not key in dic:
            return default

        dic = dic[key]

    return dic


def load_json_obj(file_path, key_list, default=None):
    jobj = None

    try:
        jf = open(resolve_path(file_path), 'r', encoding="utf-8")
        jobj = json.load(jf)
    finally:
        jf.close()

    if not jobj:
        return default

    return get_dict_value_recursive(jobj, key_list, default)


def get_platform(default="Windows"):
    try:
        import platform
        return platform.system()

    except Exception:
        pass

    return default


def get_processor():
    import platform

    processor = platform.processor()
    if(processor):
        return processor

    processor = platform.machine()
    if(processor):
        return processor

    return ""


def is_sequence(obj):
    if isinstance(obj, str):
        return False
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__")


def copy_sequence(src, dst, conv_type=None):
    # シーケンスである src から dst へ再帰的な要素のコピーを行う.
    # dst の要素に対応する src の要素が無い場合は例外が飛ぶ.

    if not (is_sequence(src) and is_sequence(dst)):
        raise RuntimeError("can't copy from", src, "to", dst)

    for i in range(len(dst)):
        if is_sequence(dst[i]):  # 多次元配列どうしのコピー.
            copy_sequence(src[i], dst[i], conv_type)
        else:
            dst[i] = conv_type(src[i]) if conv_type else src[i]


def calc_sequence_shape(seq, array_check=False):
    # シーケンスである seq の shape (numpy 形式) を返す.
    # seq は numpy でいう n 次元配列でなければならない. (array_check が True であればそのチェックを行う)

    if not is_sequence(seq):
        raise RuntimeError("{0} is not sequence".format(seq))

    elem = seq[0]
    if is_sequence(elem):
        if array_check:
            size = len(elem)
            for e in seq:
                if size != len(e):
                    raise RuntimeError("")

        shape = len(seq), *calc_sequence_shape(elem)
        return shape
    else:
        if array_check:
            for e in seq:
                if is_sequence(e):
                    raise RuntimeError("")

        return (len(seq), )
