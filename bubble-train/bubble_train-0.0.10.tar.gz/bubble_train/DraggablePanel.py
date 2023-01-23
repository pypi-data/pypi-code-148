# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DraggablePanel(Component):
    """A DraggablePanel component.


Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers | a list of or a singular dash component, string or number; optional)

- id (string; required)

- cnt_h (string | number; default '100%')

- cx0 (number; default 0)

- cy0 (number; default 0)

- edge_offset (number; default 10)

- hdr_h (string | number; default 20)

- height (string; default '100px')

- in_dot_distance (number; default 20)

- in_dot_offset (number; default 10)

- input_ids (list of strings; optional)

- left (string; default '50px')

- out_dot_distance (number; default 20)

- out_dot_offset (number; default 10)

- output_ids (list of strings; optional)

- output_target_lists (list of list of stringss; optional)

- output_target_pl_lists (list of list of list of list of numberssss; optional)

- tooltip (string; optional)

- top (string; default '50px')

- width (string; default '100px')

- x0 (number; default 0)

- y0 (number; default 0)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'bubble_train'
    _type = 'DraggablePanel'
    @_explicitize_args
    def __init__(self, children=None, id=Component.REQUIRED, width=Component.UNDEFINED, height=Component.UNDEFINED, left=Component.UNDEFINED, top=Component.UNDEFINED, cx0=Component.UNDEFINED, cy0=Component.UNDEFINED, x0=Component.UNDEFINED, y0=Component.UNDEFINED, cnt_h=Component.UNDEFINED, hdr_h=Component.UNDEFINED, input_ids=Component.UNDEFINED, output_ids=Component.UNDEFINED, output_target_lists=Component.UNDEFINED, output_target_pl_lists=Component.UNDEFINED, in_dot_offset=Component.UNDEFINED, in_dot_distance=Component.UNDEFINED, out_dot_offset=Component.UNDEFINED, out_dot_distance=Component.UNDEFINED, edge_offset=Component.UNDEFINED, tooltip=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'cnt_h', 'cx0', 'cy0', 'edge_offset', 'hdr_h', 'height', 'in_dot_distance', 'in_dot_offset', 'input_ids', 'left', 'out_dot_distance', 'out_dot_offset', 'output_ids', 'output_target_lists', 'output_target_pl_lists', 'tooltip', 'top', 'width', 'x0', 'y0']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'cnt_h', 'cx0', 'cy0', 'edge_offset', 'hdr_h', 'height', 'in_dot_distance', 'in_dot_offset', 'input_ids', 'left', 'out_dot_distance', 'out_dot_offset', 'output_ids', 'output_target_lists', 'output_target_pl_lists', 'tooltip', 'top', 'width', 'x0', 'y0']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DraggablePanel, self).__init__(children=children, **args)
