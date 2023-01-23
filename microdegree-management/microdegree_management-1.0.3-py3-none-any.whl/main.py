from typing import Optional, Union, Literal
from pathlib import Path
from pydantic import Extra
from pydantic_yaml import YamlModel
import logging
import tempfile
import click
import re

# unfortunately there is no type info ATM
import graphviz  # type: ignore
import yaml
import networkx as nx  # type: ignore


logging.basicConfig(level=logging.DEBUG)


class URL(YamlModel):
    url: str
    description: str


class Assignment(YamlModel):
    description: str
    path: Path
    attachments: Optional[list[Path]]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "examples": [
                {
                    "description": "Oefening for lus",
                    "path": "oefeningen/TypeScript/oefening-for-lus.md",
                    "attachments": ["oefeningen/TypeScript/screenshot-for-lus.png"],
                }
            ]
        }


class Job(YamlModel, extra=Extra.forbid):
    kind: Literal["text"] | Literal["video"] | Literal["proof"] | Literal["assignments"]
    assignee: str
    status: Literal["planned"] | Literal["drafted"] | Literal["reviewable"] | Literal[
        "accepted"
    ] | Literal["needs_update"]
    notes: Optional[str]


class Node(YamlModel, extra=Extra.forbid):
    """A set of learning materials local to the cluster being described."""

    id: str
    title: Optional[str]
    assignments: Optional[list[Assignment]]
    urls: Optional[list[URL]]
    jobs: Optional[list[Job]]


class NodePlaceholder(YamlModel, extra=Extra.forbid):
    """A reference to a Node belonging to a different cluster."""

    cluster: str
    id: str


class Edge(YamlModel, extra=Extra.forbid):
    """A "knowledge dependency" from end_id on start_id."""

    start_id: str
    end_id: str


class Motivation(YamlModel, extra=Extra.forbid):
    """A "motivation dependency" from end_id on start_id."""

    start_id: str
    end_id: str


class Cluster(YamlModel, extra=Extra.forbid):
    """A grouping of thematically related nodes, collected in a single data structure."""

    namespace_prefix: str
    nodes: list[Node]
    edges: list[Edge]
    motivations: Optional[list[Motivation]]


class Module(YamlModel, extra=Extra.forbid):
    clusters: list[Cluster]


@click.group()
def cli() -> None:
    pass


@click.command()
@click.argument("paths", type=click.Path(exists=True), nargs=-1)
def visualize_module(paths) -> None:
    """Show a visual representation of a complete module, with full namespacing."""
    module = Module(clusters=[])
    for path in paths:
        module.clusters.append(Cluster.parse_file(path))
    dot = graphviz.Digraph()
    for cluster in module.clusters:
        nodes: list[Node] = cluster.nodes
        for node in nodes:
            dot.node(
                f"{cluster.namespace_prefix}__{node.id}",
                f"({cluster.namespace_prefix}) {node.title or node.id}",
            )
        edges: list[Edge] = cluster.edges
        for edge in edges:
            start_id = edge.start_id
            end_id = edge.end_id
            if "__" not in start_id:
                start_id = f"{cluster.namespace_prefix}__{start_id}"
            if "__" not in end_id:
                end_id = f"{cluster.namespace_prefix}__{end_id}"
            dot.edge(start_id, end_id)
        if cluster.motivations:
            for motivation in cluster.motivations:
                start_id = motivation.start_id
                end_id = motivation.end_id
                if "__" not in start_id:
                    start_id = f"{cluster.namespace_prefix}__{start_id}"
                if "__" not in end_id:
                    end_id = f"{cluster.namespace_prefix}__{end_id}"
                dot.edge(start_id, end_id, style="dotted")
    dot.render("module.gv", directory=tempfile.gettempdir(), cleanup=True, view=True)


cli.add_command(visualize_module)


