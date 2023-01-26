"""Implementation of mcli describe run"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Generator, List, Optional, Tuple

from rich.table import Table

from mcli.api.exceptions import KubernetesException, MAPIException
from mcli.cli.m_get.display import (MCLIDisplayItem, MCLIGetDisplay, OutputDisplay, create_vertical_display_table,
                                    format_timestamp)
from mcli.config import MESSAGE, MCLIConfigError
from mcli.sdk import Run, get_runs
from mcli.utils.utils_logging import FAIL

logger = logging.getLogger(__name__)


class DescribeRunColumns(Enum):
    NAME = 'name'
    CLUSTER = 'cluster'
    GPU_TYPE = 'gpu_type'
    GPU_NUM = 'gpu_num'
    IMAGE = 'image'
    CREATED_TIME = 'created_time'
    START_TIME = 'start_time'
    END_TIME = 'end_time'
    STATUS = 'status'


@dataclass
class DescribeRunDisplayItem(MCLIDisplayItem):
    """Tuple that extracts detailed run data for display purposes"""
    name: str
    gpu_num: str
    created_time: str
    start_time: str
    end_time: str
    status: str
    image: str
    cluster: Optional[str] = None
    gpu_type: Optional[str] = None

    @classmethod
    def from_run(cls, run: Run) -> DescribeRunDisplayItem:
        extracted: Dict[str, str] = {
            DescribeRunColumns.NAME.value: run.name,
            DescribeRunColumns.CLUSTER.value: run.config.cluster,
            DescribeRunColumns.GPU_TYPE.value: run.config.gpu_type,
            DescribeRunColumns.GPU_NUM.value: str(run.config.gpu_num),
            DescribeRunColumns.IMAGE.value: run.config.image,
            DescribeRunColumns.CREATED_TIME.value: format_timestamp(run.created_at),
            DescribeRunColumns.START_TIME.value: format_timestamp(run.started_at),
            DescribeRunColumns.END_TIME.value: format_timestamp(run.completed_at),
            DescribeRunColumns.STATUS.value: run.status.display_name,
        }
        return DescribeRunDisplayItem(**extracted)


class MCLIDescribeRunDisplay(MCLIGetDisplay):
    """ Display manager for describe run """

    def __init__(self, models: List[Run]):
        self.models = sorted(models, key=lambda x: x.created_at, reverse=True)

    @property
    def index_label(self) -> str:
        return ""

    def create_custom_table(self, columns: List[str], data: List[Tuple[Any, ...]]) -> Optional[Table]:
        return create_vertical_display_table(data=data, columns=[s.upper() for s in columns])

    def __iter__(self) -> Generator[DescribeRunDisplayItem, None, None]:
        for model in self.models:
            item = DescribeRunDisplayItem.from_run(model)
            yield item


def describe_run(run_name: str, output: OutputDisplay = OutputDisplay.TABLE, **kwargs):
    """
    Fetches more details of a Run
    """
    del kwargs

    runs: List[Run] = []
    try:
        runs = get_runs(runs=[run_name], timeout=None)
    except (KubernetesException, MAPIException, RuntimeError) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)

    if len(runs) == 0:
        logger.error(f'No runs found for name: {run_name}')
        return

    run: Run = runs[0]
    display = MCLIDescribeRunDisplay([run])
    display.print(output)
