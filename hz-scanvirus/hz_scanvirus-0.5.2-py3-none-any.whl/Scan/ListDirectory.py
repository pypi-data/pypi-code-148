"""
Function Help Scan/ListDirectory.py

--[Mod]--
    --[Main]-- => Main Function
--[File]-- None.
--[Run]--
    main(rootdir)
    [filename] => Root directory path.
    Return: File MD5.
"""
import os


def main(rootdir):
    """
    :param rootdir: Root directory path.
    :return: File MD5.
    """
    global nemberfiles
    _files = []

    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        nemberfiles += 1

        path = os.path.join(rootdir, list[i])

        if os.path.isdir(path):
            _files.extend(main(path))
        if os.path.isfile(path):
            _files.append(path)

    return _files