@click.command()
@click.argument("path", type=click.Path(exists=True))
def visualize_cluster(path) -> None:
    """Show a visual representation of a cluster, with minimal namespacing."""
    cluster: Cluster = Cluster.parse_file(path)
    dot = graphviz.Digraph()
    nodes: list[Node] = cluster.nodes
    for node in nodes:
        dot.node(f"{cluster.namespace_prefix}__{node.id}", node.title or node.id)
    edges: list[Edge] = cluster.edges
    for edge in edges:
        start_id = edge.start_id
        end_id = edge.end_id
        if "__" not in start_id:
            start_id = f"{cluster.namespace_prefix}__{start_id}"
        if "__" not in end_id:
            end_id = f"{cluster.namespace_prefix}__{end_id}"
        dot.edge(start_id, end_id)
    if cluster.motivations:
        for motivation in cluster.motivations:
            start_id = motivation.start_id
            end_id = motivation.end_id
            if "__" not in start_id:
                start_id = f"{cluster.namespace_prefix}__{start_id}"
            if "__" not in end_id:
                end_id = f"{cluster.namespace_prefix}__{end_id}"
            dot.edge(start_id, end_id, style="dotted")
    dot.render("cluster.gv", directory=tempfile.gettempdir(), cleanup=True, view=True)


cli.add_command(visualize_cluster)


def writeschema() -> None:
    with open("tests/testschema.json", mode="w") as fh:
        fh.write(Cluster.schema_json(indent=2))


def check_redundancy(module: Module) -> Optional[str]:
    raise NotImplementedError("Cannot check for redundancy yet.")


@click.command()
@click.argument("paths", type=click.Path(exists=True), nargs=-1)
def validate_module(paths) -> None:
    """Run sanity checks on the graph structure and contents of a complete module."""
    messages: list[str] = []
    module = Module(clusters=[])
    for path in paths:
        module.clusters.append(Cluster.parse_file(path))
    # an inventory of all qualified names is constructed in a first pass
    # this can be used to check whether or not a node ID used in a dependency is valid
    # CHECKS: no node is namespaced inside its cluster
    qualified_names: set[str] = set()
    for cluster in module.clusters:
        for node in cluster.nodes:
            if "__" in node.id:
                messages.append(
                    f"Node {node.id} in cluster {cluster.namespace_prefix} should not mention namespace."
                )
            qualified_names.add(f"{cluster.namespace_prefix}__{node.id}")
    # CHECKS: all sources / sinks are valid IDs
    for cluster in module.clusters:
        cluster_node_ids = [node.id for node in cluster.nodes]
        for edge in cluster.edges:
            if (
                edge.start_id not in cluster_node_ids
                and edge.start_id not in qualified_names
            ):
                messages.append(
                    f"(Cluster {cluster.namespace_prefix}) Edge {edge.start_id} -> {edge.end_id} contains unknown start node"
                )
            if (
                edge.end_id not in cluster_node_ids
                and edge.end_id not in qualified_names
            ):
                messages.append(
                    f"(Cluster {cluster.namespace_prefix}) Edge {edge.start_id} -> {edge.end_id} contains unknown end node"
                )
        if cluster.motivations:
            for motivation in cluster.motivations:
                if (
                    motivation.start_id not in cluster_node_ids
                    and motivation.start_id not in qualified_names
                ):
                    messages.append(
                        f"(Cluster {cluster.namespace_prefix}) Motivation {motivation.start_id} -> {motivation.end_id} contains unknown start node"
                    )
                if (
                    motivation.end_id not in cluster_node_ids
                    and motivation.end_id not in qualified_names
                ):
                    messages.append(
                        f"(Cluster {cluster.namespace_prefix}) Motivation {motivation.start_id} -> {motivation.end_id} contains unknown end node"
                    )
    for path in paths:
        path = Path(path)
        cluster = Cluster.parse_file(path)
        for node in cluster.nodes:
            if node.assignments:
                for assignment in node.assignments:
                    if assignment.path.is_absolute():
                        assignment_path = assignment.path
                    else:
                        assignment_path = path.parent.joinpath(assignment.path)
                    if not assignment_path.exists():
                        messages.append(
                            f"Path {assignment_path} mentioned in file {path} for node {node.id} does not exist!"
                        )
                    if assignment.attachments:
                        for attachment in assignment.attachments:
                            if attachment.is_absolute():
                                locatable_attachment = attachment
                            else:
                                locatable_attachment = path.parent.joinpath(attachment)
                            if not locatable_attachment.exists():
                                messages.append(
                                    f"Path {locatable_attachment} mentioned in file {path} for node {node.id} as an attachment to assignment {assignment.description} does not exist!"
                                )
    # printing out messages first time here
    # reason is because malformed graph may cause issues
    for message in messages:
        print(message)
    messages = []
    module_dag = module_dependency_graph(module)
    cycles = list(nx.simple_cycles(module_dag))
    if cycles:
        messages.append(f"Cycles: {list(cycles)}")
    module_tr = nx.transitive_reduction(module_dag)
    for edge in module_dag.edges:
        if edge not in module_tr.edges:
            messages.append(f"Redundant edge: {edge}")
    for message in messages:
        print(message)


