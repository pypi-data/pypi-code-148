from koalak import koalak_object_storage


def test_basic_object_storage():
    class A:
        pass

    assert koalak_object_storage.get(A, "X") is None
    assert koalak_object_storage.get(A, "X", {}) == {}  # test default
    koalak_object_storage.set(A, "X", True)
    assert koalak_object_storage.get(A, "X") is True
    assert koalak_object_storage.get(A, "X", {}) is True  # test default


def test_cls_object_storage():
    class A:
        pass

    class B(A):
        pass

    assert koalak_object_storage.get(A, "Y") is None
    assert koalak_object_storage.getfromobject(A, "Y") is None
    assert koalak_object_storage.get(B, "Y") is None
    assert koalak_object_storage.getfromobject(B, "Y") is None

    # put Y only in cls A and not in cls B
    koalak_object_storage.set(A, "Y", 2)
    assert koalak_object_storage.get(A, "Y") == 2
    assert koalak_object_storage.getfromobject(A, "Y") == 2
    assert koalak_object_storage.get(B, "Y") == 2
    assert koalak_object_storage.getfromobject(B, "Y") is None


def test_object_storage_with_inheritance():
    class A:
        pass

    class B(A):
        pass

    koalak_object_storage.set(A, "x", 1)
    assert koalak_object_storage.get(A, "x") == 1
    assert koalak_object_storage.get(B, "x") == 1
    assert koalak_object_storage.getfromobject(A, "x") == 1
    assert koalak_object_storage.getfromobject(B, "x") is None

    koalak_object_storage.set(B, "y", 2)
    assert koalak_object_storage.get(A, "x") == 1
    assert koalak_object_storage.get(B, "x") == 1
    assert koalak_object_storage.getfromobject(A, "x") == 1
    assert koalak_object_storage.getfromobject(B, "x") is None

    assert koalak_object_storage.get(A, "y") is None  # attribute was set on B not A
    assert koalak_object_storage.get(B, "y") == 2
    assert koalak_object_storage.getfromobject(A, "y") is None
    assert koalak_object_storage.getfromobject(B, "y") == 2


def test_object_storage_with_instances():
    class A:
        pass

    b = A()

    koalak_object_storage.set(A, "x", 1)
    assert koalak_object_storage.get(A, "x") == 1
    assert koalak_object_storage.get(b, "x") == 1
    assert koalak_object_storage.getfromobject(A, "x") == 1
    assert koalak_object_storage.getfromobject(b, "x") is None

    koalak_object_storage.set(b, "y", 2)
    assert koalak_object_storage.get(A, "x") == 1
    assert koalak_object_storage.get(b, "x") == 1
    assert koalak_object_storage.getfromobject(A, "x") == 1
    assert koalak_object_storage.getfromobject(b, "x") is None

    assert koalak_object_storage.get(A, "y") is None  # attribute was set on B not A
    assert koalak_object_storage.get(b, "y") == 2
    assert koalak_object_storage.getfromobject(A, "y") is None
    assert koalak_object_storage.getfromobject(b, "y") == 2


def test_object_storage_default_value_with_none():
    class A:
        pass

    koalak_object_storage.set(A, "x", None)
    assert koalak_object_storage.get(A, "x") is None
    assert koalak_object_storage.get(A, "x", 1) is None

    assert koalak_object_storage.getfromobject(A, "x") is None
    assert koalak_object_storage.getfromobject(A, "x", 1) is None


def test_object_storage_nested_key():
    class A:
        pass

    class B(A):
        pass

    dictname = "alpha"
    koalak_object_storage.setindict(A, dictname, "x", 1)
    assert koalak_object_storage.get(A, dictname) == {"x": 1}
    assert koalak_object_storage.get(B, dictname) == {"x": 1}

    koalak_object_storage.setindict(A, dictname, "y", 2)
    assert koalak_object_storage.get(A, dictname) == {"x": 1, "y": 2}
    assert koalak_object_storage.get(B, dictname) == {"x": 1, "y": 2}

    # adding z in B
    koalak_object_storage.setindict(B, dictname, "z", 3)
    assert koalak_object_storage.get(A, dictname) == {"x": 1, "y": 2}
    assert koalak_object_storage.get(B, dictname) == {"z": 3}
    assert koalak_object_storage.getasdict(B, dictname) == {"x": 1, "y": 2, "z": 3}

    # overwrite y in B
    koalak_object_storage.setindict(B, dictname, "y", "newvalue")
    assert koalak_object_storage.get(A, dictname) == {"x": 1, "y": 2}
    assert koalak_object_storage.get(B, dictname) == {"z": 3, "y": "newvalue"}
    assert koalak_object_storage.getasdict(B, dictname) == {
        "x": 1,
        "y": "newvalue",
        "z": 3,
    }
