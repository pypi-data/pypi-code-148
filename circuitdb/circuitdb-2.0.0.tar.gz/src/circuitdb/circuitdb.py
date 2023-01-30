"""
Data set of optimal circuits for Boolean functions that have low arity.
"""
from __future__ import annotations
from typing import Tuple, Union, Optional, AbstractSet
import doctest
import importlib.resources
import sys
import os
import math
import base64
import bitlist
import logical
import circuit

class record(bytes):
    """
    Wrapper class for an individual record (*i.e.*, encoded data corresponding to a
    circuit).
    """
    @staticmethod
    def from_circuit(
            circuit: circuit.circuit # pylint: disable=redefined-outer-name
        ) -> record:
        """
        Encode a :obj:`~circuit.circuit.circuit` object and construct a record that
        represents it.

        >>> c = circuit.circuit()
        >>> g0 = c.gate(logical.id_, is_input=True)
        >>> g1 = c.gate(logical.id_, is_input=True)
        >>> g2 = c.gate(logical.id_, is_input=True)
        >>> g3 = c.gate(logical.xor_, [g0, g2])
        >>> g4 = c.gate(logical.nimp_, [g1, g3])
        >>> g5 = c.gate(logical.id_, [g4], is_output=True)
        >>> record.from_circuit(c).to_base64()
        'CQACBAEDBgQ='
        """
        # Create table for converting an encoded operator into an actual operator value.
        integer_to_operator = list(sorted(list(logical.every)))

        # Convert gate data into a list of integers. Note that the number of gates
        # (including input and output gates) must not exceed 256.
        bs = []
        for g in circuit.gates:
            if not g.is_input:
                bs.extend(
                    [integer_to_operator.index(g.operation)] +
                    [circuit.gates.index(gi) for gi in g.inputs]
                )

        return record(bytes(bs))

    @staticmethod
    def from_base64(string: str) -> record:
        """
        Construct an instance from a Base64-encoded string representation of a record.

        >>> record.from_base64('CQACBAEDBgQ=').hex()
        '0900020401030604'
        """
        return record(base64.standard_b64decode(string))

    def to_circuit(
            self: record,
            truthtable: Union[Tuple[int, ...], Tuple[Tuple[int, ...], ...]]
        ) -> circuit.circuit:
        """
        Decode this record into a :obj:`~circuit.circuit.circuit` object.

        >>> c = record.from_base64('CQACBAEDBgQ=').to_circuit((0, 0, 1, 0, 0, 0, 0, 1))
        >>> c.gates.to_legible()
        (('id',), ('id',), ('id',), ('xor', 0, 2), ('nimp', 1, 3), ('id', 4))
        """
        # Create table for converting an encoded operator into an actual operator value.
        integer_to_operator = list(sorted(list(logical.every)))

        # Parse the gate information from the encoded representation.
        (j, ts) = (0, [])
        while j < len(self):
            operator = integer_to_operator[self[j]]
            ts.append((operator, self[j + 1: j + 1 + operator.arity()]))
            j += 1 + operator.arity()

        # Build the circuit object programmatically.
        arity = int(math.log2(len(truthtable)))
        coarity = len(truthtable[0]) if isinstance(truthtable[0], tuple) else 1
        c = circuit.circuit()
        gs = []
        for _ in range(arity): # Input gates.
            gs.append(c.gate(logical.id_, [], is_input=True))
        for entry in ts[0:-coarity]: # Internal gates.
            gs.append(c.gate(entry[0], [gs[k] for k in entry[1]]))
        for entry in ts[-coarity:]: # Output gates.
            c.gate(entry[0], [gs[k] for k in entry[1]], is_output=True)

        return c

    def to_base64(self: record) -> str:
        """
        Convert this instance into a Base64-encoded string representation.

        >>> c = circuit.circuit()
        >>> g0 = c.gate(logical.id_, is_input=True)
        >>> g1 = c.gate(logical.not_, [g0])
        >>> g2 = c.gate(logical.id_, [g1], is_output=True)
        >>> record.from_circuit(c).to_base64()
        'DAAGAQ=='
        """
        return base64.standard_b64encode(self).decode('utf-8')