cli.add_command(validate_module)


@click.command()
@click.argument("node_id")
@click.argument("cluster_path", type=click.Path(exists=True))
def show_hard_dependencies_in_cluster(node_id, cluster_path: Path) -> None:
    """Show all knowledge dependencies of a given node within a particular cluster."""
    cluster: Cluster = Cluster.parse_file(cluster_path)
    node_in_cluster = False
    for present_node in cluster.nodes:
        if present_node.id == node_id:
            dependencies: set[str] = set()
            added_nodes = set([node_id])
            node_in_cluster = True
    if not node_in_cluster:
        raise ValueError(
            "Desired node is not in the cluster. Note that namespacing this node is not currently supported."
        )
    while len(added_nodes) > 0:
        moved_nodes: set[str] = set(added_nodes)
        dependencies = dependencies.union(moved_nodes)
        for moved_node in moved_nodes:
            added_nodes = set(
                [edge.start_id for edge in cluster.edges if edge.end_id == moved_node]
            )
    dependencies.remove(node_id)
    for node_id in sorted(dependencies):
        print(node_id)


cli.add_command(show_hard_dependencies_in_cluster)


def get_hard_dependencies_in_module(
    node_id: str, cluster_paths: list[Path]
) -> set[str]:
    module = Module(clusters=[])
    for path in cluster_paths:
        module.clusters.append(Cluster.parse_file(path))
    node_in_module = False
    for cluster in module.clusters:
        for present_node in cluster.nodes:
            present_node_id = present_node.id
            # always explicitly namespace in module context
            if "__" not in present_node_id:
                present_node_id = f"{cluster.namespace_prefix}__{present_node_id}"
            if present_node_id == node_id:
                # could initialize several times but is harmless
                dependencies: set[str] = set()
                added_nodes = set([node_id])
                node_in_module = True
    if not node_in_module:
        raise ValueError(
            f"Desired node {node_id} is not in the module. Did you check the namespace?"
        )
    while len(added_nodes) > 0:
        moved_nodes: set[str] = set(added_nodes)
        dependencies = dependencies.union(moved_nodes)
        added_nodes = set()
        for moved_node in moved_nodes:
            for cluster in module.clusters:
                namespacify = (
                    lambda x: x if "__" in x else f"{cluster.namespace_prefix}__{x}"
                )
                added_nodes = added_nodes.union(
                    set(
                        [
                            namespacify(edge.start_id)
                            for edge in cluster.edges
                            if namespacify(edge.end_id) == moved_node
                        ]
                    )
                )
    dependencies.remove(node_id)
    return dependencies


@click.command()
@click.argument("node_id")
@click.argument("cluster_paths", type=click.Path(exists=True), nargs=-1)
def show_hard_dependencies_in_module(node_id: str, cluster_paths: list[Path]) -> None:
    """Show all knowledge dependencies of a given node within a complete module."""
    dependencies = get_hard_dependencies_in_module(node_id, cluster_paths)
    for node_id in sorted(dependencies):
        print(node_id)


cli.add_command(show_hard_dependencies_in_module)


