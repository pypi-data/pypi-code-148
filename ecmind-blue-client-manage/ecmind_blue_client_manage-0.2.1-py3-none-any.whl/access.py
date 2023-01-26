from __future__ import annotations


class Access:
    """
    Represents access rights.

    R = Read index data;
    W = Write index data;
    X = Open object;
    D = Delete object;
    U = Write object
    """

    def __init__(
        self,
        R: bool = None,
        W: bool = None,
        X: bool = None,
        D: bool = None,
        U: bool = None,
    ):
        self.R = R
        self.W = W
        self.X = X
        self.D = D
        self.U = U

    def __repr__(self):
        return f'{ "R" if self.R else "-" }{ "W" if self.W else "-" }{ "X" if self.X else "-" }{ "D" if self.D else "-" }{ "U" if self.U else "-" }'

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return (
            (1 if self.R else 0)
            + (2 if self.W else 0)
            + (4 if self.X else 0)
            + (8 if self.D else 0)
            + (16 if self.U else 0)
        )

    def __eq__(self, other):
        return (
            self.R == other.R
            and self.W == other.W
            and self.X == other.X
            and self.D == other.D
            and self.U == other.U
        )

    @staticmethod
    def from_string(permission_string: str) -> Access:
        assert len(permission_string) == 5, "Malformated permission string."
        return Access(
            permission_string[0] == "R",
            permission_string[1] == "W",
            permission_string[2] == "X",
            permission_string[3] == "D",
            permission_string[4] == "U",
        )
