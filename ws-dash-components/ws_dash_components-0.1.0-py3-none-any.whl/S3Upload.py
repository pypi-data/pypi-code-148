# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class S3Upload(Component):
    """A S3Upload component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- files (dict with strings as keys and values of type dict; optional):
    The files being uploaded.

- label (string; default 'Drop files here or %{browse}'):
    A label that will be printed when this component is rendered.

- schema_id (string; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ws_dash_components'
    _type = 'S3Upload'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.UNDEFINED, schema_id=Component.REQUIRED, files=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'files', 'label', 'schema_id']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'files', 'label', 'schema_id']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['schema_id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(S3Upload, self).__init__(**args)
