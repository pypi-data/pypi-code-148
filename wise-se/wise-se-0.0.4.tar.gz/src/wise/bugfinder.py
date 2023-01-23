"""
(** A task list is a list of programs to be executed in a given symbolic state. *)
Definition tasks := list (sym_state * IMP).
"""
from dataclasses import dataclass
from typing import List, Tuple, Optional

from toolz import curry

from wise.imp import (
    Imp,
    Seq,
    Bexpr,
    Skip,
    Aff,
    Err,
    Ite,
    Band,
    Bnot,
    Loop,
    is_error,
    Bcst,
)
from wise.streams import Stream, stream_map, scons
from wise.symex import SymState, SymStore, sym_update, sym_aeval, sym_beval, Id

Tasks = List[Tuple[SymState, Imp]]

"""
(** A [status] corresponds to the current state of the bugfinding loop *)
Inductive status :=
  | BugFound (s : sym_state * IMP)
  | Pending
  (* | Clear    (s : sym_state * IMP) *)
  (* | Pending  (s : sym_state * IMP) *)
  | Finished.
"""


@dataclass(frozen=True)
class Status:
    pass


@dataclass(frozen=True)
class BugFound(Status):
    s: Tuple[SymState, Imp]


@dataclass(frozen=True)
class Pending(Status):
    pass


@dataclass(frozen=True)
class Finished(Status):
    pass


"""
Definition node := option (sym_state * IMP).
"""
Node = Optional[Tuple[SymState, Imp]]


@curry
def then_do(q: Imp, task: Tuple[SymState, Imp]) -> Tuple[SymState, Imp]:
    """
    Definition then_do q '(((path, env), p) : sym_state * IMP) :=
      ((path, env), Seq p q).
    """
    (path, env), p = task
    return (path, env), Seq(p, q)


def exec_task(path: Bexpr, env: SymStore, prog: Imp) -> List[Tuple[SymState, Imp]]:
    """
    (** Executing a task according to [sym_step] *)
    Fixpoint exec_task path env prog : list (sym_state * IMP) :=
      match prog with
      | Skip => []
      | Aff x e =>
        [(path, sym_update env x (sym_aeval env e), Skip)]
      | Err => []
      | Ite b p1 p2 =>
        [
          (Band path (sym_beval env b), env, p1);
          (Band path (Bnot (sym_beval env b)), env, p2)
        ]
      | Loop b p =>
        [
          (Band path (sym_beval env b), env, Seq p (Loop b p));
          (Band path (Bnot (sym_beval env b)), env, Skip)
        ]
      | Seq Skip p2 => [(path, env, p2)]
      | Seq p1 p2 =>
        List.map (then_do p2) (exec_task path env p1)
      end.
    """

    match prog:
        case Skip():
            return []
        case Aff(x, e):
            return [((path, sym_update(env, x, sym_aeval(env, e))), Skip())]
        case Err():
            return []
        case Ite(b, p1, p2):
            return [
                ((Band(path, sym_beval(env, b)), env), p1),
                ((Band(path, Bnot(sym_beval(env, b))), env), p2),
            ]
        case Loop(b, p):
            return [
                ((Band(path, sym_beval(env, b)), env), Seq(p, Loop(b, p))),
                ((Band(path, Bnot(sym_beval(env, b))), env), Skip()),
            ]
        case Seq(Skip(), p2):
            return [((path, env), p2)]
        case Seq(p1, p2):
            return list(map(then_do(p2), exec_task(path, env, p1)))

    assert False


def run(l: Tasks) -> Stream[Node]:
    """
    (** Bugfinding loop: at every iteration, a task is chosen and then executed.
        If the execution results in an error, a [BugFound] message is
        emitted. If executing the task terminates in a state [s] without error,
        a message [Clear s] is emitted. If executing the task generates a list [l] of
        subtasks, then the loop signals that further computations are pending and add
        [l] to the worklist. Finally, if the task list is empty, the loop emits the
        token [Finished] continuously.
        *)
    CoFixpoint run (l : tasks) : stream node :=
      match l with
      | [] => scons None (run [])
      | ((path, env), prog)::next =>
        let next_next := exec_task path env prog in
        scons (Some (path, env, prog)) (run (next ++ next_next))
      end.
    """

    match l:
        case []:
            return scons(None, lambda: run([]))
        case [((path, env), prog), *next_]:
            next_next = exec_task(path, env, prog)
            return scons(((path, env), prog), lambda: run(next_ + next_next))


def display(n: Node) -> Status:
    """
    Definition display (n : node) : status :=
      match n with
      | None => Finished
      | Some (path, env, prog) =>
        if is_error prog then BugFound (path, env, prog)
        else Pending
      end.
    """
    match n:
        case None:
            return Finished()
        case ((path, env), prog):
            return BugFound(((path, env), prog)) if is_error(prog) else Pending()


def init(p: Imp) -> List[Tuple[SymState, Imp]]:
    """
    Definition init (p : IMP) : list (sym_state * IMP) :=
      [((Bcst true, id), p)].
    """
    return [((Bcst(True), Id()), p)]


def find_bugs(p: Imp) -> Stream[Status]:
    """
    Definition find_bugs (p : IMP) : stream status :=
      map display (run (init p)).
    """

    return stream_map(display, run(init(p)))
