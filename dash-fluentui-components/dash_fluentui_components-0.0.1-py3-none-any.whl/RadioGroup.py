# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class RadioGroup(Component):
    """A RadioGroup component.
RadioGroup lets people select a single option from two or more Radio items.
Use RadioGroup to present all available choices if there's enough space.
For more than 5 choices, consider using a different component such as Dropdown.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- disabled (boolean; default False):
    Disable all Radio items in this group.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; optional):
    A label to be displayed above the RadioGroup component.

- layout (a value equal to: 'horizontal', 'vertical', 'horizontal-stacked'; default 'vertical'):
    How the radio items are laid out in the group.

- options (list of dicts; optional):
    Configuration for individual choices within the radio group.

    `options` is a list of dicts with keys:

    - disabled (boolean; optional):
        denotes if radio is disabled.

    - label (string; required):
        The Radio's label.

    - value (string; required):
        The Radio's value.

- required (boolean; default False):
    Require a selection in this group.

- value (string; optional):
    The value of the input corresponds to the values provided in the
    `options` property."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'RadioGroup'
    @_explicitize_args
    def __init__(self, label=Component.UNDEFINED, value=Component.UNDEFINED, options=Component.UNDEFINED, layout=Component.UNDEFINED, disabled=Component.UNDEFINED, required=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'disabled', 'key', 'label', 'layout', 'options', 'required', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'disabled', 'key', 'label', 'layout', 'options', 'required', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(RadioGroup, self).__init__(**args)
