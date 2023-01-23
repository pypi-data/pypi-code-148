#!/usr/bin/env python

"""Tests for `lyceum.logic` package."""
from sympy import symbols

from lyceum.logic import (
    logic2str,
    str2logic,
    table_de_verite
)

P, Q, R, S, T = symbols('P Q R S T')

def test_logic2str():
    assert logic2str(P|Q) == "P | Q"
    assert logic2str(P|    Q) == "P | Q"
    assert logic2str(     P     |    Q     ) == "P | Q"
    assert logic2str(~P&~Q) == "!P & !Q"


def test_str2logic():
    assert str2logic("P&Q|!P") == P&Q|~P


def test_table_de_verite():
    print(table_de_verite("!P"))
    assert table_de_verite("!P") == """+-----+------+
|  P  |  !P  |
+=====+======+
|  0  |  1   |
+-----+------+
|  1  |  0   |
+-----+------+"""
    print(table_de_verite("P&Q"))
    assert table_de_verite("P&Q") == """+-----+-----+---------+
|  P  |  Q  |  P & Q  |
+=====+=====+=========+
|  0  |  0  |    0    |
+-----+-----+---------+
|  0  |  1  |    0    |
+-----+-----+---------+
|  1  |  0  |    0    |
+-----+-----+---------+
|  1  |  1  |    1    |
+-----+-----+---------+"""
    