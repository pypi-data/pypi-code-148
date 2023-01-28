#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/5 17:41
# @Author  : zbc@mail.ustc.edu.cn
# @File    : config_base.py
# @Software: PyCharm

import os
import logging


class ConfigBase:

    def __init__(self, config_json):
        self._root = config_json.get('root')
        self._config_json = config_json

    def get_fp_by_key(self, key: str, check_exist: bool) -> str:
        fn = self._config_json.get(key)
        if fn is None:
            raise ValueError(f"在 config 中找不到 key: {key}")
        fp = os.path.join(self._root, fn)
        if check_exist and not os.path.exists(fp):
            raise ValueError(f"文件不存在: {fp}")
        return fp

    def get_dp_by_key(self, key: str, check_exist: bool, create_dp: bool) -> str:
        dn = self._config_json.get(key)
        if dn is None:
            raise ValueError(f"在 config 中找不到 key: {key}")
        dp = os.path.join(self._root, dn)
        if check_exist and not os.path.exists(dp):
            raise ValueError(f"文件夹不存在: {dp}")
        if create_dp and not os.path.exists(dp):
            logging.info(f"creating dir: {dp}")
            os.mkdir(dp)
        return dp


if __name__ == "__main__":
    pass
