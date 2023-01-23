# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Connector(Component):
    """A Connector component.


Keyword arguments:

- id (string; required)

- color (string; default "#ccc")

- fill (string; default "none")

- is_input (boolean; default False)

- path_list (list of strings; optional)

- pos_list (list of list of numberss; optional)

- r (number; default 8)

- stroke (string; default "#ccc")

- strokeWidth (string; default "3")

- target_list (list of strings; optional)

- target_pl_list (list of list of list of numbersss; optional)

- x (number; default 100)

- y (number; default 100)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'bubble_train'
    _type = 'Connector'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, stroke=Component.UNDEFINED, strokeWidth=Component.UNDEFINED, fill=Component.UNDEFINED, x=Component.UNDEFINED, y=Component.UNDEFINED, r=Component.UNDEFINED, color=Component.UNDEFINED, pos_list=Component.UNDEFINED, path_list=Component.UNDEFINED, target_list=Component.UNDEFINED, target_pl_list=Component.UNDEFINED, is_input=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'color', 'fill', 'is_input', 'path_list', 'pos_list', 'r', 'stroke', 'strokeWidth', 'target_list', 'target_pl_list', 'x', 'y']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'color', 'fill', 'is_input', 'path_list', 'pos_list', 'r', 'stroke', 'strokeWidth', 'target_list', 'target_pl_list', 'x', 'y']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Connector, self).__init__(**args)
