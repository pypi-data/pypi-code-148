import dataclasses
import typing
import timm
import irisml.core


class Task(irisml.core.TaskBase):
    """Create timm transforms."""
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        input_size: int
        crop_pct: float = 0.875  # Center crop the image with this ratio.
        interpolation: typing.Literal['bilinear', 'bicubic'] = 'bilinear'

    @dataclasses.dataclass
    class Outputs:
        train_transform: typing.Callable = None
        val_transform: typing.Callable = None

    class TimmTransform:
        def __init__(self, input_size, is_training, crop_pct, interpolation):
            self._input_size = input_size
            self._is_training = is_training
            self._crop_pct = crop_pct
            self._interpolation = interpolation
            self._transform = timm.data.create_transform(input_size, is_training, crop_pct=crop_pct, interpolation=interpolation, mean=0, std=1)

        def __call__(self, x):
            return self._transform(x)

        def __getstate__(self):
            return {'input_size': self._input_size, 'is_training': self._is_training, 'crop_pct': self._crop_pct, 'interpolation': self._interpolation}

        def __setstate__(self, state):
            self.__init__(**state)

    def execute(self, inputs):
        train_transform = Task.TimmTransform(self.config.input_size, is_training=True, crop_pct=self.config.crop_pct, interpolation=self.config.interpolation)
        val_transform = Task.TimmTransform(self.config.input_size, is_training=False, crop_pct=self.config.crop_pct, interpolation=self.config.interpolation)

        return self.Outputs(train_transform=train_transform, val_transform=val_transform)

    def dry_run(self, inputs):
        return self.execute(inputs)
