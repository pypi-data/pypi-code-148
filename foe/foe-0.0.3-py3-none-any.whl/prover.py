from .logic import (
    Equation,
    Function,
    Variable,
    Substitution,
    mgu,
    Problem,
    Sequent,
    Term,
    get_subterm
)
import heapq as hq


class TermInstance():
    def __init__(
        self,
        sequent_index,
        sequent_side,
        equation_index,
        equation_side,
        subterm_index,
    ):
        self.sequent_index = sequent_index
        self.sequent_side = sequent_side
        self.equation_index = equation_index
        self.equation_side = equation_side
        self.subterm_index = subterm_index

    def __repr__(self):
        return "TermInstance({}, {}, {}, {}, {})".format(
            self.sequent_index,
            self.sequent_side,
            self.equation_index,
            self.equation_side,
            self.subterm_index,
        )

    def __eq__(self, other):
        return (
            self.sequent_index == other.sequent_index
            and self.sequent_side == other.sequent_side
            and self.equation_index == other.equation_index
            and self.equation_side == other.equation_side
            and self.subterm_index == other.subterm_index
        )

    def __lt__(self, other):
        return (
            self.sequent_index,
            self.sequent_side,
            self.equation_index,
            self.equation_side,
            self.subterm_index
        ) < (
            other.sequent_index,
            other.sequent_side,
            other.equation_index,
            other.equation_side,
            other.subterm_index
        )

    def sequent(self, sequentlist: list[Sequent]) -> Sequent:
        """Converts the term instance to the corresponding sequent.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.

        Returns
        -------
        Sequent
            The sequent corresponding to the term instance.
        """
        return sequentlist[self.sequent_index]

    def equation(self, sequentlist: list[Sequent]) -> Equation:
        """Converts the sequent instance to the corresponding equation.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.

        Returns
        -------
        Equation
            The equation corresponding to the sequent instance.
        """
        if self.sequent_side == "l":
            eqs = sequentlist[self.sequent_index].antecedent
        elif self.sequent_side == "r":
            eqs = sequentlist[self.sequent_index].succedent
        else:
            raise ValueError(
                "Invalid sequent side: {}. Must be\
                'l' or 'r'.".format(self.sequent_side)
            )
        return eqs[self.equation_index]

    def toplevel(self, sequentlist: list[Sequent]) -> Term:
        """Converts the term instance to the corresponding top level term.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.

        Returns
        -------
        Term
            The term corresponding to the term instance.
        """
        eq = self.equation(sequentlist)
        if self.equation_side == "l":
            return eq.lhs
        elif self.equation_side == "r":
            return eq.rhs
        else:
            raise ValueError(
                "Invalid equation side: {}. Must be\
                'l' or 'r'.".format(self.equation_side)
            )

    def term(self, sequentlist: list[Sequent]) -> Term:
        """Converts the term instance to the corresponding subterm.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.

        Returns
        -------
        Term
            The subterm corresponding to the term instance.
        """
        term = self.toplevel(sequentlist)
        return get_subterm(term, self.subterm_index)

    def superposition(self, sequentlist: list[Sequent]) -> list[Sequent]:
        """Applies superposition to the term instance.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.

        Returns
        -------
        list[Sequent]
            The sequents resulting from applying superposition to the term
            instance.
        """
        if self.sequent_side == "l":
            return self.superposition_antecedent(sequentlist)
        elif self.sequent_side == "r":
            return self.superposition_succedent(sequentlist)
        else:
            raise ValueError(
                "Invalid sequent side: {}. Must be\
                'l' or 'r'.".format(self.sequent_side)
            )


def subtermindices(term: Term) -> list[tuple[int, ...]]:
    """Returns a list of all subterm indices for the given term.

    Parameters
    ----------
    term : Term
        The term to get the subterm indices for.

    Returns
    -------
    list[Tuple]
        The list of subterm indices.
    """
    if isinstance(term, Variable):
        return [tuple()]
    elif isinstance(term, Function):
        indices = [tuple()]
        for i, arg in enumerate(term.arguments):
            for subindex in subtermindices(arg):
                indices.append((i,) + subindex)
        return indices
    else:
        raise ValueError(
            "Invalid term type: {}. Must be\
            Variable or Function.".format(type(term))
        )


