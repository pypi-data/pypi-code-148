#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 fx-kirin <fx.kirin@gmail.com>
#
# Distributed under terms of the MIT license.

import os
import fire
import logging
import kanilog
from pathlib import Path


def main():
    pass


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    kanilog.setup_logger(
        logfile="/tmp/%s.log" % (Path(__file__).name), level=logging.INFO
    )
    fire.Fire(main)
