# info@codebasedlearning.dev, a.voss@fh-aachen.de

import unittest

from cbl_tools.snippetinfo import intro, with_intro, note
import cbl_tools
from cbl_tools.info import *

class SnippetInfoTestCase(unittest.TestCase):
    def test_info(self):
        print("huhu test info")
        info1 = cbl_tools.info.package_info2()
        info2 = cbl_tools.info.platform_info()


if __name__ == '__main__':
    unittest.main()
