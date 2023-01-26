import ast
from typing import Any, Iterable

ERROR_CODE = "DOC001"
CHECK = "missing docstring"
VERSION = "0.1.4"


class DocstringChecker(ast.NodeVisitor):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.errors: list[tuple[int, int, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # guard 1: if function is a pytest fixture, don't check for docstring
        if any(
            isinstance(decorator, ast.Attribute)
            and decorator.attr == "fixture"
            and isinstance(decorator.value, ast.Name)
            and decorator.value.id == "pytest"
            for decorator in node.decorator_list
        ):
            return

        # guard 2: if function is a dunder method, don't check for docstring
        if node.name.startswith("__") and node.name.endswith("__"):
            return

        # guard 3: if function has an overload decorator, don't check for docstring
        if any(
            isinstance(decorator, ast.Name) and decorator.id == "overload"
            for decorator in node.decorator_list
        ):
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
