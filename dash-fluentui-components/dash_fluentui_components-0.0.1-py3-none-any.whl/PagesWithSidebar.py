# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class PagesWithSidebar(Component):
    """A PagesWithSidebar component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Array of @link(Page) components.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- collapsed (boolean; default False):
    whether the Sidebar element is collapsed.

- collapsible (boolean; default False):
    whether the Sidebar element should be collapsible.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-render+er.

    `loading_state` is a dict with keys:

    - component_name (string; required):
        Holds the name of the component that is loading.

    - is_loading (boolean; required):
        Determines if the component is loading or not.

    - prop_name (string; required):
        Holds which property is loading.

- selected_key (string; optional):
    Key of the currently selected page item in navigation controls.

- sidebar_collapsed_width (number; default 80):
    width of the collapsed Sidebar element.

- sidebar_width (number; default 250):
    width of the PagesWithSidebar element."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'PagesWithSidebar'
    @_explicitize_args
    def __init__(self, children=None, selected_key=Component.UNDEFINED, collapsible=Component.UNDEFINED, collapsed=Component.UNDEFINED, sidebar_width=Component.UNDEFINED, sidebar_collapsed_width=Component.UNDEFINED, loading_state=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'collapsed', 'collapsible', 'key', 'loading_state', 'selected_key', 'sidebar_collapsed_width', 'sidebar_width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'collapsed', 'collapsible', 'key', 'loading_state', 'selected_key', 'sidebar_collapsed_width', 'sidebar_width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(PagesWithSidebar, self).__init__(children=children, **args)