class records(list):
    """
    Wrapper class for a base-level operation-to-circuit map (corresponding to a fixed
    combination of arity, coarity, operator set, and operator set to minimize).
    """
    @staticmethod
    def from_file(resource: str) -> records:
        """
        Construct an instance from a binary file of circuit data (where the specified
        resource is either a package resource of this package or a file path).

        >>> len(records.from_file('3_1_every_every'))
        256
        """
        if os.path.exists(resource):
            with open(resource, 'rb') as file:
                data = file.read()
        else:
            # Support Python version 3.7 and above.
            if sys.version_info.minor >= 9: # pragma: no cover
                # Available in Python version 3.9 and above.
                with { # pylint: disable=no-member
                    r.name: r
                    for r in importlib.resources.files('circuitdb').iterdir()
                }[resource].open('rb') as file:
                    data = file.read()
            else: # pragma: no cover
                # Not deprecated in Python version 3.10 and below.
                data = importlib.resources.read_binary('circuitdb', resource)

        return records([
            bytes([b - 1 for b in bs])
            for bs in data.split(bytes([0]))
        ])

    def to_file(self: records, path: str):
        """
        Write the data in this instance to a binary file.

        >>> rs = records.from_file('3_1_every_every')
        >>> rs.to_file('test-output-records.to_file')
        >>> len(records.from_file('test-output-records.to_file'))
        256
        >>> os.remove('test-output-records.to_file')
        """
        bs = []
        for (j, r) in enumerate(self):
            bs.extend(
                [b + 1 for b in record(r)] +
                ([] if j == len(self) - 1 else [0])
            )
        with open(path, 'wb') as file:
            file.write(bytes(bs))

    def __getitem__(
            self: records,
            truthtable: Union[Tuple[int, ...], Tuple[Tuple[int, ...], ...]]
        ) -> record:
        """
        Data retrieval wrapper that performs normalization of the truth table,
        but does not check that it has a correct structure. To ensure the supplied
        truth table representation is valid, the :obj:`circuitdb.__call__` should
        be used to retrieve circuit data.
        """
        # Normalize the truth table representation (no validation) and
        # convert it into an index into the data.
        if all(isinstance(e, tuple) for e in truthtable):
            truthtable = tuple(tuple(map(int, e)) for e in truthtable)
            ls = set(len(e) for e in truthtable)
            if len(ls) == 1 and list(ls)[0] == 1:
                truthtable = list(e[0] for e in truthtable)
                index = int(bitlist.bitlist(truthtable))
            else:
                index = int(bitlist.bitlist([b for t in truthtable for b in t]))
        else:
            truthtable = list(map(int, truthtable))
            index = int(bitlist.bitlist(truthtable))

        # Retrieve, decode, and return the circuit data.
        return record(super().__getitem__(index)).to_circuit(truthtable)

_db: dict = {}
"""
Private dictionary object that represents the data set.
"""

# Set up containers for each (arity, coarity, operator set) combination
# for which data is included.
for i in range(0, 4):
    _db[i] = {}

    if i == 0:
        _db[i][1] = {
            logical.every: {}
        }

    if i in range(1, 4):
        _db[i][1] = {
            frozenset({logical.id_, logical.not_, logical.and_, logical.or_}): {},
            frozenset({logical.id_, logical.not_, logical.and_, logical.xor_}): {},
            logical.every: {}
        }

    if i == 2:
        _db[i][2] = {
            frozenset({logical.id_, logical.not_, logical.and_, logical.or_}): {},
            frozenset({logical.id_, logical.not_, logical.and_, logical.xor_}): {},
            logical.every: {}
        }

_db \
    [1][1] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.or_})] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.or_})] \
    = records(map(base64.standard_b64decode, [
        'DAADAAEGAg==',
        'BgA=',
        'DAAGAQ==',
        'DAAKAAEGAg==',
    ]))

_db \
    [2][1] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.or_})] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.or_})] \
    = records(map(base64.standard_b64decode, [
        'DAADAAIGAw==',
        'AwABBgI=',
        'DAEDAAIGAw==',
        'BgA=',
        'DAADAQIGAw==',
        'BgE=',
        'AwABDAIKAAEDAwQGBQ==',
        'CgABBgI=',
        'CgABDAIGAw==',
        'AwABCgABDAMKAgQGBQ==',
        'DAEGAg==',
        'DAEKAAIGAw==',
        'DAAGAg==',
        'DAAKAQIGAw==',
        'AwABDAIGAw==',
        'DAAKAAIGAw==',
    ]))

