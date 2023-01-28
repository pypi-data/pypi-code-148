# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Panel(Component):
    """A Panel component.
## Overview
Panels are modal UI overlays that provide contextual app information. They often
request some kind of creation or management action from the user. Panels are paired
with the Overlay component, also known as a Light Dismiss. The Overlay blocks
interactions with the app view until dismissed either through clicking or tapping
on the Overlay or by selecting a close or completion action within the Panel.
### Examples of experiences that use Panels
- Member or group list creation or management
- Document list creation or management
- Permissions creation or management
- Settings creation or management
- Multi-field forms

Keyword arguments:

- children (a list of or a singular dash component, string or number; required):
    The content of the panel.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- header_text (string; default ''):
    Header text for the Panel.

- is_open (boolean; required):
    Whether the panel is displayed. If True, will cause panel to stay
    open even if dismissed. If False, will cause panel to stay hidden.
    If undefined, will allow the panel to control its own visibility
    through open/dismiss methods.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; default 'Open panel'):
    Text inside the button to trigger the panel.

- light_dismiss (boolean; default False):
    Whether the panel can be light dismissed by clicking outside the
    panel.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- type (a value equal to: 'small', 'medium', 'large'; default 'small'):
    Type of the panel determines its size."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Panel'
    @_explicitize_args
    def __init__(self, children=None, type=Component.UNDEFINED, is_open=Component.REQUIRED, label=Component.UNDEFINED, header_text=Component.UNDEFINED, light_dismiss=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'class_name', 'header_text', 'is_open', 'key', 'label', 'light_dismiss', 'style', 'type']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'class_name', 'header_text', 'is_open', 'key', 'label', 'light_dismiss', 'style', 'type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['is_open']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(Panel, self).__init__(children=children, **args)
