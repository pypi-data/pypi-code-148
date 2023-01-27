import ast
import sys
from typing import Any, Generator, List, Tuple, Type

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


VARS = ["DEBUG", "TEST"]


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.problems: List[Tuple[int, int, str]] = []

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if hasattr(target, "id"):
                        if str(target.id).upper() in VARS:
                            if hasattr(node.value, "value") and node.value.value:
                                self.problems.append(
                                    (node.lineno, node.col_offset, target.id)
                                )
                            if hasattr(node.value, "n") and node.value.n:
                                self.problems.append(
                                    (node.lineno, node.col_offset, target.id)
                                )
                if isinstance(target, ast.Attribute):
                    if hasattr(target, "attr"):
                        if str(target.attr).upper() in VARS:
                            if node.value.value:
                                self.problems.append(
                                    (node.lineno, node.col_offset, target.attr)
                                )
        elif isinstance(node.value, ast.NameConstant):
            for target in node.targets:
                if hasattr(target, "id"):
                    if str(target.id).upper() in VARS:
                        if node.value.value:
                            self.problems.append(
                                (node.lineno, node.col_offset, target.id)
                            )
        elif isinstance(node.value, ast.Num):
            for target in node.targets:
                if hasattr(target, "id"):
                    if str(target.id).upper() in VARS:
                        if node.value.n:
                            self.problems.append(
                                (node.lineno, node.col_offset, target.id)
                            )
                if isinstance(target, ast.Attribute):
                    if hasattr(target, "attr"):
                        if str(target.attr).upper() in VARS:
                            if node.value.n:
                                self.problems.append(
                                    (node.lineno, node.col_offset, target.attr)
                                )
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col, var in visitor.problems:
            yield (
                line,
                col,
                f"NDV100 variable '{var}' must be false",
                type(self),
            )
