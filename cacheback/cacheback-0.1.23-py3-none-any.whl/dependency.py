import ast
from . import headers
import pip

''' Solution inspired/copied from source: https://stackoverflow.com/a/58847554
    Following snippet uses AST to trace all high level imports. '''

_modules = set()

def _visit_Import(node):
    for name in node.names:
        _modules.add(name.name.split(".")[0])

def _visit_ImportFrom(node):
    if node.module is not None and node.level == 0:
        _modules.add(node.module.split(".")[0])

node_iter = ast.NodeVisitor()
node_iter.visit_Import = _visit_Import
node_iter.visit_ImportFrom = _visit_ImportFrom

def _read_imports_from_notebook(notebook_path):
    codebase = headers.get_code_from_notebook(notebook_path)
    node_iter.visit(ast.parse(codebase))
    print(f"Imports: {_modules}")

def _install_dependencies():
    ''' Automatically install all required dependencies '''
    for module in  _modules:
        install_dependency(module)
    
def install_dependency(package: str):
    ''' Pass package name as parameter, Eg. package=cacheback==0.1.17'''
    try:
        pip.main(["install", package])
    except Exception as e:
        print(e.args[0])

def handle_imports(notebook_path):
    _read_imports_from_notebook(notebook_path)
    _install_dependencies()