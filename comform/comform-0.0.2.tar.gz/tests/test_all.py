from comform.fixers import run_all

TEST_KEY = "all"


def test_all() -> None:
    with open(Rf".\tests\examples\{TEST_KEY}_good.py") as fh:
        correct_text = fh.read()
    result = run_all(Rf".\tests\examples\{TEST_KEY}_bad.py")

    # with open("temp.py", "w") as fh:
    #     fh.write(result)
    assert correct_text == result
