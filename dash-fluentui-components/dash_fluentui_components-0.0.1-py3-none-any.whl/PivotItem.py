# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class PivotItem(Component):
    """A PivotItem component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; required):
    Array that holds PivotItem components.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- value (string | list of strings; required):
    Value corresponding to keys in parent pivot element."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'PivotItem'
    @_explicitize_args
    def __init__(self, children=None, value=Component.REQUIRED, id=Component.UNDEFINED, key=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'key', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'key', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['value']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(PivotItem, self).__init__(children=children, **args)
