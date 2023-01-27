# info@codebasedlearning.dev, a.voss@fh-aachen.de

import unittest

from cbl_tools.snippetinfo import intro, with_intro, note
import cbl_tools
#from cbl_tools.info import package_info

class SnippetInfoTestCase(unittest.TestCase):
    def test_info(self):
        print("huhu test info")
        info = cbl_tools.info.package_info()


if __name__ == '__main__':
    unittest.main()
