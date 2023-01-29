#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jandd.sphinxext.ip unit test driver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script runs the jandd.sphinxext.ip unit test suite.

:copyright: Copyright 2016 Jan Dittberner
:license: GPLv3+, see COPYING for details.
"""

import sys
import unittest
from os import path


def run(extra_args=[]):
    sys.path.insert(0, path.join(path.dirname(__file__), path.pardir))
    sys.path.insert(
        1,
        path.abspath(
            path.join(path.dirname(__file__), path.pardir, "jandd", "sphinxext", "ip")
        ),
    )

    try:
        import sphinx
    except ImportError:
        print(
            "The sphinx package is needed to run the jandd.sphinxext.ip " "test suite."
        )

    from tests.test_ip import TestIPExtension

    print("Running jandd.sphinxext.ip test suite ...")

    suite = unittest.TestLoader().loadTestsFromTestCase(TestIPExtension)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    run()
