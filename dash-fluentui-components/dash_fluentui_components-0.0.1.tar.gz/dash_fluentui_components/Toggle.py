# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Toggle(Component):
    """A Toggle component.
## Overview
Toggles represent a physical switch that allows users to turn things on or off.
Use Toggles to present users with two mutually exclusive options (like on/off),
where choosing an option results in an immediate action. Use a Toggle for binary
operations that take effect right after the user flips the Toggle. For example,
use a Toggle to turn services or hardware components on or off. In other words,
if a physical switch would work for the action, a Toggle is probably the best control to use.
### Choosing between Toggle and Checkbox
For some actions, either a Toggle or a Checkbox might work. To decide which control
would work better, follow these tips:
- Use a Toggle for binary settings when changes become effective immediately after the user changes them.
- In the above example, it's clear with the Toggle that the wireless is set to "On." But with the Checkbox, the user needs to think about whether the wireless is on now or whether they need to check the box to turn wireless on.
- Use a Checkbox when the user has to perform extra steps for changes to be effective. For example, if the user must click a "Submit", "Next", "Ok" button to apply changes, use a Checkbox.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- disabled (boolean; default False):
    If True, the toggle is disabled and can't be clicked on.

- inline_label (boolean; default False):
    Whether the label (not the onText/offText) should be positioned
    inline with the toggle control. Left (right in RTL) side when
    on/off text provided VS right (left in RTL) side when no on/off
    text.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; default ''):
    A label to be displayed along with the toggle component.

- off_text (string; default 'Off'):
    Text to display when toggle is OOF. Caution: when not providing
    on/off text user may get confused in differentiating the on/off
    states of the toggle. Defaults to `off`.

- on_text (string; default 'On'):
    Text to display when toggle is ON. Caution: when not providing
    on/off text user may get confused in differentiating the on/off
    states of the toggle. Defaults to `on`.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- toggled (boolean; default False):
    Checked state of the toggle."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Toggle'
    @_explicitize_args
    def __init__(self, label=Component.UNDEFINED, toggled=Component.UNDEFINED, on_text=Component.UNDEFINED, off_text=Component.UNDEFINED, disabled=Component.UNDEFINED, inline_label=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'class_name', 'disabled', 'inline_label', 'key', 'label', 'off_text', 'on_text', 'style', 'toggled']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'class_name', 'disabled', 'inline_label', 'key', 'label', 'off_text', 'on_text', 'style', 'toggled']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Toggle, self).__init__(**args)
