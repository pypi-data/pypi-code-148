"""Module relatif à la logique utilisant sympy.

Les conventions utilisées sont celles de lyceum

- ET: &
- OU: |
- NOT: !
"""

from sympy.logic.boolalg import truth_table
from sympy import symbols, sympify
from operator import methodcaller
from tabulate import tabulate
from sympy.core.expr import Expr as SympyExpr


def logic2str(expr: SympyExpr) -> str:
    """Convertit une expression logique Sympy en str

    en utilisant les conventions de lyceum:

    - ET: &
    - OU: |
    - NOT: !
    """
    return str(expr).replace("~", "!")


def str2logic(expr: str) -> SympyExpr:
    """Convertit str en une expression logique Sympy

    en utilisant les conventions de lyceum:

    - ET: &
    - OU: |
    - NOT: !
    """
    return sympify(expr.replace("!", "~"), {str(s): s for s in symbols("P Q R S T")})


def table_de_verite(expr: str, tablefmt: str = "grid") -> str:
    """Produit la table de vérité d'une expression booléenne
    
    au format markdown grid par défaut
    
    se reporter à la librairie tabulate pour d'autres format
    """
    expr = str2logic(expr)
    variables = sorted(expr.free_symbols, key=methodcaller("__str__"))
    table = []
    for t in truth_table(expr, variables):
        table.append(t[0] + [int(bool(t[1]))])
    return tabulate(
        table,
        variables + [logic2str(expr)],
        tablefmt=tablefmt,
        colalign=["center" for _ in range(len(variables) + 1)],
    )
