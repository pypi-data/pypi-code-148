from collections.abc import Iterable
from dataclasses import dataclass, field
import itertools
import os
import shutil
from typing import Union

import htcondor

from .options import Argument, Option


@dataclass
class Layer:
    """Defines a single layer (or set of related jobs) in an HTCondor DAG.

    Stores submit configuration for a set of nodes as well as
    providing functionality to determine the parent-child
    relationships between nodes.

    Parameters
    ----------
    executable
        The path of the executable to run.
    name
        The human-readable name of this node. Defaults to the basename
        of the executable if not given.
    universe
        The execution environment for a job. Defaults to 'vanilla'.
    retries
        The number of retries given for a job. Defaults to 3.
    transfer_files
        Whether to leverage Condor file transfer for moving around
        files. On by default.
    dynamic_memory
        Whether to dynamically increase memory request if jobs are
        put on hold due to going over memory requested.
        Off by default.
    requirements
        Additional key-value pairs in the submit description.
    inputs
        The arguments the nodes takes as inputs. If not specified,
        they will be automatically generated when nodes are added
        to this layer.
    outputs
        The arguments the nodes takes as outputs. If not specified,
        they will be automatically generated when nodes are added
        to this layer.
    nodes
        The nodes representing the layer. Nodes can be passed upon
        instantiation or added to the layer after the fact via
        Layer.append(node), Layer.extend(nodes), or Layer += node.

    """

    executable: str
    name: str = ""
    universe: str = "vanilla"
    log_dir: str = "logs"
    retries: int = 3
    transfer_files: bool = True
    dynamic_memory: bool = False
    requirements: dict = field(default_factory=dict)
    inputs: dict = field(default_factory=dict)
    outputs: dict = field(default_factory=dict)
    nodes: list = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            self.name = os.path.basename(self.executable)

    def config(self):
        # check that nodes are valid
        self.validate()

        # add base submit opts + requirements
        submit_options = {
            "universe": self.universe,
            "executable": shutil.which(self.executable),
            "arguments": self._arguments(),
            "periodic_release": "(HoldReasonCode == 5)",
            **self.requirements,
        }

        # file submit opts
        if self.transfer_files:
            inputs = self._inputs()
            outputs = self._outputs()
            output_remaps = self._output_remaps()

            if inputs or outputs:
                submit_options["should_transfer_files"] = "YES"
                submit_options["when_to_transfer_output"] = "ON_SUCCESS"
                submit_options["success_exit_code"] = 0
                submit_options["preserve_relative_paths"] = True
            if inputs:
                submit_options["transfer_input_files"] = inputs
            if outputs:
                submit_options["transfer_output_files"] = outputs
                submit_options["transfer_output_remaps"] = f'"{output_remaps}"'

        # log submit opts
        submit_options[
            "output"
        ] = f"{self.log_dir}/$(nodename)-$(cluster)-$(process).out"
        submit_options[
            "error"
        ] = f"{self.log_dir}/$(nodename)-$(cluster)-$(process).err"

        # extra boilerplate submit opts
        submit_options["notification"] = "never"

        # set dynamic memory opts if requested
        if self.dynamic_memory:
            base_memory = submit_options["request_memory"]
            submit_options["+MemoryUsage"] = f"( {base_memory} )"
            submit_options["request_memory"] = "( MemoryUsage ) * 3 / 2"
            hold_condition = (
                "((CurrentTime - EnteredCurrentStatus > 180)"
                " && (HoldReasonCode != 34))"
            )
            submit_options["periodic_release"] = " || ".join(
                [
                    submit_options["periodic_release"],
                    hold_condition,
                ]
            )

        return {
            "name": self.name,
            "submit_description": htcondor.Submit(submit_options),
            "vars": self._vars(),
            "retries": self.retries,
        }

    def append(self, node: "Node"):
        """Append a node to this layer."""
        assert isinstance(node.inputs, list)
        assert isinstance(node.outputs, list)
        for input_ in node.inputs:
            self.inputs.setdefault(input_.name, []).append(input_.argument)
        for output in node.outputs:
            self.outputs.setdefault(output.name, []).append(output.argument)
        self.nodes.append(node)

    def extend(self, nodes: Iterable["Node"]):
        """Append multiple nodes to this layer."""
        for node in nodes:
            self.append(node)

    def __iadd__(self, nodes):
        if isinstance(nodes, Iterable):
            self.extend(nodes)
        else:
            self.append(nodes)
        return self

    def validate(self):
        """Ensure all nodes in this layer are consistent with each other."""
        assert self.nodes, "at least one node must be connected to this layer"

        # check arg names across nodes are equal
        args = [arg.name for arg in self.nodes[0].arguments]
        for node in self.nodes[:-1]:
            assert args == [arg.name for arg in node.arguments]

        # check input/output names across nodes are equal
        inputs = [arg.name for arg in self.nodes[0].inputs]
        for node in self.nodes[:-1]:
            assert inputs == [arg.name for arg in node.inputs]
        outputs = [arg.name for arg in self.nodes[0].outputs]
        for node in self.nodes[:-1]:
            assert outputs == [arg.name for arg in node.outputs]

    @property
    def has_dependencies(self):
        """Check if any of the nodes in this layer have dependencies."""
        return any([node.requires for node in self.nodes])

    def _arguments(self):
        args = [f"$({arg.condor_name})" for arg in self.nodes[0].arguments]
        io_args = []
        io_opts = []
        for arg in itertools.chain(self.nodes[0].inputs, self.nodes[0].outputs):
            if not arg.suppress:
                if isinstance(arg, Argument):
                    io_args.append(f"$({arg.condor_name})")
                else:
                    io_opts.append(f"$({arg.condor_name})")
        return " ".join(itertools.chain(args, io_opts, io_args))

    def _inputs(self):
        return ",".join([f"$(input_{arg.condor_name})" for arg in self.nodes[0].inputs])

    def _outputs(self):
        return ",".join(
            [f"$(output_{arg.condor_name})" for arg in self.nodes[0].outputs]
        )

    def _output_remaps(self):
        return ";".join(
            [f"$(output_{arg.condor_name}_remap)" for arg in self.nodes[0].outputs]
        )

    def _vars(self):
        allvars = []
        for i, node in enumerate(self.nodes):
            nodevars = {"nodename": f"{self.name}_{i:05X}"}
            # add arguments which aren't suppressed
            if node.arguments:
                nodevars.update(
                    {
                        arg.condor_name: arg.vars()
                        for arg in node.arguments
                        if not arg.suppress
                    }
                )
            # then add arguments defined as 'inputs'. if file transfer is enabled,
            # also define the $(input_{arg}) variable containing the files
            if node.inputs:
                if self.transfer_files:
                    # adjust file location for input files if they are absolute paths.
                    # condor will transfer the file /path/to/file.txt to the job's
                    # current working directory, so arguments should point to file.txt
                    args = {}
                    for arg in node.inputs:
                        if not arg.suppress:
                            args[f"{arg.condor_name}"] = arg.vars(
                                basename=os.path.isabs
                            )
                    nodevars.update(args)
                    nodevars.update(
                        {f"input_{arg.condor_name}": arg.files() for arg in node.inputs}
                    )
                else:
                    nodevars.update(
                        {
                            f"{arg.condor_name}": arg.vars()
                            for arg in node.inputs
                            if not arg.suppress
                        }
                    )
            # finally, add arguments defined as 'outputs'. if file transfer is
            # enabled, also define the $(output_{arg}) variable containing the
            # files. if argument if not suppressed, some extra hoops are done
            # with remaps to ensure that files are also saved to the right
            # place. the main problem is that when jobs are submitted, the
            # directory structure is present in the submit node but not the
            # execute node, so when a job tries to create a file assuming the
            # directories are there, the job fails. this gets around the issue
            # by writing the files to the root directory then remaps them so
            # they get stored in the right place after the job completes and
            # files are transferred back
            if node.outputs:
                for arg in node.outputs:
                    if not arg.suppress:
                        basename = self.transfer_files and arg.remap
                        nodevars.update(
                            {f"{arg.condor_name}": arg.vars(basename=basename)}
                        )
                    if self.transfer_files:
                        if arg.remap:
                            nodevars.update(
                                {f"output_{arg.condor_name}": arg.files(basename=True)}
                            )
                            nodevars.update(
                                {f"output_{arg.condor_name}_remap": arg.remaps()}
                            )
                        else:
                            nodevars.update({f"output_{arg.condor_name}": arg.files()})
            allvars.append(nodevars)

        return allvars


