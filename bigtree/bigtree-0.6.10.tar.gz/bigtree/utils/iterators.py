from typing import Callable, Iterable, List, Tuple

__all__ = [
    "inorder_iter",
    "preorder_iter",
    "postorder_iter",
    "levelorder_iter",
    "levelordergroup_iter",
    "dag_iterator",
]


def inorder_iter(
    tree,
    filter_condition: Callable = None,
    max_depth: int = None,
) -> Iterable:
    """Iterate through all children of a tree.

    In Iteration Algorithm, LNR
        1. Recursively traverse the current node's left subtree.
        2. Visit the current node.
        3. Recursively traverse the current node's right subtree.

    >>> from bigtree import BinaryNode, list_to_binarytree, inorder_iter, print_tree
    >>> num_list = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> root = list_to_binarytree(num_list)
    >>> print_tree(root)
    1
    ├── 2
    │   ├── 4
    │   │   └── 8
    │   └── 5
    └── 3
        ├── 6
        └── 7

    >>> [node.node_name for node in inorder_iter(root)]
    ['8', '4', '2', '5', '1', '6', '3', '7']

    >>> [node.node_name for node in inorder_iter(root, filter_condition=lambda x: x.node_name in ["1", "4", "3", "6", "7"])]
    ['4', '1', '6', '3', '7']

    >>> [node.node_name for node in inorder_iter(root, max_depth=3)]
    ['4', '2', '5', '1', '6', '3', '7']

    Args:
        tree (BaseNode): input tree
        filter_condition (Callable): function that takes in node as argument, optional
            Returns node if condition evaluates to `True`
        max_depth (int): maximum depth of iteration, based on `depth` attribute, optional

    Returns:
        (Iterable[BaseNode])
    """
    if tree and (not max_depth or not tree.depth > max_depth):
        yield from inorder_iter(tree.left, filter_condition, max_depth)
        if not filter_condition or filter_condition(tree):
            yield tree
        yield from inorder_iter(tree.right, filter_condition, max_depth)


def preorder_iter(
    tree,
    filter_condition: Callable = None,
    stop_condition: Callable = None,
    max_depth: int = None,
) -> Iterable:
    """Iterate through all children of a tree.

    Pre-Order Iteration Algorithm, NLR
        1. Visit the current node.
        2. Recursively traverse the current node's left subtree.
        3. Recursively traverse the current node's right subtree.
    It is topologically sorted because a parent node is processed before its child nodes.

    >>> from bigtree import Node, list_to_tree, preorder_iter, print_tree
    >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
    >>> root = list_to_tree(path_list)
    >>> print_tree(root)
    a
    ├── b
    │   ├── d
    │   └── e
    │       ├── g
    │       └── h
    └── c
        └── f

    >>> [node.node_name for node in preorder_iter(root)]
    ['a', 'b', 'd', 'e', 'g', 'h', 'c', 'f']

    >>> [node.node_name for node in preorder_iter(root, filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
    ['a', 'd', 'e', 'g', 'f']

    >>> [node.node_name for node in preorder_iter(root, stop_condition=lambda x: x.node_name=="e")]
    ['a', 'b', 'd', 'c', 'f']

    >>> [node.node_name for node in preorder_iter(root, max_depth=3)]
    ['a', 'b', 'd', 'e', 'c', 'f']

    Args:
        tree (BaseNode): input tree
        filter_condition (Callable): function that takes in node as argument, optional
            Returns node if condition evaluates to `True`
        stop_condition (Callable): function that takes in node as argument, optional
            Stops iteration if condition evaluates to `True`
        max_depth (int): maximum depth of iteration, based on `depth` attribute, optional

    Returns:
        (Iterable[BaseNode])
    """
    if (
        tree
        and (not max_depth or not tree.depth > max_depth)
        and (not stop_condition or not stop_condition(tree))
    ):
        if not filter_condition or filter_condition(tree):
            yield tree
        for child in tree.children:
            yield from preorder_iter(child, filter_condition, stop_condition, max_depth)


