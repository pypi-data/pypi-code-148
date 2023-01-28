# (C) 2023 A. Voß setup@codebasedlearning.dev, a.voss@fh-aachen.de

import unittest

import cbl
from cbl.setup import about_package, about_platform, about_python

class SnippetInfoTestCase(unittest.TestCase):
    def test_info(self):
        print("huhu test setup")
        info1 = cbl.setup.about_package()
        print(info1)
        info2 = cbl.setup.about_platform()
        print(info2)
        info3 = about_platform()
        print(info3)
        info4 = about_python()
        print(info4)

    pi = cbl.setup.PackageInfo(1,2,3)


if __name__ == '__main__':
    unittest.main()
