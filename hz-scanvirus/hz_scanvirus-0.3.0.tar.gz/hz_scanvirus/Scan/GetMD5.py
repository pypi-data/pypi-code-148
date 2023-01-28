"""
Function Help Scan/GetMD5.py

--[Mod]--
    --[Main]-- => Main Function
--[File]-- None.
--[Run]--
    main(filename)
    [filename] => File Path.
    Return: File MD5.
"""


import hashlib


def main(filename):  # 获取MD5
    """
    :param filename: File Path.
    :return: File MD5.
    """
    file_object = open(filename, 'rb')
    file_name = filename
    file_content = file_object.read()
    file_object.close()
    file_md5 = hashlib.md5(file_content)
    file_object.close()
    return file_md5.hexdigest()
