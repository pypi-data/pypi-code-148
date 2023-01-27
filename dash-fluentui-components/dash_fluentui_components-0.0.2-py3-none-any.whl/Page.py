# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Page(Component):
    """A Page component.
A page within a multi page layout

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    child components.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- controls (a list of or a singular dash component, string or number; optional):
    child components.

- icon (a list of or a singular dash component, string or number; optional):
    Icon for display in page navigation.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; optional):
    Show clear button.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; required):
        Holds the name of the component that is loading.

    - is_loading (boolean; required):
        Determines if the component is loading or not.

    - prop_name (string; required):
        Holds which property is loading.

- page_key (string; optional):
    Show clear button.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    _children_props = ['controls', 'icon']
    _base_nodes = ['controls', 'icon', 'children']
    _namespace = 'dash_fluentui_components'
    _type = 'Page'
    @_explicitize_args
    def __init__(self, children=None, controls=Component.UNDEFINED, label=Component.UNDEFINED, page_key=Component.UNDEFINED, icon=Component.UNDEFINED, loading_state=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'class_name', 'controls', 'icon', 'key', 'label', 'loading_state', 'page_key', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'class_name', 'controls', 'icon', 'key', 'label', 'loading_state', 'page_key', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Page, self).__init__(children=children, **args)
