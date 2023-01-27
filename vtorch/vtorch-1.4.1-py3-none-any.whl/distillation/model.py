import transformers

from ..common.checks import ConfigurationError
from ..models.model import IModel


def reduce_base_model(
    model: IModel, reduction: int, layer_shift: int = 1, base_model_attr: str = "_base_model"
) -> IModel:
    """
    Parameters
    ----------
    model: IModel, teacher model
    reduction: the factor of reduction the children model's size
        (e.g with reduction=2 6-layer student would be initialized from the 12-layer teacher)
    layer_shift: int (default = 1) index shift of the corresponding layer when mapping from student
        layer to teacher layer, `teacher_layer_index = (student_layer_index * reduction) + layer_shift`.
        Must be in `0 <= layer_shift < reduction` range.
    base_model_attr: str (default = "_base_model") attribute of base model (e.g Transformer) whose
        parameters will be used for initialization
    """
    if layer_shift < 0 or layer_shift >= reduction:
        raise ConfigurationError(
            f"Layer shift must not be less than 0 or higher than reduction={reduction}. "
            f"You have got layer_shift={layer_shift}"
        )
    base_model = getattr(model, base_model_attr)
    base_model.config.num_hidden_layers = base_model.config.num_hidden_layers // reduction

    base_model_copy = getattr(transformers, base_model.__class__.__name__)(base_model.config)

    base_model_state_dict = base_model.state_dict()
    reduced_model_state_dict = base_model_copy.state_dict()

    for layer_id in reduced_model_state_dict.keys():
        # e.g "encoder.layer.4.attention.self.query.weight" -> "encoder.layer.9.attention.self.query.weight"
        base_layer_id = ".".join(
            str((int(substring) * reduction) + layer_shift) if substring.isdigit() else substring
            for substring in layer_id.split(".")
        )
        reduced_model_state_dict[layer_id] = base_model_state_dict[base_layer_id]

    base_model_copy.load_state_dict(reduced_model_state_dict)

    setattr(model, base_model_attr, base_model_copy)

    return model
