import sys
from tealish import TealishCompiler

lines = open(sys.argv[1]).readlines()


def f(node):
    # line = node.line
    # scope_path = node.get_current_scope()["name"]
    print(node.__class__.__name__)
    # # func_call = node.expression.expression.node
    # # if func_call.name == 'log':
    # # print(scope_path, line)
    # print(scope_path, line)


callers = {}
funcs = []


def visitor(node, func=None):
    if node.__class__.__name__ == "Func":
        func = node.name
        funcs.append(func)
    if node.__class__.__name__ == "FunctionCall":
        print(node, node.name, func)
        callers.setdefault(node.name, [])
        callers[node.name].append(func)
    else:
        print(node)
    if getattr(node, "nodes", []):
        for n in node.nodes:
            visitor(n, func)


compiler = TealishCompiler(lines)
compiler.parse()
# compiler.traverse(visitor=printer)

indent = 0
root = compiler.nodes[0]


def printer(node, level=0):
    indent = " " * level
    print(f"{indent}{node.__class__.__name__}")
    if getattr(node, "nodes", []):
        print(f"{indent}[")
        for n in node.nodes:
            printer(n, level + 1)
        print(f"{indent}]")


printer(root)

output = compiler.compile()
print("\n".join(output))


# visitor(root)

# edges = []
# for f in funcs:
#     for c in callers.get(f, []):
#         edges.append((c, f))

# for e in edges:
#     print(e)
