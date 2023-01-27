# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Modal(Component):
    """A Modal component.
## Overview
Modals are temporary, modal UI overlay that generally provide contextual app information
or require user confirmation/input, or can be used to advertise new app features.
In some cases, Modals block interactions with the web page or application until being
explicitly dismissed. They can be used for lightweight creation or edit tasks and simple
management tasks, or for hosting heavier temporary content.
For usage requiring a quick choice from the user, Dialog may be a more appropriate control.

Keyword arguments:

- children (a list of or a singular dash component, string or number; required):
    The children of this component.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- is_blocking (boolean; default False):
    Whether the dialog can be light dismissed by clicking outside the
    dialog (on the overlay).

- is_draggable (boolean; default False):
    Whether modal can be dragged.

- is_open (boolean; default False):
    Whether modal is currently open.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Modal'
    @_explicitize_args
    def __init__(self, children=None, is_open=Component.UNDEFINED, is_draggable=Component.UNDEFINED, is_blocking=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'class_name', 'is_blocking', 'is_draggable', 'is_open', 'key', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'class_name', 'is_blocking', 'is_draggable', 'is_open', 'key', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(Modal, self).__init__(children=children, **args)
