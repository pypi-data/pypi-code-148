from pytatsu_tui import *

colorama.init()

os.chdir(Path(__file__).parent)

bm_dir().mkdir(0o755, exist_ok=True)

create_config()

nest_asyncio.apply()

__all__ = ["main"]
