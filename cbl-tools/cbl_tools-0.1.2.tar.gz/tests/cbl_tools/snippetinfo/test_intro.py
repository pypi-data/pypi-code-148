# info@codebasedlearning.dev, a.voss@fh-aachen.de

import unittest

from cbl_tools.snippetinfo import intro, with_intro, note


class SnippetInfoTestCase(unittest.TestCase):
    def test_console_output(self):
        with intro:                         # => '_jb_unittest_runner' outer shell
            note.info("first info")         # => 'SnippetInfoTestCase.test_console_output' info

            @with_intro                     # => 'f' inner shell
            def f():
                note.detail("inside f")     # => 'f' detail
            f()

            note.info("end of test")        # => 'SnippetInfoTestCase.test_console_output' info


if __name__ == '__main__':
    unittest.main()