def postorder_iter(
    tree,
    filter_condition: Callable = None,
    stop_condition: Callable = None,
    max_depth: int = None,
) -> Iterable:
    """Iterate through all children of a tree.

    Post-Order Iteration Algorithm, LRN
        1. Recursively traverse the current node's left subtree.
        2. Recursively traverse the current node's right subtree.
        3. Visit the current node.

    >>> from bigtree import Node, list_to_tree, postorder_iter, print_tree
    >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
    >>> root = list_to_tree(path_list)
    >>> print_tree(root)
    a
    ├── b
    │   ├── d
    │   └── e
    │       ├── g
    │       └── h
    └── c
        └── f

    >>> [node.node_name for node in postorder_iter(root)]
    ['d', 'g', 'h', 'e', 'b', 'f', 'c', 'a']

    >>> [node.node_name for node in postorder_iter(root, filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
    ['d', 'g', 'e', 'f', 'a']

    >>> [node.node_name for node in postorder_iter(root, stop_condition=lambda x: x.node_name=="e")]
    ['d', 'b', 'f', 'c', 'a']

    >>> [node.node_name for node in postorder_iter(root, max_depth=3)]
    ['d', 'e', 'b', 'f', 'c', 'a']

    Args:
        tree (BaseNode): input tree
        filter_condition (Callable): function that takes in node as argument, optional
            Returns node if condition evaluates to `True`
        stop_condition (Callable): function that takes in node as argument, optional
            Stops iteration if condition evaluates to `True`
        max_depth (int): maximum depth of iteration, based on `depth` attribute, optional

    Returns:
        (Iterable[BaseNode])
    """
    if (
        tree
        and (not max_depth or not tree.depth > max_depth)
        and (not stop_condition or not stop_condition(tree))
    ):
        for child in tree.children:
            yield from postorder_iter(
                child, filter_condition, stop_condition, max_depth
            )
        if not filter_condition or filter_condition(tree):
            yield tree


def levelorder_iter(
    tree,
    filter_condition: Callable = None,
    stop_condition: Callable = None,
    max_depth: int = None,
) -> Iterable:
    """Iterate through all children of a tree.

    Level Order Algorithm
        1. Recursively traverse the nodes on same level.

    >>> from bigtree import Node, list_to_tree, levelorder_iter, print_tree
    >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
    >>> root = list_to_tree(path_list)
    >>> print_tree(root)
    a
    ├── b
    │   ├── d
    │   └── e
    │       ├── g
    │       └── h
    └── c
        └── f

    >>> [node.node_name for node in levelorder_iter(root)]
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    >>> [node.node_name for node in levelorder_iter(root, filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
    ['a', 'd', 'e', 'f', 'g']

    >>> [node.node_name for node in levelorder_iter(root, stop_condition=lambda x: x.node_name=="e")]
    ['a', 'b', 'c', 'd', 'f']

    >>> [node.node_name for node in levelorder_iter(root, max_depth=3)]
    ['a', 'b', 'c', 'd', 'e', 'f']

    Args:
        tree (BaseNode): input tree
        filter_condition (Callable): function that takes in node as argument, optional
            Returns node if condition evaluates to `True`
        stop_condition (Callable): function that takes in node as argument, optional
            Stops iteration if condition evaluates to `True`
        max_depth (int): maximum depth of iteration, based on `depth` attribute, defaults to None

    Returns:
        (Iterable[BaseNode])
    """
    if not isinstance(tree, List):
        tree = [tree]
    next_level = []
    for _tree in tree:
        if _tree:
            if (not max_depth or not _tree.depth > max_depth) and (
                not stop_condition or not stop_condition(_tree)
            ):
                if not filter_condition or filter_condition(_tree):
                    yield _tree
                next_level.extend(list(_tree.children))
    if len(next_level):
        yield from levelorder_iter(
            next_level, filter_condition, stop_condition, max_depth
        )


