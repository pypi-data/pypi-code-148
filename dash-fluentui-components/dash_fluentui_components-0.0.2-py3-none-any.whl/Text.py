# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Text(Component):
    """A Text component.
Typography and styling abstraction component used to ensure
consistency and standardize text throughout your application.
### Do
- Use Text whenever you need to display stylized text
- Use Text to display read-only text

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- align (a value equal to: 'center', 'start', 'end', 'justify'; default 'start'):
    Aligns text based on the parent container.

- block (boolean; default False):
    Applies a block display for the content.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- italic (boolean; default False):
    Applies the italic font style to the content.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- size (a value equal to: 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000; default 300):
    Applies font size and line height based on the theme tokens.

- strikethrough (boolean; default False):
    Applies the strikethrough text decoration to the content.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- truncate (boolean; default False):
    Truncate overflowing text for block displays.

- underline (boolean; default False):
    Applies the underline text decoration to the content.

- weight (a value equal to: 'medium', 'regular', 'semibold', 'bold'; default 'regular'):
    Applies font weight to the content.

- wrap (boolean; default True):
    Applies the underline text decoration to the content."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Text'
    @_explicitize_args
    def __init__(self, children=None, align=Component.UNDEFINED, block=Component.UNDEFINED, italic=Component.UNDEFINED, size=Component.UNDEFINED, strikethrough=Component.UNDEFINED, truncate=Component.UNDEFINED, underline=Component.UNDEFINED, weight=Component.UNDEFINED, wrap=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'align', 'block', 'class_name', 'italic', 'key', 'size', 'strikethrough', 'style', 'truncate', 'underline', 'weight', 'wrap']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'align', 'block', 'class_name', 'italic', 'key', 'size', 'strikethrough', 'style', 'truncate', 'underline', 'weight', 'wrap']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Text, self).__init__(children=children, **args)
