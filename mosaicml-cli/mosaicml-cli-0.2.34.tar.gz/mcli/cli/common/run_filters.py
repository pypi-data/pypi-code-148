""" MCLI Run Filters """
import argparse
import fnmatch
import functools
import logging
from typing import Dict, List, Optional, Tuple

from mcli.api.exceptions import MCLIException
from mcli.config import FeatureFlag, MCLIConfig
from mcli.sdk import Run, get_runs
from mcli.utils.utils_cli import comma_separated, date_time_parse
from mcli.utils.utils_logging import console
from mcli.utils.utils_run_status import CLI_STATUS_OPTIONS, RunStatus
from mcli.utils.utils_string_functions import is_glob

logger = logging.getLogger(__name__)


def configure_run_filter_argparser(action: str, parser: argparse.ArgumentParser, include_all: bool = True):

    parser.add_argument(
        dest='name_filter',
        nargs='*',
        metavar='RUN',
        default=None,
        help=f'String or glob of the name(s) of the run(s) to {action}',
    )

    parser.add_argument(
        '-c',
        '--cluster',
        '-p',
        '--platform',
        dest='cluster_filter',
        metavar='CLUSTER',
        type=comma_separated,
        default=None,
        help=f'{action.capitalize()} runs on the specified cluster(s). If no other arguments are provided, will '
        f'{action} all runs on the specified cluster(s). Multiple clusters should be specified '
        'using a comma-separated list, e.g. "cluster1,cluster2"',
    )
    parser.add_argument(
        '--before',
        dest='before_filter',
        metavar='DATE/TIME',
        nargs='?',
        type=date_time_parse,
        help=f'{action.capitalize()} runs created before specific time. Datetimes must be surrounded by \'\'. '
        'e.g 2023-01-01 or 01-13-2023 or 12:30:23.4 or \'01-13-2023 19:20:21.9\'',
    )
    parser.add_argument(
        '--after',
        dest='after_filter',
        metavar='DATE/TIME',
        nargs='?',
        type=date_time_parse,
        help=f'{action.capitalize()} runs created after specific time. Datetimes must be surrounded by \'\'. '
        'e.g 2023-01-01 or 01-13-2023 or 12:30:23.4 or \'01-13-2023 19:20:21.9\'',
    )
    parser.add_argument(
        '-t',
        '--gpu-type',
        dest='gpu_type_filter',
        metavar='GPU',
        default=None,
        type=comma_separated,
        help=f'{action.capitalize()} runs with specific GPU type. '
        'Multiple types should be specified using a comma-separated list, e.g. "a100_40gb,v100_16gb"',
    )
    parser.add_argument(
        '-n',
        '--gpu-num',
        dest='gpu_num_filter',
        metavar='# GPUs',
        default=None,
        type=functools.partial(comma_separated, fun=int),
        help=f'{action.capitalize()} runs with specific number of GPUs. '
        'Multiple values should be specified using a comma-separated list, e.g. "1,8"',
    )

    def status(value: str) -> List[RunStatus]:
        res = comma_separated(value, RunStatus.from_string)
        if res == [RunStatus.UNKNOWN] and value != [RunStatus.UNKNOWN.value]:
            raise TypeError(f'Unknown value {value}')
        return res

    parser.add_argument(
        '-s',
        '--status',
        dest='status_filter',
        default=None,
        metavar='STATUS',
        type=status,
        help=f'{action.capitalize()} runs with the specified statuses (choices: {", ".join(CLI_STATUS_OPTIONS)}). '
        'Multiple statuses should be specified using a comma-separated list, e.g. "failed,completed"',
    )

    if include_all:
        parser.add_argument(
            '-a',
            '--all',
            dest=f'{action}_all',
            action='store_true',
            help=f'{action} all runs',
        )


def _split_glob_filters(filters: List[str]) -> Tuple[List[str], List[str]]:
    """Split a list of filters into glob-containing and non-glob-containing filters
    """

    globbers: List[str] = []
    non_globbers: Optional[List[str]] = []
    for f in filters:
        if is_glob(f):
            globbers.append(f)
        else:
            non_globbers.append(f)

    return globbers, non_globbers


def get_runs_with_filters(
    name_filter: Optional[List[str]] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[RunStatus]] = None,
    action_all: Optional[bool] = None,
) -> List[Run]:

    filter_used = any(
        [name_filter, before_filter, after_filter, cluster_filter, gpu_type_filter, gpu_num_filter, status_filter])
    if not filter_used:
        if action_all is False:
            raise MCLIException('Must specify at least one filter or --all')

    if not name_filter:
        # Accept all that pass other filters
        name_filter = []

    conf = MCLIConfig.load_config()

    # Use get_runs only for the non-glob names provided
    glob_filters, run_names = _split_glob_filters(name_filter)
    if not conf.feature_enabled(FeatureFlag.USE_MCLOUD) and not conf.clusters:
        raise MCLIException('No clusters found. You must have at least 1 cluster added before working with runs.')

    with console.status('Retrieving requested runs...'):
        runs = get_runs(
            runs=(run_names or None) if not glob_filters else None,
            clusters=cluster_filter,
            before=before_filter,
            after=after_filter,
            gpu_types=gpu_type_filter,
            gpu_nums=gpu_num_filter,
            statuses=status_filter,
            timeout=None,
        )

    if glob_filters:
        found_runs: Dict[str, Run] = {r.name: r for r in runs}

        # Any globs will be handled by additional client-side filtering
        filtered = set()
        for pattern in glob_filters:
            for match in fnmatch.filter(found_runs, pattern):
                filtered.add(match)

        expected_names = set(run_names)
        for run_name in found_runs:
            if run_name in expected_names:
                filtered.add(run_name)

        runs = list(found_runs[r] for r in filtered)

    return runs
