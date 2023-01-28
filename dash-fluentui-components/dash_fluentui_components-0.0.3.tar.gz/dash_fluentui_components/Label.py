# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Label(Component):
    """A Label component.
A label provides a name or title for an input.

Keyword arguments:

- children (a list of or a singular dash component, string or number; required)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- disabled (boolean; default False):
    Renders the label as disabled.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- required (boolean; default False):
    Displays an indicator that the label is for a required field.

- size (a value equal to: 'small', 'medium', 'large'; default 'medium'):
    A label supports different sizes.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- weight (a value equal to: 'regular', 'semibold'; default 'regular'):
    A label supports regular and semibold fontweight."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Label'
    @_explicitize_args
    def __init__(self, children=None, disabled=Component.UNDEFINED, required=Component.UNDEFINED, size=Component.UNDEFINED, weight=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'class_name', 'disabled', 'key', 'required', 'size', 'style', 'weight']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'class_name', 'disabled', 'key', 'required', 'size', 'style', 'weight']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(Label, self).__init__(children=children, **args)
