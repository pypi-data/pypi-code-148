# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CompoundButton(Component):
    """A CompoundButton component.
A compound button is a button with an additional slot for secondary textual content.
Since both primary and secondary textual contents are part of a compound button's name they should be kept concise.
### Layout
- For dialog boxes and panels, where people are moving through a sequence of screens,
  right-align buttons with the container.
- For single-page forms and focused tasks, left-align buttons with the container.
- Always place the primary button on the left, the secondary button just to the right of it.
- Show only one primary button that inherits theme color at rest state. If there are more
  than two buttons with equal priority, all buttons should have neutral backgrounds.
- Don't use a button to navigate to another place; use a link instead. The exception
  is in a wizard where "Back" and "Next" buttons may be used.
- Don't place the default focus on a button that destroys data. Instead, place the
  default focus on the button that performs the "safe act" and retains the content
  (such as "Save") or cancels the action (such as "Cancel").
### Content
- Use sentence-style capitalization—only capitalize the first word.
- Make sure it's clear what will happen when people interact with the button.
  Be concise; usually a single verb is best. Include a noun if there is any room
  for interpretation about what the verb means. For example, "Delete folder" or "Create account".

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- appearance (a value equal to: 'subtle', 'outline', 'secondary', 'primary', 'transparent'; optional):
    A button can have its content and borders styled for greater
    emphasis or to be subtle.   - 'secondary' (default): Gives
    emphasis to the button in such a way that it indicates a secondary
    action.  - 'primary': Emphasizes the button as a primary action.
    - 'outline': Removes background styling.  - 'subtle': Minimizes
    emphasis to blend into the background until hovered or focused.  -
    'transparent': Removes background and border styling.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- disabled (boolean; optional):
    Disabled state of button.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- secondary_content (string; optional):
    Second line of text that describes the action this button takes.

- shape (a value equal to: 'circular', 'square', 'rounded'; optional):
    A button can be rounded, circular, or square.

- size (a value equal to: 'small', 'medium', 'large'; optional):
    A button supports different sizes.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'CompoundButton'
    @_explicitize_args
    def __init__(self, children=None, secondary_content=Component.UNDEFINED, appearance=Component.UNDEFINED, disabled=Component.UNDEFINED, shape=Component.UNDEFINED, size=Component.UNDEFINED, n_clicks=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'appearance', 'class_name', 'disabled', 'key', 'n_clicks', 'secondary_content', 'shape', 'size', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'appearance', 'class_name', 'disabled', 'key', 'n_clicks', 'secondary_content', 'shape', 'size', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(CompoundButton, self).__init__(children=children, **args)
