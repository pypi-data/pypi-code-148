import dataclasses
import typing
import timm
import torch
import irisml.core


class Task(irisml.core.TaskBase):
    """Create a timm model.

    To get a list of supported models, you can use timm.list_models() method. For the detail, please see the timm documents.
    ```
    import timm
    print(timm.list_models())
    ```
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass(frozen=True)
    class Config:
        name: str
        num_classes: int
        pretrained: bool = False
        task_type: typing.Literal['multiclass_classification', 'multilabel_classification'] = 'multiclass_classification'

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module = None

    class TimmModel(torch.nn.Module):
        def __init__(self, model_name: str, num_classes: int, task_type: str, state_dict: typing.Dict = None):
            super().__init__()
            self._model_name = model_name
            self._num_classes = num_classes
            self._task_type = task_type
            self._model = timm.create_model(model_name, pretrained=False, num_classes=num_classes)

            # Get mean and std values.
            default_cfg = getattr(self._model, 'default_cfg', {})
            mean_value = default_cfg.get('mean', timm.data.IMAGENET_DEFAULT_MEAN)
            std_value = default_cfg.get('std', timm.data.IMAGENET_DEFAULT_STD)
            assert len(mean_value) == 3 and len(std_value) == 3
            self.register_buffer('mean_value', torch.Tensor(mean_value).reshape((3, 1, 1)))
            self.register_buffer('std_value', torch.Tensor(std_value).reshape((3, 1, 1)))

            assert task_type in ('multiclass_classification', 'multilabel_classification')
            if task_type == 'multiclass_classification':
                self._criterion = torch.nn.CrossEntropyLoss()
                self._predictor = torch.nn.Softmax(1)
            elif task_type == 'multilabel_classification':
                self._criterion = torch.nn.BCEWithLogitsLoss()
                self._predictor = torch.nn.Sigmoid()

            if state_dict:
                self._model.load_state_dict(state_dict, strict=False)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self._model((x - self.mean_value) / self.std_value)

        @property
        def criterion(self):
            return self._criterion

        @property
        def predictor(self):
            return self._predictor

        def __getstate__(self):
            return {'model_name': self._model_name, 'num_classes': self._num_classes, 'task_type': self._task_type, 'state_dict': self._model.state_dict()}

        def __setstate__(self, state):
            self.__init__(**state)

    def execute(self, inputs):
        if self.config.pretrained:
            model = timm.create_model(self.config.name, pretrained=self.config.pretrained, num_classes=self.config.num_classes)
            state_dict = model.state_dict()
        else:
            state_dict = None

        return self.Outputs(Task.TimmModel(self.config.name, self.config.num_classes, self.config.task_type, state_dict))

    def dry_run(self, inputs):
        # Create a model without pretrained weights.
        return self.Outputs(Task.TimmModel(self.config.name, self.config.num_classes, self.config.task_type))