_db \
    [2][2] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.or_})] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.or_})] \
    = records.from_file('2_2_id-not-and-or_id-not-and-or')

_db \
    [3][1] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.or_})] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.or_})] \
    = records.from_file('3_1_id-not-and-or_id-not-and-or')

_db \
    [1][1] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.xor_})] \
    [frozenset({logical.and_})] \
    = records(map(base64.standard_b64decode, [
        'DAAMAAkBAgYD',
        'BgA=',
        'DAAGAQ==',
        'DAAJAAEGAg==',
    ]))

_db \
    [2][1] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.xor_})] \
    [frozenset({logical.and_})] \
    = records(map(base64.standard_b64decode, [
        'DAAMAAkCAwYE',
        'AwABBgI=',
        'DAEDAAIGAw==',
        'BgA=',
        'DAADAQIGAw==',
        'BgE=',
        'CQABBgI=',
        'DAADAQIJAAMGBA==',
        'DAAMAQMCAwYE',
        'DAAJAQIGAw==',
        'DAEGAg==',
        'DAADAQIMAwYE',
        'DAAGAg==',
        'DAADAAEJAgMGBA==',
        'AwABDAIGAw==',
        'DAAJAAIGAw==',
    ]))

_db \
    [2][2] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.xor_})] \
    [frozenset({logical.and_})] \
    = records.from_file('2_2_id-not-and-xor_and')

_db \
    [3][1] \
    [frozenset({logical.id_, logical.not_, logical.and_, logical.xor_})] \
    [frozenset({logical.and_})] \
    = records.from_file('3_1_id-not-and-xor_and')

_db \
    [0][1] \
    [logical.every] \
    [logical.every] \
    = records(map(base64.standard_b64decode, [
        'AAYA',
        'CwYA',
    ]))

_db \
    [1][1] \
    [logical.every] \
    [logical.every] \
    = records(map(base64.standard_b64decode, [
        'AQAGAQ==',
        'BgA=',
        'DAAGAQ==',
        'EQAGAQ==',
    ]))

_db \
    [2][1] \
    [logical.every] \
    [logical.every] \
    = records(map(base64.standard_b64decode, [
        'AgABBgI=',
        'AwABBgI=',
        'BAABBgI=',
        'BQABBgI=',
        'BwABBgI=',
        'CAABBgI=',
        'CQABBgI=',
        'CgABBgI=',
        'DQABBgI=',
        'DgABBgI=',
        'DwABBgI=',
        'EAABBgI=',
        'EgABBgI=',
        'EwABBgI=',
        'FAABBgI=',
        'FQABBgI=',
    ]))

_db \
    [2][2] \
    [logical.every] \
    [logical.every] \
    = records.from_file('2_2_every_every')

_db \
    [3][1] \
    [logical.every] \
    [logical.every] \
    = records.from_file('3_1_every_every')