def positive_toplevel_terminstances(
    sequentlist: list[Sequent]
) -> list[TermInstance]:
    """Converts a list of sequents to a list of top level term instances.

    Parameters
    ----------
    sequentlist : list[Sequent]
        The list of sequents to convert.

    Returns
    -------
    list[TermInstance]
        The list of top level term instances.
    """
    terminstances = []
    for i, seq in enumerate(sequentlist):
        for j, eq in enumerate(seq.succedent):
            for side in ["l", "r"]:
                terminstances.append(
                    TermInstance(i, "r", j, side, tuple())
                )
    return terminstances


def terminstances(sequentlist: list[Sequent]) -> list[TermInstance]:
    """Converts a list of sequents to a list of term instances.

    Parameters
    ----------
    sequentlist : list[Sequent]
        The list of sequents to convert.

    Returns
    -------
    list[TermInstance]
        The list of term instances.
    """
    terminstances = []
    for i, seq in enumerate(sequentlist):
        for j, eq in enumerate(seq.antecedent):
            for subindex in subtermindices(eq.lhs):
                terminstances.append(
                    TermInstance(i, "l", j, "l", subindex)
                )
            for subindex in subtermindices(eq.rhs):
                terminstances.append(
                    TermInstance(i, "l", j, "r", subindex)
                )
        for j, eq in enumerate(seq.succedent):
            for subindex in subtermindices(eq.lhs):
                terminstances.append(
                    TermInstance(i, "r", j, "l", subindex)
                )
            for subindex in subtermindices(eq.rhs):
                terminstances.append(
                    TermInstance(i, "r", j, "r", subindex)
                )
    return terminstances


class Prover():
    def __init__(self, problem: Problem, evaluator):
        self.problem = problem
        self.sequents = [s.normalize() for s in problem.sequents]
        self.evaluator = evaluator
        self.evaluations = hq.heapify(
            [(self.evaluator(s), s) for s in self.sequents]
        )
        self.superposition_instances: dict[
            Sequent,
            list[(
                TermInstance,
                TermInstance,
                dict[Substitution, Substitution]
            )]
        ] = {s: [] for s in self.sequents}
        for toplevel in positive_toplevel_terminstances(self.sequents):
            for index in terminstances(self.sequents):
                m = mgu(
                    toplevel.toplevel(self.sequents),
                    index.term(self.sequents)
                )
                if m:
                    if toplevel.sequent_index == index.sequent_index:
                        if index.subterm_index == ():
                            if index < toplevel:
                                self.superposition_instances[
                                    toplevel.sequent(self.sequents)
                                ].append(
                                    (toplevel, index, m)
                                )
                        else:
                            self.superposition_instances[
                                toplevel.sequent(self.sequents)
                            ].append(
                                (toplevel, index, m)
                            )
                    else:
                        self.superposition_instances[
                            toplevel.sequent(self.sequents)
                        ].append(
                            (toplevel, index, m)
                        )
                        self.superposition_instances[
                            toplevel.sequent(self.sequents)
                        ].append(
                            (index, toplevel, (m[1], m[0]))
                        )

    def expand(self, seq: Sequent):
        """Expands the given sequent.

        Parameters
        ----------
        index : int
            The index of the sequent to expand.

        Returns
        -------
        list
            The expanded sequents.
        """
        expanded = []
        for toplevel, index, m in self.superposition_instances[seq]:
            expanded.append(
                self.superposition(toplevel, index, m)
            )
        return expanded

    def superposition(
        self,
        toplevel: TermInstance,
        index: TermInstance,
        m: dict[Substitution, Substitution]
    ):
        """Performs superposition on the given sequents.

        Parameters
        ----------
        toplevel : TermInstance
            The top level term instance.
        index : TermInstance
            The term instance to superpose.
        m : dict[Substitution, Substitution]
            The most general unifier.

        Returns
        -------
        Sequent
            The sequent resulting from superposition.
        """
        if toplevel.sequent_side == "l":
            return self.superposition_antecedent(toplevel, index, m)
        elif toplevel.sequent_side == "r":
            return self.superposition_succedent(toplevel, index, m)
        else:
            raise ValueError(
                "Invalid sequent side: {}. Must be\
                'l' or 'r'.".format(toplevel.sequent_side)
            )

    def prove(self, maxsteps: int):
        """Attemps a saturation proof of the given problem.

        Parameters
        ----------
        maxsteps : int
            The maximum number of steps to take.

        Returns
        -------
        bool
            True if the sequents are provable, False otherwise.
        """
        pass
