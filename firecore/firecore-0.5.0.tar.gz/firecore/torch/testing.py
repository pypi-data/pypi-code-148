import torch.distributed as dist
from firecore.system import find_free_port
from firecore.logging import get_logger


logger = get_logger(__name__)


def init_single_gloo_process_group():
    if not dist.is_available():
        logger.exception('pytorch distributed is not available')

    if not dist.is_initialized():
        dist.init_process_group(
            'GLOO',
            init_method="tcp://127.0.0.1:{}".format(find_free_port()),
            rank=0,
            world_size=1
        )
    else:
        logger.info('already initialized, reuse exsiting process group')
