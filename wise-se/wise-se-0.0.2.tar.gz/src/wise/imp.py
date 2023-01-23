from dataclasses import dataclass

##############
### Syntax ###
##############
from typing import Callable

"""
Definition ident := string.
"""
Ident = str

Z = int

"""
Inductive aexpr : Type :=
  | Var : ident -> aexpr
  | Cst : Z -> aexpr
  | Add : aexpr -> aexpr -> aexpr
  | Sub : aexpr -> aexpr -> aexpr.
"""


@dataclass(frozen=True)
class Aexpr:
    pass


@dataclass(frozen=True)
class Var(Aexpr):
    ident: Ident


@dataclass(frozen=True)
class Cst(Aexpr):
    num: Z


@dataclass(frozen=True)
class Add(Aexpr):
    left: Aexpr
    right: Aexpr


@dataclass(frozen=True)
class Sub(Aexpr):
    left: Aexpr
    right: Aexpr


"""
Inductive bexpr : Type :=
  | Bcst  : bool -> bexpr
  | Ble   : aexpr -> aexpr -> bexpr
  | Beq   : aexpr -> aexpr -> bexpr
  | Bnot  : bexpr -> bexpr
  | Band  : bexpr -> bexpr -> bexpr.
"""


@dataclass(frozen=True)
class Bexpr:
    pass


@dataclass(frozen=True)
class Bcst(Bexpr):
    b: bool


@dataclass(frozen=True)
class Ble(Bexpr):
    left: Aexpr
    right: Aexpr


@dataclass(frozen=True)
class Beq(Bexpr):
    left: Aexpr
    right: Aexpr


@dataclass(frozen=True)
class Bnot(Bexpr):
    expr: Bexpr


@dataclass(frozen=True)
class Band(Bexpr):
    left: Bexpr
    right: Bexpr


def Bor(b1: Bexpr, b2: Bexpr) -> Bexpr:
    """
    Definition Bor (b1 b2 : bexpr) := Bnot (Band (Bnot b1) (Bnot b2)).
    """

    return Bnot(Band(Bnot(b1), Bnot(b2)))


"""
Inductive IMP : Type :=
  | Skip  : IMP
  | Ite   : bexpr -> IMP -> IMP -> IMP
  | Seq   : IMP -> IMP -> IMP
  | Aff   : string -> aexpr -> IMP
  | Err   : IMP
  | Loop  : bexpr -> IMP -> IMP.
"""


@dataclass(frozen=True)
class Imp:
    pass


@dataclass(frozen=True)
class Skip(Imp):
    pass


@dataclass(frozen=True)
class Ite(Imp):
    guard: Bexpr
    then_branch: Imp
    else_branch: Imp


@dataclass(frozen=True)
class Seq(Imp):
    first: Imp
    second: Imp


@dataclass(frozen=True)
class Aff(Imp):
    var: Ident
    expr: Aexpr


@dataclass(frozen=True)
class Err(Imp):
    pass


@dataclass(frozen=True)
class Loop(Imp):
    guard: Bexpr
    body: Imp


def Assert(c: Bexpr) -> Imp:
    """
    Definition Assert c := Ite c Skip Err.
    """
    return Ite(c, Skip(), Err())


def is_error(p: Imp) -> bool:
    """
    (** Executable check for erroneous state *)
    Fixpoint is_error (p : IMP) : bool :=
      match p with
      | Err => true
      | Seq p _ => is_error p
      | _ => false
      end.
    """
    match p:
        case Err():
            return True
        case Seq(p, _):
            return is_error(p)
        case _:
            return False


#################
### Semantics ###
#################

"""
Definition store := ident -> Z.
"""
Store = Callable[[Ident], Z]


def aeval(s: Store, e: Aexpr) -> Z:
    """
    (** Semantic of Arithmetic expressions *)
    Fixpoint aeval (s : store) (e : aexpr) : Z :=
      match e with
      | Var x => s x
      | Cst c => c
      | Add e1 e2 => aeval s e1 + aeval s e2
      | Sub e1 e2 => aeval s e1 - aeval s e2
      end.
    """

    match e:
        case Var(x):
            return s(x)
        case Cst(c):
            return c
        case Add(e1, e2):
            return aeval(s, e1) + aeval(s, e2)
        case Sub(e1, e2):
            return aeval(s, e1) - aeval(s, e2)
