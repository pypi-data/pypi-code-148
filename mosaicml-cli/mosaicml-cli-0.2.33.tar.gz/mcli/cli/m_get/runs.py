"""Implementation of mcli get runs"""
from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Generator, List, Optional

from mcli.api.exceptions import cli_error_handler
from mcli.cli.common.run_filters import configure_run_filter_argparser, get_runs_with_filters
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay, format_timestamp
from mcli.objects.clusters.cluster_info import get_cluster_list
from mcli.sdk import Run
from mcli.serverside.clusters import GPUType
from mcli.serverside.clusters.cluster_instances import InstanceRequest, UserInstanceRegistry
from mcli.utils.utils_run_status import RunStatus

logger = logging.getLogger(__name__)


class RunColumns(Enum):
    NAME = 'name'
    CLUSTER = 'cluster'
    GPU_TYPE = 'gpu_type'
    GPU_NUM = 'gpu_num'
    CREATED_TIME = 'created_time'
    START_TIME = 'start_time'
    END_TIME = 'end_time'
    STATUS = 'status'


@dataclass
class RunDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for display purposes.
    """
    name: str
    gpu_num: str
    created_time: str
    start_time: str
    end_time: str
    status: str
    cluster: Optional[str] = None
    gpu_type: Optional[str] = None

    @classmethod
    def from_run(cls, run: Run, use_compact_view: bool) -> RunDisplayItem:
        display_status = run.status.display_name
        if run.reason:
            display_status = f"{display_status} ({run.reason})"
        extracted: Dict[str, str] = {
            RunColumns.NAME.value: run.name,
            RunColumns.GPU_NUM.value: str(run.config.gpu_num),
            RunColumns.CREATED_TIME.value: format_timestamp(run.created_at),
            RunColumns.START_TIME.value: format_timestamp(run.started_at),
            RunColumns.END_TIME.value: format_timestamp(run.completed_at),
            RunColumns.STATUS.value: display_status
        }
        if not use_compact_view:
            extracted.update({
                RunColumns.CLUSTER.value: run.config.cluster,
                RunColumns.GPU_TYPE.value: run.config.gpu_type,
            })

        return RunDisplayItem(**extracted)


class MCLIRunDisplay(MCLIGetDisplay):
    """Display manager for runs
    """

    def __init__(self, models: List[Run]):
        self.models = sorted(models, key=lambda x: x.created_at, reverse=True)

        # Omit cluster and gpu_type columns if there only exists one valid cluster/gpu_type combination
        # available to the user
        self.use_compact_view = False
        clusters_list = get_cluster_list()
        if len(clusters_list) == 1:
            request = InstanceRequest(cluster=clusters_list[0].name, gpu_type=None, gpu_num=None)
            user_instances = UserInstanceRegistry()
            options = user_instances.lookup(request)
            num_gpu_types = len({x.gpu_type for x in options if GPUType.from_string(x.gpu_type) != GPUType.NONE})
            if num_gpu_types <= 1:
                self.use_compact_view = True

    @property
    def override_column_ordering(self) -> Optional[List[str]]:
        if self.use_compact_view:
            return [
                RunColumns.GPU_NUM.value, RunColumns.CREATED_TIME.value, RunColumns.START_TIME.value,
                RunColumns.END_TIME.value, RunColumns.STATUS.value
            ]
        return [e.value for e in RunColumns][1:]  # exclude 'name' column

    def __iter__(self) -> Generator[RunDisplayItem, None, None]:
        for model in self.models:
            item = RunDisplayItem.from_run(model, self.use_compact_view)
            yield item


@cli_error_handler('mcli get runs')
def cli_get_runs(
    name_filter: Optional[List[str]] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[RunStatus]] = None,
    output: OutputDisplay = OutputDisplay.TABLE,
    **kwargs,
) -> int:
    """Get a table of ongoing and completed runs
    """
    del kwargs

    runs = get_runs_with_filters(
        name_filter,
        cluster_filter,
        before_filter,
        after_filter,
        gpu_type_filter,
        gpu_num_filter,
        status_filter,
    )

    display = MCLIRunDisplay(runs)
    display.print(output)

    return 0


def get_runs_argparser(subparsers: argparse._SubParsersAction):
    """Configures the ``mcli get runs`` argparser
    """

    run_examples: str = """Examples:
    $ mcli get runs

    NAME                         CLUSTER   GPU_TYPE      GPU_NUM      CREATED_TIME     STATUS
    run-foo                      c-1        g0-type       8            05/06/22 1:58pm  Completed
    run-bar                      c-2        g0-type       1            05/06/22 1:57pm  Completed
    """
    runs_parser = subparsers.add_parser('runs',
                                        aliases=['run'],
                                        help='Get information on all of your existing runs across all clusters.',
                                        epilog=run_examples,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)

    configure_run_filter_argparser('get', runs_parser, include_all=False)
    runs_parser.set_defaults(func=cli_get_runs)
    return runs_parser
