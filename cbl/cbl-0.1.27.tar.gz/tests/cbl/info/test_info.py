# info@codebasedlearning.dev, a.voss@fh-aachen.de

import unittest

from cbl_tools.snippetinfo import intro, with_intro, note
import cbl_tools
from cbl_tools.info import package_info, platform_info

class SnippetInfoTestCase(unittest.TestCase):
    def test_info(self):
        print("huhu test info")
        info1 = cbl_tools.info.package_info()
        print(info1)
        info2 = cbl_tools.info.platform_info()
        print(info2)
        info3 = platform_info()
        print(info3)
        pi = cbl_tools.info.PackageInfo(1,2)


if __name__ == '__main__':
    unittest.main()
