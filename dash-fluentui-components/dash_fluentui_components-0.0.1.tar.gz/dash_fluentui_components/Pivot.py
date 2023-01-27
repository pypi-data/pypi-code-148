# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Pivot(Component):
    """A Pivot component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; required):
    Array that holds PivotItem components.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- loading_state (dict; required):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; required):
        Holds the name of the component that is loading.

    - is_loading (boolean; required):
        Determines if the component is loading or not.

    - prop_name (string; required):
        Holds which property is loading.

- options (list of dicts; required):
    Choices to be displayed in the pivot control.

    `options` is a list of dicts with keys:

    - disabled (boolean; optional)

    - icon (string; optional)

    - label (string; required)

    - value (string | number; required)

- selected_key (string; default ''):
    Currently selected key.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Pivot'
    @_explicitize_args
    def __init__(self, children=None, options=Component.REQUIRED, selected_key=Component.UNDEFINED, loading_state=Component.REQUIRED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'class_name', 'key', 'loading_state', 'options', 'selected_key', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'class_name', 'key', 'loading_state', 'options', 'selected_key', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['loading_state', 'options']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(Pivot, self).__init__(children=children, **args)