class circuitdb(dict):
    """
    Wrapper class for a circuit data set that contains an (arbitrary but fixed)
    example of the smallest possible logical circuit (in terms of the number of
    unary and/or binary gates) for each possible logical function (from a finite
    set of functions). This class supports both a dictionary-like interface
    (inherited from the :obj:`dict` type) and a function-like interface (via the
    :obj:`__call__` method).

    **Logical Function Representation:** Logical functions are represented using
    tuples in an identical manner to that of the :obj:`~logical.logical.logical`
    class defined in the `logical <https://pypi.org/project/logical>`__ library. For
    example, the logical function *f* (*x*, *y*, *z*) = *x* **and** *y* **and** *z*
    (*i.e.*, three-argument conjunction) is represented using a tuple representation
    of the output column of the truth table for the function (assuming that the
    possible inputs are in ascending dictionary order): ``(0, 0, 0, 0, 0, 0, 0, 1)``.

    >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 1)).gates.to_legible()
    (('id',), ('id',), ('id',), ('and', 0, 1), ('and', 2, 3), ('id', 4))

    For logical functions having multiple outputs, the entries in the tuple may
    themselves be tuples. For example, *f* (*x*, *y*) = (*y*, *x*) is represented
    using the tuple ``((0, 0), (1, 0), (0, 1), (1, 1))``.

    >>> circuitdb(((0, 0), (1, 0), (0, 1), (1, 1))).gates.to_legible()
    (('id',), ('id',), ('id', 1), ('id', 0))

    **Circuit Representation:** Retrieved circuits are instances of the
    :obj:`~circuit.circuit.circuit` class that is defined in the
    `circuit <https://pypi.org/project/circuit>`__ library. In order to make this
    documentation human-readible, the examples include an invocation of the
    :obj:`~circuit.circuit.gates.to_legible` method belonging to the gate list
    associated with the returned :obj:`~circuit.circuit.circuit` object. This
    representation of a circuit consists of a list of unary and binary gates. Each
    gate is represented as a tuple. The first entry in each gate tuple is the name
    of the logical function corresponding to that gate (as defined in the
    :obj:`~logical.logical.logical.names` class attribute in the
    `logical <https://pypi.org/project/logical>`__ library). The remaining
    entries in the gate tuple are the indices of the input gates to that gate.

    >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 1)).gates.to_legible()
    (('id',), ('id',), ('id',), ('and', 0, 1), ('and', 2, 3), ('id', 4))

    In the circuit above, the entry ``('and', 2, 3)`` represents a gate that
    is a conjunction of the gates at positions ``2`` and ``3`` in the overall list
    (*i.e.* , ``('id',)`` and ``('and', 0, 1)``).

    **Set of Permitted Gates:** For any given logical function, it is possible to
    construct a corresponding circuit using a variety of gate sets. For each logical
    function, the database contains an example of a smallest circuit for each of a
    small collection of sets of unary and binary gates. The set of gates that can be
    used to construct a circuit can be supplied using the ``operators`` parameter.
    In the remaining examples below, circuits are retrieved for the specific function
    ``(0, 0, 1, 0, 0, 0, 0, 1)``. The unary and binary logical operators represented
    by the gates in the circuit below are drawn from the set of permitted gates
    ``{logical.id_, logical.not_, logical.and_, logical.or_}``.

    >>> from logical import logical
    >>> for g in circuitdb(
    ...     (0, 0, 1, 0, 0, 0, 0, 1),
    ...     frozenset({logical.id_, logical.not_, logical.and_, logical.or_})
    ... ).gates.to_legible():
    ...     print(g)
    ('id',)
    ('id',)
    ('id',)
    ('and', 0, 2)
    ('or', 0, 2)
    ('not', 4)
    ('or', 3, 5)
    ('and', 1, 6)
    ('id', 7)

    All gates in the circuit below are found in the set
    ``{logical.id_, logical.not_, logical.and_, logical.xor_}``.

    >>> for g in circuitdb(
    ...     (0, 0, 1, 0, 0, 0, 0, 1),
    ...     frozenset({logical.id_, logical.not_, logical.and_, logical.xor_})
    ... ).gates.to_legible():
    ...     print(g)
    ('id',)
    ('id',)
    ('id',)
    ('not', 0)
    ('xor', 2, 3)
    ('and', 1, 4)
    ('id', 5)

    By default (or if the set of *all* gates is supplied using the constant
    :obj:`~logical.logical.logical.every` that is defined in the
    `logical <https://pypi.org/project/logical>`__), a smallest circuit that can
    be built using *any* combination of unary or binary gates is returned.

    >>> circuitdb((0, 0, 1, 0, 0, 0, 0, 1)).gates.to_legible()
    (('id',), ('id',), ('id',), ('xor', 0, 2), ('nimp', 1, 3), ('id', 4))
    >>> circuitdb((0, 0, 1, 0, 0, 0, 0, 1), logical.every).gates.to_legible()
    (('id',), ('id',), ('id',), ('xor', 0, 2), ('nimp', 1, 3), ('id', 4))

    **Set of Gates to Minimize:** Multiple possible circuits that use gates from
    a given gate set can be used to implement a logical function. Some of these
    circuits may have more of one type of gate than other circuits. Thus, there
    is an option to specify using the ``minimize`` parameter *which* gates *do*
    contribute to the *size* of the circuit (*i.e.*, the metric that is being
    minimized). All other gates are *not counted* for the purposes of comparing
    circuits according to their size.

    >>> for g in circuitdb(
    ...     (0, 0, 1, 0, 0, 0, 0, 1),
    ...     frozenset({logical.id_, logical.not_, logical.and_, logical.xor_}), {logical.and_}
    ... ).gates.to_legible():
    ...     print(g)
    ('id',)
    ('id',)
    ('id',)
    ('not', 0)
    ('xor', 2, 3)
    ('and', 1, 4)
    ('id', 5)

    **Supported Combinations:** Each logical function has a number of input values,
    a number of output values, a set of permitted gates/**operators**, and a set of
    gates to **minimize** in quantity. Entries exist in the database for only a finite
    set of logical functions. The table below lists the supported combinations of
    function input count, function output count, and gate set that are found in the
    database. **All** functions for a given combination of inputs and outputs are
    supported (*e.g.*, all ``2**(2**3) = 256`` functions having three inputs and one
    output are supported). Gate sets are defined using operator constants found in
    the `logical <https://pypi.org/project/logical>`__ library).

    +------------+-------------+-----------------------------+----------------------------+
    | **inputs** | **outputs** | **operators**               | **minimize**               |
    +------------+-------------+-----------------------------+----------------------------+
    | 1          | 1           | ``{id_, not_, and_, or_}``  | ``{id_, not_, and_, or_}`` |
    +------------+-------------+-----------------------------+----------------------------+
    | 1          | 1           | ``{id_, not_, and_, xor_}`` | ``{and_}``                 |
    +------------+-------------+-----------------------------+----------------------------+
    | 1          | 1           | ``every``                   | ``every``                  |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 1           | ``{id_, not_, and_, or_}``  | ``{id_, not_, and_, or_}`` |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 1           | ``{id_, not_, and_, xor_}`` | ``{and_}``                 |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 1           | ``every``                   | ``every``                  |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 2           | ``{id_, not_, and_, or_}``  | ``{id_, not_, and_, or_}`` |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 2           | ``{id_, not_, and_, xor_}`` | ``{and_}``                 |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 2           | ``every``                   | ``every``                  |
    +------------+-------------+-----------------------------+----------------------------+
    | 3          | 1           | ``{id_, not_, and_, or_}``  | ``{id_, not_, and_, or_}`` |
    +------------+-------------+-----------------------------+----------------------------+
    | 3          | 1           | ``{id_, not_, and_, xor_}`` | ``{and_}``                 |
    +------------+-------------+-----------------------------+----------------------------+
    | 3          | 1           | ``every``                   | ``every``                  |
    +------------+-------------+-----------------------------+----------------------------+

    The database supports retrieval using index notation, as well.

    >>> ops = logical.every
    >>> circuitdb[1][1][ops][ops][(0, 0)].gates.to_legible()
    (('id',), ('uf', 0), ('id', 1))
    >>> circuitdb[1][1][ops][ops][((0,), (0,))].gates.to_legible()
    (('id',), ('uf', 0), ('id', 1))

    The top-level database instance has keys that represent to the number of
    inputs of the logical function. The second level down, the keys represent
    the number of outputs of a logical function. The third level down, keys
    represent the set of unary or binary gates to which circuits are restricted.
    Finally, the last level down, the keys represent logical functions.

    >>> list(sorted(list(circuitdb.keys()))) == [0, 1, 2, 3]
    True
    >>> ks = list(sorted(list(circuitdb[1][1].keys())))
    >>> ks[0] == frozenset({logical.and_, logical.or_, logical.not_, logical.id_})
    True
    >>> circuitdb[2][1][ks[0]][ks[0]][(1,1,1,1)].gates.to_legible()
    (('id',), ('id',), ('not', 0), ('or', 0, 2), ('id', 3))

    Note that the internal representation organizes the circuits by arity.

    >>> _d = {i: _db[i][1] for i in range(1,4)}
    >>> all(len(_d[1][o][m]) == 4 for o in _d[1] for m in _d[1][o])
    True
    >>> all(len(_d[2][o][m]) == 16 for o in _d[2] for m in _d[2][o])
    True
    >>> all(len(_d[3][o][m]) == 256 for o in _d[3] for m in _d[3][o])
    True
    """
    def __call__(
        self: circuitdb,
        truthtable: Union[Tuple[int, ...], Tuple[Tuple[int, ...], ...]],
        operators: Optional[AbstractSet[logical.logical]] = None,
        minimize: Optional[AbstractSet[logical.logical]] = None
    ) -> circuit.circuit:
        """
        Function-like interface for the circuit database, with user-friendly
        defaults for retrieving circuit data.

        By supplying a logical function (represented as a tuple), it is possible
        to retrieve a smallest circuit that implements that function. Logical
        functions having one output are represented using a tuple of
        integers (or booleans), or a tuple of one-element tuples.

        >>> circuitdb((0, 0)).gates.to_legible()
        (('id',), ('uf', 0), ('id', 1))
        >>> circuitdb(((0,), (0,))).gates.to_legible()
        (('id',), ('uf', 0), ('id', 1))
        >>> circuitdb((False, False)).gates.to_legible()
        (('id',), ('uf', 0), ('id', 1))

        A logical function having a vector of two outputs is represented using
        a tuple of two-element tuples.

        >>> circuitdb(((1, 0), (1, 0), (1, 0), (0, 1))).gates.to_legible()
        (('id',), ('id',), ('and', 0, 1), ('not', 2), ('id', 3), ('id', 2))

        It is also possible to retrieve a smallest circuit that only uses gates
        from a specific set of gates.

        >>> circuitdb(
        ...     (0, 0, 0, 0, 0, 0, 0, 0),
        ...     {logical.id_, logical.not_, logical.and_, logical.or_}
        ... ).gates.to_legible()
        (('id',), ('id',), ('id',), ('not', 0), ('and', 0, 3), ('id', 4))

        Any attempt to access the data with a malformed key raises an
        exception.

        >>> circuitdb([0, 0, 0, 0])
        Traceback (most recent call last):
          ...
        TypeError: truth table must be a tuple
        >>> circuitdb((0, 0, 0))
        Traceback (most recent call last):
          ...
        ValueError: truth table must have a length that is a power of two
        >>> circuitdb(('abc', 'xyz'))
        Traceback (most recent call last):
          ...
        TypeError: truth table must contain boolean values, integers in the range ... of such
        >>> circuitdb((('abc', 'xyz')))
        Traceback (most recent call last):
          ...
        TypeError: truth table must contain boolean values, integers in the range ... of such
        >>> circuitdb(((1, 'abc'), (1, 0), (1, 0), (0, 1)))
        Traceback (most recent call last):
          ...
        TypeError: truth table must contain boolean values, integers in the range ... of such
        >>> circuitdb(((), ()))
        Traceback (most recent call last):
          ...
        ValueError: truth table entries must each represent at least one value
        >>> circuitdb(((), (1, 0)))
        Traceback (most recent call last):
          ...
        ValueError: truth table entries must all have the same length
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 4
        >>> circuitdb(((0,0,0), (1,1,1)))
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 1 having output vectors of length 1
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), 132)
        Traceback (most recent call last):
          ...
        TypeError: collection of operators must be a set or frozenset
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), 132)
        Traceback (most recent call last):
          ...
        TypeError: collection of operators must be a set or frozenset
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), {(0, 1, 0)})
        Traceback (most recent call last):
          ...
        ValueError: collection of operators must only contain valid operators
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), {(0, 1)})
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 3 that have only the specified operators
        >>> id_not_and_or = {logical.id_, logical.not_, logical.and_, logical.or_}
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), id_not_and_or, 123)
        Traceback (most recent call last):
          ...
        TypeError: collection of operators the number of which to minimize must be a ... frozenset
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), id_not_and_or, {(0, 1, 0)})
        Traceback (most recent call last):
          ...
        ValueError: collection of operators the number of which to minimize must ... operators
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), id_not_and_or, {(0, 1)})
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 3 for specified operators ... criteria

        Additional exhaustive tests are presented below.

        >>> from itertools import product
        >>> evals = lambda c, a: tuple([c.evaluate(v)[0] for v in product(*[[0, 1]]*a)])
        >>> _d = {i: _db[i][1] for i in range(1,4)}
        >>> aoms = [(a, o, m) for a in _d for o in _d[a] for m in _d[a][o]]
        >>> all(
        ...     all(t == evals(circuitdb(t, o, m), a) for t in product(*[[0, 1]]*(2**a)))
        ...     for (a, o, m) in aoms
        ... )
        True
        >>> evals = lambda c, a: tuple([tuple(c.evaluate(v)) for v in product(*[[0, 1]]*a)])
        >>> aoms = [(a, o, m) for a in [2] for o in _db[a][2] for m in _db[a][2][o]]
        >>> pairs = [(0, 0), (0, 1), (1, 0), (0, 1)]
        >>> all(
        ...     all(t == evals(circuitdb(t, o, m), a) for t in product(*[pairs]*(2**a)))
        ...     for (a, o, m) in aoms
        ... )
        True
        """
        # pylint: disable=too-many-branches

        # Ensure the function truth table is a tuple.
        if not isinstance(truthtable, tuple):
            raise TypeError('truth table must be a tuple')

        # Ensure that the function truth table has valid entry types.
        if all(isinstance(e, tuple) for e in truthtable):
            if not all(all(b in (0, 1, False, True) for b in e) for e in truthtable):
                raise TypeError(
                    'truth table must contain boolean values, integers in the ' +
                    'range [0, 1], or tuples of such'
                )
        elif not all(e in (0, 1, False, True) for e in truthtable):
            raise TypeError(
                'truth table must contain boolean values, integers in the ' +
                'range [0, 1], or tuples of such'
            )

        # Determine the arity of the function represented by the truth table.
        arity = int(math.log2(len(truthtable)))

        # Check that the number of entries in the truth table is a power of two.
        if len(truthtable) < 1 or 2**arity != len(truthtable):
            raise ValueError('truth table must have a length that is a power of two')

        # Determine the number of outputs in the truth table (and check it is consistent).
        coarity = 1
        if all(isinstance(e, tuple) for e in truthtable):
            ls = set(len(e) for e in truthtable)
            if len(ls) == 1:
                coarity = list(ls)[0]
                if coarity < 1:
                    raise ValueError('truth table entries must each represent at least one value')
                if coarity == 1: # Convert tuple of singleton tuples into simple tuple.
                    truthtable = tuple(e[0] for e in truthtable)
            else:
                raise ValueError('truth table entries must all have the same length')

        # Ensure that data for functions of the requested arity and coarity is available.
        if arity not in _db:
            raise ValueError('no entries for functions of arity ' + str(arity))

        if coarity not in _db[arity]:
            raise ValueError(
                'no entries for functions of arity ' + str(arity) + ' ' +
                'having output vectors of length ' + str(arity)
            )

        # Normalize the truth table representation.
        if coarity == 1:
            truthtable = tuple(map(int, truthtable))
        else:
            truthtable = tuple(tuple(map(int, e)) for e in truthtable)

        # Allow all operators by default or check that data is present for given operators.
        operators = logical.every if operators is None else operators

        if not isinstance(operators, (set, frozenset)):
            raise TypeError('collection of operators must be a set or frozenset')

        if not operators.issubset(logical.every):
            raise ValueError('collection of operators must only contain valid operators')

        if frozenset(operators) not in _db[arity][1]:
            raise ValueError(
                'no entries for functions of arity ' + str(arity) + ' ' +
                'that have only the specified operators'
            )

        # Minimize the total number of operators of any available kind by default.
        minimize_ = list(sorted(list(_db[arity][1][frozenset(operators)].keys())))[0]
        minimize = minimize_ if minimize is None else minimize

        # Check that the operators to minimize are valid and corresponding data exists.
        if not isinstance(minimize, (set, frozenset)):
            raise TypeError(
                'collection of operators the number of which to minimize ' +
                'must be a set or frozenset'
            )

        if not minimize.issubset(logical.every):
            raise ValueError(
                'collection of operators the number of which to minimize ' +
                'must contain only valid operators'
            )

        if frozenset(minimize) not in _db[arity][1][frozenset(operators)]:
            raise ValueError(
                'no entries for functions of arity ' + str(arity) + ' ' +
                'for specified operators and minimization criteria'
            )

        # The bracket notation below is overloaded in the :obj:`records.__getitem__` method,
        # so there is no risk of users modifying the data.
        return _db[arity][coarity][frozenset(operators)][frozenset(minimize)][truthtable]

# Exported object with function-like and dictionary-like interfaces
# hides the class definition that is used to construct it (unless
# this module is being used to auto-generate documentation).
if os.environ.get('CIRCUITDB_DOCS') != '1':
    cls: type = circuitdb
    circuitdb: cls = cls(_db)

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
