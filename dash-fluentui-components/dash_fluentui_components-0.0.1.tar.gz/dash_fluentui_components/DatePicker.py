# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DatePicker(Component):
    """A DatePicker component.
## Overview
The DatePicker component enables a user to pick a date value.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- allow_text_input (boolean; default False):
    Whether the DatePicker allows input a date string directly or not.

- borderless (boolean; default False):
    Determines if DatePicker has a border.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- date (string; optional):
    Specifies the starting date for the component, best practice is to
    pass value via datetime object.

- disabled (boolean; default False):
    If True, no dates can be selected.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; default ''):
    Text displayed inside the button.

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

- max_date_allowed (string; optional):
    Specifies the highest selectable date for the component. Accepts
    datetime.datetime objects or strings in the format 'YYYY-MM-DD'.

- min_date_allowed (string; optional):
    Specifies the lowest selectable date for the component. Accepts
    datetime.datetime objects or strings in the format 'YYYY-MM-DD'.

- placeholder (string; default 'Select date.'):
    A string value to be displayed if no date is selected.

- show_month_picker (boolean; default True):
    Whether the month picker is shown beside the day picker or hidden.

- show_week_numbers (boolean; default False):
    Whether the calendar should show the week number (weeks 1 to 53)
    before each week row.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'DatePicker'
    @_explicitize_args
    def __init__(self, label=Component.UNDEFINED, date=Component.UNDEFINED, placeholder=Component.UNDEFINED, disabled=Component.UNDEFINED, min_date_allowed=Component.UNDEFINED, max_date_allowed=Component.UNDEFINED, show_week_numbers=Component.UNDEFINED, show_month_picker=Component.UNDEFINED, allow_text_input=Component.UNDEFINED, borderless=Component.UNDEFINED, loading_state=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'allow_text_input', 'borderless', 'class_name', 'date', 'disabled', 'key', 'label', 'loading_state', 'max_date_allowed', 'min_date_allowed', 'placeholder', 'show_month_picker', 'show_week_numbers', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'allow_text_input', 'borderless', 'class_name', 'date', 'disabled', 'key', 'label', 'loading_state', 'max_date_allowed', 'min_date_allowed', 'placeholder', 'show_month_picker', 'show_week_numbers', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DatePicker, self).__init__(**args)
