# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Card(Component):
    """A Card component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- appearance (a value equal to: 'filled', 'subtle', 'outline', 'filled-alternative'; default 'filled'):
    Sets the appearance of the card. - \"filled\": The card will have
    a shadow, border and background color. - \"filled-alternative\":
    This appearance is similar to filled, but the background color
    will be a little darker. - \"outline\": This appearance is similar
    to filled, but the background color will be transparent and no
    shadow applied. - \"subtle\": This appearance is similar to
    filled-alternative, but no border is applied.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

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

- orientation (a value equal to: 'horizontal', 'vertical'; default 'vertical'):
    Defines the orientation of the card.

- selected (boolean; default False):
    Defines the controlled selected state of the card.

- show_loading (boolean; optional):
    Denotes wether a loading bar should be displayed when content is
    loading.

- size (a value equal to: 'small', 'medium', 'large'; default 'medium'):
    Controls the card's border radius and padding between inner
    elements.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Card'
    @_explicitize_args
    def __init__(self, children=None, appearance=Component.UNDEFINED, orientation=Component.UNDEFINED, size=Component.UNDEFINED, selected=Component.UNDEFINED, show_loading=Component.UNDEFINED, loading_state=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'appearance', 'class_name', 'key', 'loading_state', 'orientation', 'selected', 'show_loading', 'size', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'appearance', 'class_name', 'key', 'loading_state', 'orientation', 'selected', 'show_loading', 'size', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Card, self).__init__(children=children, **args)
