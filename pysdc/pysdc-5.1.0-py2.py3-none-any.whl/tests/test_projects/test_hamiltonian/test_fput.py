import pytest


@pytest.mark.base
def test_main():
    from pySDC.projects.Hamiltonian.fput import main

    main()