@click.command()
@click.argument("cluster_paths", type=click.Path(exists=True), nargs=-1)
def check_learning_path(cluster_paths: list[Path]) -> None:
    """Provide a newline-separated list of namespaced node IDs and check whether it is a valid linear learning path."""
    module = Module(clusters=[])
    for path in cluster_paths:
        module.clusters.append(Cluster.parse_file(path))
    learning_path: list[str] = []
    comment_pattern = re.compile(r" *#.*")
    try:
        while True:
            line = re.sub(comment_pattern,'',input().strip())
            if line != "":
                learning_path.append(line)
    except EOFError:
        pass
    if len(learning_path) > 0:
        seen_namespaced: set[str] = set()
        for (index, namespaced_node_id) in enumerate(learning_path):
            namespaced_hard_dependencies = get_hard_dependencies_in_module(
                namespaced_node_id, cluster_paths
            )
            # first node has to be accessible and has to motivate something
            if index == 0:
                if namespaced_hard_dependencies:
                    print(f"Starting node has hard dependencies:")
                    for dependency in namespaced_hard_dependencies:
                        print(dependency)
                motivates_something = False
                for cluster in module.clusters:
                    if cluster.motivations:
                        for motivation in cluster.motivations:
                            namespaced_start = (
                                motivation.start_id
                                if "__" in motivation.start_id
                                else f"{cluster.namespace_prefix}__{motivation.start_id}"
                            )
                            if namespaced_start == namespaced_node_id:
                                motivates_something = True
                                break
                if not motivates_something:
                    print(f"Starting node does not motivate anything.")
            # other nodes need to be reachable given what has been visited before
            # there also needs to be a motivation to visit them
            # this may be because they are a necessary intermediate step
            else:
                unmet_dependencies = namespaced_hard_dependencies.difference(
                    seen_namespaced
                )
                for dependency in unmet_dependencies:
                    print(
                        f"Node {index} ({namespaced_node_id}) has unmet dependency {dependency}."
                    )
                is_motivated = False
                # don't include motivations in graph
                # this means the current node is a *non-optional* step towards something
                # (everything is a non-optional step towards itself, so direct motivation is possible)
                module_dag = module_dependency_graph(module, include_motivations=False)
                current_and_dependents_namespaced = nx.descendants(
                    module_dag, namespaced_node_id
                )
                current_and_dependents_namespaced.add(namespaced_node_id)
                for cluster in module.clusters:
                    if cluster.motivations:
                        for motivation in cluster.motivations:
                            namespaced_start = (
                                motivation.start_id
                                if "__" in motivation.start_id
                                else f"{cluster.namespace_prefix}__{motivation.start_id}"
                            )
                            namespaced_end = (
                                motivation.end_id
                                if "__" in motivation.end_id
                                else f"{cluster.namespace_prefix}__{motivation.end_id}"
                            )
                            if (
                                namespaced_end in current_and_dependents_namespaced
                                and namespaced_start in seen_namespaced
                            ):
                                is_motivated = True
                                break
                if not is_motivated:
                    print(
                        f"Node {index} ({namespaced_node_id}) is not a motivated part of the learning path."
                    )

            seen_namespaced.add(namespaced_node_id)
    else:
        print("Empty learning path is technically valid, but pointless.")
    print("Done checking path.")


cli.add_command(check_learning_path)


def module_dependency_graph(module: Module, include_motivations=True):
    """Assumes the module has already been validated."""
    dag = nx.DiGraph()
    for cluster in module.clusters:
        for node in cluster.nodes:
            dag.add_node(f"{cluster.namespace_prefix}__{node.id}")
    for cluster in module.clusters:
        for edge in cluster.edges:
            u_of_edge = (
                edge.start_id
                if "__" in edge.start_id
                else f"{cluster.namespace_prefix}__{edge.start_id}"
            )
            v_of_edge = (
                edge.end_id
                if "__" in edge.end_id
                else f"{cluster.namespace_prefix}__{edge.end_id}"
            )
            dag.add_edge(u_of_edge, v_of_edge)
        if include_motivations and cluster.motivations:
            for motivation in cluster.motivations:
                u_of_edge = (
                    edge.start_id
                    if "__" in edge.start_id
                    else f"{cluster.namespace_prefix}__{edge.start_id}"
                )
                v_of_edge = (
                    edge.end_id
                    if "__" in edge.end_id
                    else f"{cluster.namespace_prefix}__{edge.end_id}"
                )
                dag.add_edge(u_of_edge, v_of_edge)
    return dag


if __name__ == "__main__":
    cli()
