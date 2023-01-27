# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dropdown(Component):
    """A Dropdown component.
## Overview
A Dropdown is a list in which the selected item is always visible, and the others are visible
on demand by clicking a drop-down button. They are used to simplify the design and make a
choice within the UI. When closed, only the selected item is visible. When users click
the drop-down button, all the options become visible. To change the value, users open the
list and click another value or use the arrow keys (up and down) to select a new value.

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
    Choices to be displayed in the dropdown control. Each item mus
    have either set of keys [`label`, `value`] or [`key`, `text`]. The
    former is available to accept options consistent with Dash's build
    in Dropdown control, while the latter keys are according to the
    underlying UI fabric component. Additionally, a `disabled` and
    `icon` can be optionally passed. The `icon` property must
    correspond to the name of a Fabric icon:
    https://developer.microsoft.com/en-us/fabric#/styles/web/icons.

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
    The value of the input. If `multi` is False (the default) then
    value is just a string that corresponds to the values provided in
    the `options` property. If `multi` is True, then multiple values
    can be selected at once, and `value` is an array of items with
    values corresponding to those in the `options` prop."""
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
