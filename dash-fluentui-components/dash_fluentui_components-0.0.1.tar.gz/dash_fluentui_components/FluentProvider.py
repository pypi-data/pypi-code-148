# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FluentProvider(Component):
    """A FluentProvider component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; required):
    Array that holds PivotItem components.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- theme (a value equal to: 'light', 'dark', 'teamsLight', 'teamsDark'; default 'light')"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'FluentProvider'
    @_explicitize_args
    def __init__(self, children=None, theme=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'key', 'theme']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'key', 'theme']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(FluentProvider, self).__init__(children=children, **args)
