import ast
from typing import Iterable, Any

ERROR_CODE = "DOC001"
CHECK = "missing docstring"
VERSION = "0.1.1"


class DocstringChecker(ast.NodeVisitor):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.errors: list[tuple[int, int, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # guard 1: if return type is Mock, don't check for docstring
        if isinstance(node.returns, ast.Name) and node.returns.id.endswith("Mock"):
            return

        if ast.get_docstring(node) is None:
            self.errors.append(
                (
                    node.lineno,
                    node.col_offset,
                    f"{ERROR_CODE} Missing docstring for function '{node.name}'",
                )
            )



class Plugin:
    name = "flake8-has-docstring"
    version = VERSION

    def __init__(self, tree: ast.Module) -> None:
        self.tree = tree

    def run(self) -> Iterable[tuple[int, int, str, str]]:
        visitor = DocstringChecker()
        visitor.visit(self.tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, ""
