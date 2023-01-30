import os

try:
    from importlib.resources import path as get_path, read_text

    _CACERT_CTX = None
    _CACERT_PATH = None


    def where():
        # 使用全局的配置
        global _CACERT_CTX
        global _CACERT_PATH

        # 如果cert文件路径不存在
        if _CACERT_PATH is None:
            f = os.path.dirname(__file__)
            return os.path.join(f, "cacert.pem")

        return _CACERT_PATH


except ImportError:
    # 如果没有导入模块成功
    def read_text(_module, _path, encoding="ascii"):
        with open(where(), "r", encoding=encoding) as data:
            return data.read()


    def where():
        f = os.path.dirname(__file__)
        return os.path.join(f, "cacert.pem")


def contents():
    """
    读取文件内容
    """
    return read_text("certifi", "cacert.pem", encoding="ascii")
