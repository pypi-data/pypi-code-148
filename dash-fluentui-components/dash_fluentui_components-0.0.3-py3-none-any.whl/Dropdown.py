# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dropdown(Component):
    """A Dropdown component.
A Dropdown is a selection component composed of a button and a list of options.
The button displays the current selected item or a placeholder, and the list is
visible on demand by clicking the button. Dropdowns are typically used in forms.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- appearance (a value equal to: 'outline', 'underline', 'filled-darker', 'filled-lighter'; default 'outline'):
    Controls the colors and borders of the combobox trigger.

- disabled (boolean; default False):
    If True, the dropdown is disabled and can't be clicked on.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; optional):
    A label to be displayed above the dropdown component.

- multiselect (boolean; default False):
    If True, the user can select multiple values.

- options (list of dicts; optional):
    Choices to be displayed in the dropdown control.

    `options` is a list of dicts with keys:

    - disabled (boolean; optional):
        denotes if radio is disabled.

    - label (string; required):
        The Radio's label.

    - value (string; required):
        The Radio's value.

- placeholder (string; optional):
    A string value to be displayed if no item is selected.

- size (a value equal to: 'small', 'medium', 'large'; default 'medium'):
    Controls the size of the combobox faceplate.

- value (list of strings; optional):
    The value of the input."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Dropdown'
    @_explicitize_args
    def __init__(self, label=Component.UNDEFINED, value=Component.UNDEFINED, multiselect=Component.UNDEFINED, options=Component.UNDEFINED, placeholder=Component.UNDEFINED, disabled=Component.UNDEFINED, size=Component.UNDEFINED, appearance=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'appearance', 'disabled', 'key', 'label', 'multiselect', 'options', 'placeholder', 'size', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'appearance', 'disabled', 'key', 'label', 'multiselect', 'options', 'placeholder', 'size', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Dropdown, self).__init__(**args)
