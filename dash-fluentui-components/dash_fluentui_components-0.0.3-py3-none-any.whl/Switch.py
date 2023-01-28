# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Switch(Component):
    """A Switch component.
A switch represents a physical switch that allows someone to choose between two mutually exclusive options.
For example, "On/Off" and "Show/Hide". Choosing an option should produce an immediate result.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- checked (boolean; default False):
    Checked state of the toggle.

- disabled (boolean; default False):
    If True, the switch is disabled and can't be clicked on.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; default ''):
    A label to be displayed along with the toggle component.

- label_postion (a value equal to: 'before', 'after', 'above'; required):
    The position of the label relative to the Switch."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Switch'
    @_explicitize_args
    def __init__(self, label=Component.UNDEFINED, checked=Component.UNDEFINED, label_postion=Component.REQUIRED, disabled=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'checked', 'disabled', 'key', 'label', 'label_postion']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'checked', 'disabled', 'key', 'label', 'label_postion']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['label_postion']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Switch, self).__init__(**args)
