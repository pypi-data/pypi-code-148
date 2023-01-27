# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ToggleSlider(Component):
    """A ToggleSlider component.


Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- checked (boolean; required)

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; required)

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- tooltip (string; required)

- value (number; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'ToggleSlider'
    @_explicitize_args
    def __init__(self, tooltip=Component.REQUIRED, label=Component.REQUIRED, value=Component.REQUIRED, checked=Component.REQUIRED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'checked', 'class_name', 'key', 'label', 'style', 'tooltip', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'checked', 'class_name', 'key', 'label', 'style', 'tooltip', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['checked', 'label', 'tooltip', 'value']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ToggleSlider, self).__init__(**args)
