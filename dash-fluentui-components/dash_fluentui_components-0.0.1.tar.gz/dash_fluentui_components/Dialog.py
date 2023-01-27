# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dialog(Component):
    """A Dialog component.
`Dialog` is a window overlaid on either the primary window or another dialog window. Windows
under a modal dialog are inert. That is, users cannot interact with content outside an active
dialog window. Inert content outside an active dialog is typically visually obscured or
dimmed so it is difficult to discern, and in some implementations, attempts to interact
with the inert content cause the dialog to close.
### Do
- Dialog boxes consist of a header (`DialogTitle`), content (`DialogSurface`), and footer (`DialogActions`),
  which should all be included inside a body (DialogBody).
- Validate that people’s entries are acceptable before closing the dialog. Show an inline validation error
  near the field they must correct.
- Modal dialogs should be used very sparingly—only when it’s critical that people make a choice or provide
  information before they can proceed. Thee dialogs are generally used for irreversible or potentially
  destructive tasks. They’re typically paired with an backdrop without a light dismiss.
- Add a aria-describedby attribute on DialogSurface pointing to the dialog content on short confirmation like dialogs.
### Don't
- Don't use more than three buttons between `DialogActions`.
- Don't open a `Dialog` from a `Dialog`
- Don't use a `Dialog` with no focusable elements

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Can contain two children including  {@link  DialogTrigger  }  and
    {@link  DialogSurface  } . Alternatively can only contain  {@link
    DialogSurface  }  if using trigger outside dialog, or controlling
    state.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- actions (a list of or a singular dash component, string or number; optional)

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- modal_type (a value equal to: 'alert', 'modal', 'non-modal'; default 'modal'):
    Dialog variations.  - `modal`: When this type of dialog is open,
    the rest of the page is dimmed out and cannot be interacted with.
    The tab sequence is kept within the dialog and moving the focus
    outside the dialog will imply closing it.   This is the default
    type of the component. - `non-modal`: When a non-modal dialog is
    open, the rest of the page is not dimmed out and users can
    interact   with the rest of the page. This also implies that the
    tab focus can move outside the dialog when it reaches   the last
    focusable element. - `alert`: is a special type of modal dialogs
    that interrupts the user's workflow to communicate an important
    message or ask for a decision. Unlike a typical modal dialog, the
    user must take an action through the   options given to dismiss
    the dialog, and it cannot be dismissed through the dimmed
    background or escape key.

- open (boolean; default False):
    Controls the open state of the dialog.

- title (a list of or a singular dash component, string or number; optional):
    Title displayed in the Dialog header.

- trigger (a list of or a singular dash component, string or number; optional):
    Usually a button component o.a. If the state is not controlled
    (externally managed), clicking this component will open the
    dialog. This component will also be rendered when the dialog is
    not open.

- trigger_action (a list of or a singular dash component, string or number; optional)"""
    _children_props = ['title', 'trigger', 'actions', 'trigger_action']
    _base_nodes = ['title', 'trigger', 'actions', 'trigger_action', 'children']
    _namespace = 'dash_fluentui_components'
    _type = 'Dialog'
    @_explicitize_args
    def __init__(self, children=None, title=Component.UNDEFINED, trigger=Component.UNDEFINED, actions=Component.UNDEFINED, trigger_action=Component.UNDEFINED, modal_type=Component.UNDEFINED, open=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'actions', 'key', 'modal_type', 'open', 'title', 'trigger', 'trigger_action']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'actions', 'key', 'modal_type', 'open', 'title', 'trigger', 'trigger_action']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Dialog, self).__init__(children=children, **args)
