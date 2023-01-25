import time
from typing import Any, Callable
from .node import Node
import logging
import threading

log = logging.getLogger("graph")


def evaluate_json(json_eval: dict) -> None:
    def _evaluate_json(dep_inputs: dict[str, Any], state: dict[str, Any], event: threading.Event):
        return eval(json_eval)

    return _evaluate_json


class Graph:
    def __init__(self, sleep_time_seconds=5) -> None:
        self.nodes: dict[str, Node] = {}
        self.num_starter_nodes = 0
        self.outputs: dict[str, Any] = {}
        self.sleep_time_seconds = sleep_time_seconds

    def add_node(self, name: str, dependencies: list[str], fun: Callable) -> Node:
        if name in self.nodes:
            raise ValueError(f"Node {name} already exists")
        node = Node(name)
        self.nodes[node.name] = node
        if dependencies == []:
            self.num_starter_nodes += 1

        # Create all dependencies.
        for dep in dependencies:
            node.dependencies.append(self.nodes[dep])
            self.nodes[dep].num_downstream += 1
        node.fun = fun
        return node

    def remove_node(self, name: str) -> None:
        if name not in self.nodes:
            raise ValueError(f"Node {name} does not exist")
        node = self.nodes[name]
        for dep in node.dependencies:
            dep.num_downstream -= 1
        del self.nodes[name]

    def from_json(self, input: dict) -> None:
        # Create all nodes without dependencies.
        nodes = input["nodes"]
        for name, node in nodes.items():
            n = Node(name)
            if "dependencies" not in node:
                self.num_starter_nodes += 1
            self.nodes[name] = n

        # Create all dependencies.
        for node in self.nodes.values():
            if "fun" in nodes[node.name]:
                node.fun = evaluate_json(nodes[node.name]["fun"])
            if "dependencies" not in nodes[node.name]:
                continue
            for dep in nodes[node.name]["dependencies"]:
                node.dependencies.append(self.nodes[dep])
                self.nodes[dep].num_downstream += 1

    def run(self) -> dict[str, Any]:
        # Run the graph.
        threads_data = []
        for node in self.nodes.values():
            e = threading.Event()
            t = threading.Thread(target=node.listen, args=(e,))
            t.start()
            threads_data.append({"thread": t, "event": e, "node": node})

        # We could just join the threads. But we want to be able to stop the graph early.
        # So if any node throws an exception, we stop the graph by setting all events.
        while True:
            for entry in threads_data:
                node = entry["node"]
                if entry["thread"].is_alive():
                    continue
                if node.exception is not None:
                    for tdata in threads_data:
                        tdata["event"].set()
                    for tdata in threads_data:
                        tdata["thread"].join()
                    raise node.exception
            if all(not data["thread"].is_alive() for data in threads_data):
                break
            time.sleep(self.sleep_time_seconds)

        # Check if any node threw an exception in the meantime.
        for node in self.nodes.values():
            if node.exception is not None:
                log.error("Exception in node %s: %s", node.name, node.exception)
                raise node.exception

        # Get all outputs.
        for node in self.nodes.values():
            self.outputs[node.name] = node.output_queue.get()
        log.info("Graph finished running.")
        return self.outputs
