from collections import defaultdict
import os
from pathlib import Path
import re
from typing import Optional, Tuple

from htcondor import dags

from .layers import Layer


class DAG(dags.DAG):
    """Defines a DAGMan workflow including the execution graph and related config.

    Parameters
    ----------
    config
        If specified, any user-level configuration passed in for convenience
    *args
        Any positional arguments that htcondor.dags.DAG accepts
    **kwargs
        Any keyword arguments that htcondor.dags.DAG accepts

    """

    def __init__(self, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self._node_layers = {}
        self._layers = {}
        self._provides = {}

    def attach(self, layer: Layer):
        """Attach a layer of related job nodes to this DAG.

        Parameters
        ----------
        layer
            The layer to attach.

        """
        key = layer.name
        if key in self._layers:
            return KeyError(f"{key} layer already added to DAG")
        self._layers[layer.name] = layer

        # determine parent-child relationships and connect accordingly
        all_edges = defaultdict(set)
        if layer.has_dependencies:
            # determine edges
            for child_idx, node in enumerate(layer.nodes):
                for input_ in node.requires:
                    if input_ in self._provides:
                        parent_name, parent_idx = self._provides[input_]
                        all_edges[parent_name].add((parent_idx, child_idx))

            if not all_edges:
                self._node_layers[key] = self.layer(**layer.config())

            # determine edge type and connect
            for num, (parent, edges) in enumerate(all_edges.items()):
                edge = self._get_edge_type(parent, layer.name, edges)
                if num == 0:
                    self._node_layers[key] = self._node_layers[parent].child_layer(
                        **layer.config(), edge=edge
                    )
                else:
                    self._node_layers[key].add_parents(
                        self._node_layers[parent], edge=edge
                    )

        else:
            self._node_layers[key] = self.layer(**layer.config())

        # register any data products the layer provides
        for idx, node in enumerate(layer.nodes):
            for output in node.provides:
                self._provides[output] = (key, idx)

    def create_log_dir(self, log_dir: Path = Path("logs")):
        """Create the log directory where job logs are stored.

        If not specified, creates a log directory in ./logs
        """
        os.makedirs(log_dir, exist_ok=True)

    def write_dag(self, filename: str, path: Path = Path.cwd(), **kwargs):
        """Write out the given DAG to the given directory.

        This includes the DAG description file itself, as well as any
        associated submit descriptions.
        """
        write_dag(self, dag_file_name=filename, dag_dir=path, **kwargs)

    def write_script(
        self,
        filename: str,
        path: Path = Path.cwd(),
        formatter: Optional[dags.NodeNameFormatter] = None,
    ):
        if not formatter:
            formatter = HexFormatter()

        # write script
        with open(path / filename, "w") as f:
            # traverse DAG in breadth-first order
            for layer in self.walk(dags.WalkOrder("BREADTH")):
                # grab relevant submit args, format $(arg) to {arg}
                executable = layer.submit_description["executable"]
                args = layer.submit_description["arguments"]
                args = re.sub(r"\$\(((\w+?))\)", r"{\1}", args)

                # evaluate vars for each node in layer, write to disk
                for idx, node_vars in enumerate(layer.vars):
                    node_name = formatter.generate(layer.name, idx)
                    print(f"# Job {node_name}", file=f)
                    print(executable + " " + args.format(**node_vars) + "\n", file=f)

    def _get_edge_type(self, parent_name, child_name, edges):
        parent = self._layers[parent_name]
        child = self._layers[child_name]
        edges = sorted(list(edges))

        # check special cases, defaulting to explicit edge connections via indices
        if len(edges) == (len(parent.nodes) + len(child.nodes)):
            return dags.ManyToMany()

        elif len(parent.nodes) == len(child.nodes) and all(
            [parent_idx == child_idx for parent_idx, child_idx in edges]
        ):
            return dags.OneToOne()

        else:
            return EdgeConnector(edges)


class HexFormatter(dags.SimpleFormatter):
    """A hex-based node formatter that produces names like LayerName_000C."""

    def __init__(self, offset: int = 0):
        self.separator = "."
        self.index_format = "{:05X}"
        self.offset = offset

    def parse(self, node_name: str) -> Tuple[str, int]:
        layer, hex_index = node_name.split(self.separator)
        index = int(hex_index, 16)
        return layer, index - self.offset


class EdgeConnector(dags.BaseEdge):
    """This edge connects individual nodes in layers given an explicit mapping."""

    def __init__(self, indices):
        self.indices = indices

    def get_edges(self, parent, child, join_factory):
        for parent_idx, child_idx in self.indices:
            yield (parent_idx,), (child_idx,)


def write_dag(
    dag: dags.DAG,
    dag_dir: Path = Path.cwd(),
    formatter: Optional[dags.NodeNameFormatter] = None,
    **kwargs,
):
    """Write out the given DAG to the given directory.

    This includes the DAG description file itself, as well as any associated
    submit descriptions.
    """
    if not formatter:
        formatter = HexFormatter()
    return dags.write_dag(dag, dag_dir, node_name_formatter=formatter, **kwargs)