@dataclass
class Node:
    """Defines a single node (or job) in an HTCondor DAG.

    Stores both the arguments used within a job as well
    as capturing any inputs and outputs the job uses/creates.

    Parameters
    ----------
    arguments
        The arguments the node uses which aren't I/O related.
    inputs
        The arguments the node takes as inputs.
    outputs
        The arguments the node takes as outputs.

    """

    arguments: Union[Argument, Option, list] = field(default_factory=list)
    inputs: Union[Argument, Option, list] = field(default_factory=list)
    outputs: Union[Argument, Option, list] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.arguments, Argument) or isinstance(self.arguments, Option):
            self.arguments = [self.arguments]
        if isinstance(self.inputs, Argument) or isinstance(self.inputs, Option):
            self.inputs = [self.inputs]
        if isinstance(self.outputs, Argument) or isinstance(self.outputs, Option):
            self.outputs = [self.outputs]

    @property
    def requires(self):
        """
        Returns
        -------
        list
            The inputs this node explicitly depends on to run.

        """
        assert isinstance(self.inputs, list)
        return list(
            itertools.chain(*[input_.args() for input_ in self.inputs if input_.track])
        )

    @property
    def provides(self):
        """
        Returns
        -------
        list
            The outputs this node provides when it completes.

        """
        assert isinstance(self.outputs, list)
        return list(
            itertools.chain(*[output.args() for output in self.outputs if output.track])
        )