def levelordergroup_iter(
    tree,
    filter_condition: Callable = None,
    stop_condition: Callable = None,
    max_depth: int = None,
) -> Iterable[Iterable]:
    """Iterate through all children of a tree.

    Level Order Group Algorithm
        1. Recursively traverse the nodes on same level, returns nodes level by level in a nested list.

    >>> from bigtree import Node, list_to_tree, levelordergroup_iter, print_tree
    >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
    >>> root = list_to_tree(path_list)
    >>> print_tree(root)
    a
    ├── b
    │   ├── d
    │   └── e
    │       ├── g
    │       └── h
    └── c
        └── f

    >>> [[node.node_name for node in group] for group in levelordergroup_iter(root)]
    [['a'], ['b', 'c'], ['d', 'e', 'f'], ['g', 'h']]

    >>> [[node.node_name for node in group] for group in levelordergroup_iter(root, filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
    [['a'], [], ['d', 'e', 'f'], ['g']]

    >>> [[node.node_name for node in group] for group in levelordergroup_iter(root, stop_condition=lambda x: x.node_name=="e")]
    [['a'], ['b', 'c'], ['d', 'f']]

    >>> [[node.node_name for node in group] for group in levelordergroup_iter(root, max_depth=3)]
    [['a'], ['b', 'c'], ['d', 'e', 'f']]

    Args:
        tree (BaseNode): input tree
        filter_condition (Callable): function that takes in node as argument, optional
            Returns node if condition evaluates to `True`
        stop_condition (Callable): function that takes in node as argument, optional
            Stops iteration if condition evaluates to `True`
        max_depth (int): maximum depth of iteration, based on `depth` attribute, defaults to None

    Returns:
        (Iterable[Iterable])
    """
    if not isinstance(tree, List):
        tree = [tree]

    current_tree = []
    next_tree = []
    for _tree in tree:
        if (not max_depth or not _tree.depth > max_depth) and (
            not stop_condition or not stop_condition(_tree)
        ):
            if not filter_condition or filter_condition(_tree):
                current_tree.append(_tree)
            next_tree.extend([_child for _child in _tree.children if _child])
    yield tuple(current_tree)
    if len(next_tree) and (not max_depth or not next_tree[0].depth > max_depth):
        yield from levelordergroup_iter(
            next_tree, filter_condition, stop_condition, max_depth
        )


def dag_iterator(dag) -> Iterable[Tuple]:
    """Iterate through all nodes of a Directed Acyclic Graph (DAG).
    Note that node names must be unique.
    Note that DAG must at least have two nodes to be shown on graph.

    1. Visit the current node.
    2. Recursively traverse the current node's parents.
    3. Recursively traverse the current node's children.

    >>> from bigtree import DAGNode, dag_iterator
    >>> a = DAGNode("a", step=1)
    >>> b = DAGNode("b", step=1)
    >>> c = DAGNode("c", step=2, parents=[a, b])
    >>> d = DAGNode("d", step=2, parents=[a, c])
    >>> e = DAGNode("e", step=3, parents=[d])
    >>> [(parent.node_name, child.node_name) for parent, child in dag_iterator(a)]
    [('a', 'c'), ('a', 'd'), ('b', 'c'), ('c', 'd'), ('d', 'e')]

    Args:
        dag (DAGNode): input dag

    Returns:
        (Iterable[Tuple[DAGNode, DAGNode]])
    """
    visited_nodes = set()

    def recursively_parse_dag(node):
        node_name = node.node_name
        visited_nodes.add(node_name)

        # Parse upwards
        for parent in node.parents:
            parent_name = parent.node_name
            if parent_name not in visited_nodes:
                yield parent, node

        # Parse downwards
        for child in node.children:
            child_name = child.node_name
            if child_name not in visited_nodes:
                yield node, child

        # Parse upwards
        for parent in node.parents:
            parent_name = parent.node_name
            if parent_name not in visited_nodes:
                yield from recursively_parse_dag(parent)

        # Parse downwards
        for child in node.children:
            child_name = child.node_name
            if child_name not in visited_nodes:
                yield from recursively_parse_dag(child)

    yield from recursively_parse_dag(dag)
