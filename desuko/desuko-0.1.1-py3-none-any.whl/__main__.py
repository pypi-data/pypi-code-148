"""Desuko - An extensible Discord bot, written in Python & Pycord.

## How is it structured?
Desuko aims to be modular. It has a base package implemented here and modules
to extend its functionality.

To make changes into Desuko code, please, make sure that your edits will **not** break
any existing modules.
"""
import logging
import sys
from importlib import import_module
from pathlib import Path

from yaml import safe_load

from desuko.bot import DesukoBot

BASE_DIR = Path(__file__).parent.parent

logging.basicConfig(
    format='%(asctime)23s | %(levelname)8s | %(message)s',
    level=logging.INFO,
)
logging.getLogger('discord').setLevel(logging.WARNING)

try:
    with open(BASE_DIR / 'desuko.yaml', 'rb') as yaml_f:
        CONFIG = safe_load(yaml_f)

    if CONFIG.get('config_file'):
        logging.info('Found configuration re-direct')
        with open(BASE_DIR / CONFIG['config_file'], 'rb') as yaml_f:
            CONFIG = safe_load(yaml_f)
except IOError:
    logging.critical('Failed to load Desuko configuration. Abort.')
    sys.exit(1)


def load_module(import_path: str) -> dict:
    """Load a Desuko Python module.

    Args:
        import_path (str): Import path of a module (e.g. `desuko_foo_bar`)

    Returns:
        dict: Information about the module

    Raises:
        AttributeError: One of Desuko modules miss required functions
        ModuleNotFoundError: Configuration requires non-existing modules
    """
    try:
        module = import_module(import_path)
        return {
            module.__NAME__: {
                'desc': module.__DESC__,
                'version': getattr(module, '__VERSION__', 'Stable'),
                'config': CONFIG['modules'][import_path],
                'class': module.Module,
                'import_path': import_path,
            },
        }
    except (AttributeError, ModuleNotFoundError) as exc:
        if CONFIG.get('silence_import_exceptions'):
            logging.critical('Unable to import %s. Abort.', import_path)
            sys.exit(1)

        raise exc


modules = {}
for module_import_path in CONFIG['modules'].keys():
    modules.update(load_module(module_import_path))

logging.warning('Loaded %d modules', len(modules))

DesukoBot(CONFIG, modules).run()
