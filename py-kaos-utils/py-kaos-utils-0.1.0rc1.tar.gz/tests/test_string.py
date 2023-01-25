from py_kaos_utils.string import create_initials


def test_create_initials():
    s = "Aaaa bbb"
    assert create_initials(s) == "AB"

    s = ""
    assert create_initials(s) == ""

    s = "AB c DB fG"
    assert create_initials(s) == "ACDF"
