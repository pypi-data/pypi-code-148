# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Separator(Component):
    """A Separator component.
## Overview
A separator visually separates content into groups.
You can render content in the separator by specifying the component's children.
The component's children can be plain text or a component like Icon. The content
is center-aligned by default.

Keyword arguments:

- children (a list of or a singular dash component, string or number; required):
    The children of this component.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- align_content (a value equal to: 'start', 'center', 'end'; default 'center'):
    Where the content should be aligned in the separator.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- vertical (boolean; default False):
    Whether the content should be aligned vertically."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Separator'
    @_explicitize_args
    def __init__(self, children=None, align_content=Component.UNDEFINED, vertical=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'align_content', 'class_name', 'key', 'style', 'vertical']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'align_content', 'class_name', 'key', 'style', 'vertical']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(Separator, self).__init__(children=children, **args)
