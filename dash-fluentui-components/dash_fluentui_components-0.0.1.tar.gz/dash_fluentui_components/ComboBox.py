# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ComboBox(Component):
    """A ComboBox component.
## Overview
A ComboBox is a list in which the selected item is always visible, and the others
are visible on demand by clicking a drop-down button or by typing in the input
(unless allowFreeform and autoComplete are both false). They are used to simplify
the design and make a choice within the UI. When closed, only the selected item is
visible. When users click the drop-down button, all the options become visible.
To change the value, users open the list and click another value or use the arrow
keys (up and down) to select a new value. When collapsed if autoComplete and/or
allowFreeform are true, the user can select a new value by typing.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- allow_freeform (boolean; default False):
    Whether the ComboBox is free form, meaning that the user input is
    not bound to provided options. Defaults to False.

- auto_complete (a value equal to: 'on', 'off'; default 'on'):
    Whether the ComboBox auto completes. As the user is inputting
    text, it will be suggested potential matches from the list of
    options. If the combo box is expanded, this will also scroll to
    the suggested option, and give it a selected style.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- disabled (boolean; default False):
    If True, the dropdown is disabled and can't be clicked on.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; optional):
    A label to be displayed above the dropdown component.

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

- multi (boolean; default False):
    If True, the user can select multiple values.

- options (list of dicts; optional):
    Configuration for individual choices within the choice group.

    `options` is a list of dicts with keys:

    - disabled (boolean; optional)

    - icon (string; optional)

    - label (string; required)

    - value (string | number; required)

- persist_menu (boolean; default False):
    Menu will not be created or destroyed when opened or closed,
    instead it will be hidden. This will improve perf of the menu
    opening but could potentially impact overall perf by having more
    elements in the dom. Should only be used when perf is important.
    Note: This may increase the amount of time it takes for the
    comboBox itself to mount.

- placeholder (string; optional):
    A string value to be displayed if no item is selected.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- use_combo_box_as_menu_width (boolean; default True):
    Whether to use the ComboBoxes width as the menu's width.

- value (string | number | list of strings | list of numbers; default ''):
    The value of the input. If `multi` is False (the default) then
    value is just a string that corresponds to the values provided in
    the `options` property. If `multi` is True, then multiple values
    can be selected at once, and `value` is an array of items with
    values corresponding to those in the `options` prop.

- virtualized (boolean; default False):
    If True, VirtualizedComboBox is used. Most useful when there are
    al lot of options to display."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'ComboBox'
    @_explicitize_args
    def __init__(self, disabled=Component.UNDEFINED, label=Component.UNDEFINED, placeholder=Component.UNDEFINED, value=Component.UNDEFINED, options=Component.UNDEFINED, multi=Component.UNDEFINED, virtualized=Component.UNDEFINED, allow_freeform=Component.UNDEFINED, auto_complete=Component.UNDEFINED, use_combo_box_as_menu_width=Component.UNDEFINED, persist_menu=Component.UNDEFINED, loading_state=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'allow_freeform', 'auto_complete', 'class_name', 'disabled', 'key', 'label', 'loading_state', 'multi', 'options', 'persist_menu', 'placeholder', 'style', 'use_combo_box_as_menu_width', 'value', 'virtualized']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'allow_freeform', 'auto_complete', 'class_name', 'disabled', 'key', 'label', 'loading_state', 'multi', 'options', 'persist_menu', 'placeholder', 'style', 'use_combo_box_as_menu_width', 'value', 'virtualized']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(ComboBox, self).__init__(**args)
