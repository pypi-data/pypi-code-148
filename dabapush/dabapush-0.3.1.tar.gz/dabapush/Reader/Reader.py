import abc
import ujson
from pathlib import Path
from typing import Generator
from loguru import logger as log
from ..Configuration.ReaderConfiguration import ReaderConfiguration


class Reader(abc.ABC):
    """Abstract base class for all reader plugins.

    **BEWARE**: readers and writers are never to be instanced directly by the user but rather will be obtain by calling
    `get_instance()` on their specific Configuration-counterparts.

    Attributes
    ----------
    config : ReaderConfiguration


    """

    def __init__(self, config: ReaderConfiguration):
        """
        Parameters
        ----------
        config : ReaderConfiguration
            Configuration file for the reader. In concrete classes it will be sub-class of ReaderConfiguration.
        """
        self.config = config
        # initialize file log
        if not Path(".dabapush/").exists():
            Path(".dabapush/").mkdir()

        self.log_path = Path(".dabapush/log.jsonl")

    @abc.abstractmethod
    def read(self) -> Generator[dict, None, None]:
        """Subclasses **must** implement this abstract method and implement their reading logic here.

        Returns
        -------
        type: Generator[dict, None, None]
            Generator which _should_ be one item per element.
        """
        return

    @property
    def files(self) -> Generator[Path, None, None]:
        fresh = Path(self.config.read_path).rglob(self.config.pattern)
        oldstock_dir = Path("./.dabapush")
        oldstock = []

        if oldstock_dir.exists() and (oldstock_dir / "log.jsonl").exists():
            with (oldstock_dir / "log.jsonl").open("r") as ff:
                oldstock = [ujson.loads(_) for _ in ff.readlines()]

        return (
            self._log(a)
            for a in (_ for _ in fresh if str(_) not in [f["file"] for f in oldstock])
        )

    # TODO: Move this functionality to Dabapush, it should manage waht has been done and what has not
    def _log(self, file: Path) -> Path:
        with self.log_path.open("a") as f:
            ujson.dump({"file": str(file), "status": "read"}, f)
            f.write("\n")
            log.debug(f"Done with {str(file)}")
        return file
