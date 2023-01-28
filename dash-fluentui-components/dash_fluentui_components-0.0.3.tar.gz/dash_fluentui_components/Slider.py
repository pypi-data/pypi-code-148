# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Slider(Component):
    """A Slider component.
A Slider represents an input that allows user to choose a value from within a specific range.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- disabled (boolean; default False):
    Optional flag to render the Slider as disabled.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; optional):
    Description label of the Slider.

- max (number; required):
    The max value of the Slider.

- min (number; required):
    The min value of the Slider.

- size (a value equal to: 'small', 'medium'; default 'medium'):
    The size of the Slider.

- step (number; optional):
    The difference between the two adjacent values of the Slider.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- value (number; optional):
    The initial value of the Slider.

- vertical (boolean; default False):
    Optional flag to render the slider vertically. Defaults to
    rendering horizontal."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Slider'
    @_explicitize_args
    def __init__(self, label=Component.UNDEFINED, value=Component.UNDEFINED, min=Component.REQUIRED, max=Component.REQUIRED, step=Component.UNDEFINED, vertical=Component.UNDEFINED, size=Component.UNDEFINED, disabled=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'class_name', 'disabled', 'key', 'label', 'max', 'min', 'size', 'step', 'style', 'value', 'vertical']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'class_name', 'disabled', 'key', 'label', 'max', 'min', 'size', 'step', 'style', 'value', 'vertical']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['max', 'min']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Slider, self).__init__(**args)
