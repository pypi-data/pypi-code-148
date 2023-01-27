class TestInlineTeal(unittest.TestCase):
    def test_pass_simple(self):
        teal = compile_min(
            [
                "teal:",
                "pushint 1",
                "pushint 2",
                "+",
                "end",
            ]
        )
        self.assertListEqual(
            teal,
            [
                "pushint 1",
                "pushint 2",
                "+",
            ],
        )
