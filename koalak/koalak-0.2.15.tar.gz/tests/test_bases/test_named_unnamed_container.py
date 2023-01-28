from koalak import NamedAndUnnamedContainer


def test_named_unnamed_container_basics():
    class A:
        pass

    class B:
        pass

    class C:
        pass

    class D:
        pass

    l = NamedAndUnnamedContainer()

    assert len(l) == 0
    assert bool(l) is False
    assert list(l) == []
    assert not A in l

    l.add(A)
    assert len(l) == 1
    assert bool(l) is True
    assert list(l) == [A]
    assert A in l

    # Same element is okay
    l.add(A)
    assert len(l) == 2
    assert bool(l) is True
    assert list(l) == [A, A]
    assert A in l

    # Other element is okay
    l.add(B)
    assert len(l) == 3
    assert bool(l) is True
    assert list(l) == [A, A, B]
    assert B in l

    # Other element is okay
    l.add(C, name="a")
    assert len(l) == 4
    assert bool(l) is True
    assert list(l) == [A, A, B, C]
    assert C in l
    assert l["a"] is C

    # Order is kept after adding unnamed element
    l.add(D)
    assert len(l) == 5
    assert bool(l) is True
    assert list(l) == [A, A, B, C, D]
    assert D in l
