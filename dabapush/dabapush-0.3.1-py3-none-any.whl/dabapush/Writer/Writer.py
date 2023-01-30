import abc
from typing import Generator
from ..Configuration.WriterConfiguration import WriterConfiguration


class Writer(object):
    """ """

    def __init__(self, config: WriterConfiguration):
        super().__init__()

        self.config = config
        self.buffer = []

    def __del__(self):
        # flush buffer before destruction
        self.persist()

    def write(self, queue: Generator[any, any, any]) -> None:
        """

        Parameters
        ----------
        queue :
            queue: Generator[any, any, any] : Items to be consumed.

        Returns
        -------
        type : None
        """
        for item in queue:
            self.buffer.append(item)
            if len(self.buffer) >= self.config.chunk_size:
                self.persist()

    @abc.abstractmethod
    def persist(self) -> None:
        """ """
        pass

    @property
    def name(self):
        """ """
        return self.config.name

    @property
    def id(self):
        """ """
        return self.config.id
