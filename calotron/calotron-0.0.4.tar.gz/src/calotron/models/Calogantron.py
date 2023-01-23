import tensorflow as tf

from calotron.models.Calotron import Calotron
from calotron.models.Generator import Generator


class Calogantron(Calotron):
    def __init__(self, transformer, discriminator, generator):
        super().__init__(transformer, discriminator)
        if not isinstance(generator, Generator):
            raise TypeError(
                f"`generator` should be a calotron's "
                f"`Generator`, instead "
                f"{type(generator)} passed"
            )
        self._generator = generator

    def call(self, inputs):
        source, target = inputs
        output, d_output_true, d_output_pred = super().call(inputs)
        start_token = self.get_start_token(target)
        return output, d_output_true, d_output_pred, start_token

    def summary(self):
        self._transformer.summary()
        self._discriminator.summary()
        self._generator.summary()

    @property
    def generator(self) -> Generator:
        return self._generator
