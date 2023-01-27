# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MessageBar(Component):
    """A MessageBar component.
A MessageBar is an area at the top of a primary view that displays relevant status information.
You can use a MessageBar to tell the user about a situation that does not require their immediate
attention and therefore does not need to block other activities.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- is_multiline (boolean; default False):
    Denotes if the MessageBar contains multi-line text.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- message (string; default ''):
    The message to display in the message bar.

- show (boolean; default False):
    DEnotes wether the MessageBar should be visible or not.

- status (a value equal to: 'default', 'blocked', 'error', 'warning', 'success'; default 'default'):
    The severity of the message bar. Available options are: 'default',
    'blocked', 'error', 'warning', 'success'.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'MessageBar'
    @_explicitize_args
    def __init__(self, message=Component.UNDEFINED, status=Component.UNDEFINED, show=Component.UNDEFINED, is_multiline=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'class_name', 'is_multiline', 'key', 'message', 'show', 'status', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'class_name', 'is_multiline', 'key', 'message', 'show', 'status', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(MessageBar, self).__init__(**args)
