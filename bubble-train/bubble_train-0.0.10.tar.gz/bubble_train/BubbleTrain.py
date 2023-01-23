# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class BubbleTrain(Component):
    """A BubbleTrain component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; default PropTypes.string.isRequired)

- height (string; default '100%')

- overflow (string; default 'auto')

- width (string; default '100%')"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'bubble_train'
    _type = 'BubbleTrain'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, overflow=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'height', 'overflow', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'height', 'overflow', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(BubbleTrain, self).__init__(**args)
