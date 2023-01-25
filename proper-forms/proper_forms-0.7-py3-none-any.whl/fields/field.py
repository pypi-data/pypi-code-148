from __future__ import annotations

import re
import typing as t
from uuid import uuid4

from markupsafe import Markup, escape_silent

from ..ftypes import type_boolean
from ..utils import get_html_attrs, render_error


__all__ = ("Field",)


REQUIRED = "required"
TYPE = "type"
MIN_NUM = "min_num"
MAX_NUM = "max_num"
INVALID = "Invalid value"
HARD_MAX_NUM = 1000

default_error_messages = {
    REQUIRED: "This field is required.",
    TYPE: "Invalid type.",
    MIN_NUM: "You need at least {num} values.",
    MAX_NUM: "You can have at most {num} values.",
}


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def in_(value, values):
    """Test if the value is in a list of values, or if the value as string is, or
    if the value is one of the values as strings.
    """
    ext_values = values + [str(val) for val in values]
    return value in ext_values or str(value) in ext_values


class Field:
    r"""

    Arguments are:

        *validators,

        name=None,
        required=False,
        strict=True,
        error_messages=None,

        prepare=None,
        clean=None,

        collection (bool):
            This field takes an open number of values of the same kind.
            For example, a list of comma separated tags or email addresses.

        sep (str):
            If `collection` is True, string to separate each value (default is ",").
            Ignored otherwise

        multiple=False,
        min_num=None,
        max_num=None,

        **extra

    """

    name: str = ""
    required: bool = False
    strict: bool = True
    multiple: bool = False
    min_num: int | None = None
    max_num: int | None = None
    collection: bool = False
    sep: str = ","
    input_type: str = "text"
    error: str | None = None
    error_value: t.Any = None
    updated: bool = False

    validators: t.Sequence[t.Callable]
    error_messages: dict
    custom_prepare: t.Callable | None
    custom_clean: t.Callable | None
    extra: dict[str, t.Any]

    input_values: list[t.Any] | None = None
    object_value: t.Any = None

    def __init__(
        self,
        *validators: t.Callable,
        name: str = "",
        required: bool = False,
        strict: bool = True,
        multiple: bool = False,
        min_num: int | None = None,
        max_num: int | None = None,
        collection: bool = False,
        sep: str = ",",
        error_messages: dict[str, str] | None = None,
        prepare: t.Callable | None = None,
        clean: t.Callable | None = None,
        **extra,
    ) -> None:
        self.validators = validators
        self.name = name
        self.required = required
        self.strict = strict
        self.min_num = min_num
        if max_num is not None:
            max_num = min(max_num, HARD_MAX_NUM)
        self.max_num = max_num

        self.collection = collection
        if collection:
            self.sep = sep
            multiple = False
        self.multiple = multiple

        self.error_messages = error_messages or {}
        self.custom_prepare = prepare
        self.custom_clean = clean
        self.extra = extra

        self.error = None
        self.input_values = None
        self.object_value = None

    def load_data(
        self,
        input_values: list[t.Any] | None = None,
        object_value: t.Any = None,
    ) -> None:
        self.input_values = input_values
        self.object_value = object_value

    @property
    def values(self) -> list[t.Any]:
        if self.input_values:
            return self.input_values
        if self.object_value:
            return (self.custom_prepare or self.prepare)(self.object_value)
        return []

    @property
    def value(self) -> t.Any:
        return self.values[0] if self.values else ""

    def get_value(self, index: int = 0) -> t.Any:
        if self.values and index < len(self.values):
            return self.values[index]
        return ""

    def prepare(self, object_value: t.Any) -> list[t.Any]:
        return [object_value]

    def validate(self) -> t.Any:
        self._reset()
        values = [str(value).strip() for value in self.input_values or []]

        if self.required and not values:
            self._set_error(REQUIRED)
            return None

        if not values:
            return None

        values = self._pre(values)
        pyvalues = self._typecast_values(values)
        if self.error:
            return None

        # Typecasting with `strict=False` could've emptied the values without erroring.
        # An empty string is only an error if the field is required
        if (not pyvalues or pyvalues[0] == "") and self.required:
            self._set_error(REQUIRED)
            return None

        self._validate_values(pyvalues)
        if self.error:
            return None

        pyvalue = self._post(pyvalues)
        if self.custom_clean:
            pyvalue = self.custom_clean(pyvalue)
        self.updated = pyvalue != self.object_value
        return pyvalue

    def type(self, value: t.Any, **kwargs) -> str:
        return str(value)

    def render_attrs(self, **attrs) -> Markup:
        html = get_html_attrs(attrs, show_error=bool(self.error))
        return Markup(html)

    def label(self, text: str, html: str = "", **attrs) -> str:
        text = escape_silent(str(text))
        attrs.setdefault("for", self.name)
        html_attrs = get_html_attrs(attrs, show_error=bool(self.error))
        if html:
            html = html + " "
        return "<label {}>{}{}</label>".format(html_attrs, html, text)

    def as_input(
        self,
        *,
        label: str | None = None,
        value_index: int = 0,
        **attrs,
    ) -> Markup:
        """Renders the field as a `<input type="text">` element, although the type
        can be changed.

        value_index (int):
            If `multiple` is True but the field display only one value,
            this is the index of the value that will be used.
            By default this is 0.
            If the list of values is not long enough, the value used is
            an empty string.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        value = self.get_value(value_index)
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        attrs.setdefault("type", self.input_type)
        attrs.setdefault("value", value)
        html_attrs = get_html_attrs(attrs, show_error=bool(self.error))

        html = "<input {}>".format(html_attrs)
        if label:
            kwargs = {"for": attrs.get("id", self.name)}
            html = self.label(label, **kwargs) + "\n" + html
        return Markup(html)

    def as_textarea(
        self,
        *,
        label: str | None = None,
        value_index: int = 0,
        **attrs,
    ) -> Markup:
        """Renders the field as a `<textarea>` tag.

        value_index (int):
            If `multiple` is True but the field display only one value,
            this is the index of the value that will be used.
            By default this is 0.
            If the list of values is not long enough, the value used is
            an empty string.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)

        value = attrs.pop("value", None) or self.get_value(value_index)
        html_attrs = get_html_attrs(attrs, show_error=bool(self.error))
        html = "<textarea {}>{}</textarea>".format(html_attrs, value)
        if label:
            kwargs = {"for": attrs.get("id", self.name)}
            html = self.label(label, **kwargs) + "\n" + html
        return Markup(html)

    def as_richtext(
        self,
        *,
        label: str | None = None,
        value_index: int = 0,
        **attrs,
    ) -> Markup:
        """Renders the field as a `<trix-editor>` tag with a matching
        hidden input file.

        Thi sonly render the tags, you must include the `trix.css` and `trix.js` files
        in the <head> of your page to make it a working rich-text editor
        (See https://github.com/basecamp/trix#getting-started).

        value_index (int):
            If `multiple` is True but the field display only one value,
            this is the index of the value that will be used.
            By default this is 0.
            If the list of values is not long enough, the value used is
            an empty string.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        name = attrs.pop("name", self.name)
        value = attrs.pop("value", None) or self.get_value(value_index)
        input_id = attrs.pop("id", str(uuid4()))

        attrs["input"] = input_id
        attrs.setdefault("required", self.required)
        attrs.setdefault("classes", "trix-content")
        if label:
            attrs["aria-labelledby"] = f"label-{input_id}"

        html_attrs = get_html_attrs(attrs, show_error=bool(self.error))
        html = "\n".join(
            [
                f'<input id="{input_id}" name="{name}" value="{value}" type="hidden">',
                f"<trix-editor {html_attrs}></trix-editor>",
            ]
        )
        if label:
            kw = {"id": f"label-{input_id}", "for": False}
            html = self.label(label, **kw) + "\n" + html
        return Markup(html)

    def as_checkbox(
        self,
        *,
        label: str | None = None,
        **attrs,
    ) -> Markup:
        """Renders the field as a `<input type="checkbox">` tag.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs["type"] = "checkbox"
        attrs.setdefault("required", self.required)

        value = attrs.get("value")
        if value is not None:
            attrs.setdefault("checked", in_(value, self.values))
        else:
            attrs.setdefault("checked", type_boolean(self.value))
        html_attrs = get_html_attrs(attrs, show_error=bool(self.error))

        html = "<input {}>".format(html_attrs)
        if label:
            kwargs = {"for": None, "classes": attrs.get("classes", "checkbox")}
            html = self.label(label, html=html, **kwargs)

        return Markup(html)

    def as_radio(
        self,
        *,
        label: str | None = None,
        **attrs,
    ) -> Markup:
        """Renders the field as a `<input type="radio">` tag.

        value_index (int):
            If `multiple` is True but the field display only one value,
            this is the index of the value that will be used.
            By default this is 0.
            If the list of values is not long enough, the value used is
            an empty string.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs["type"] = "radio"
        attrs.setdefault("required", self.required)

        value = attrs.get("value")
        if value is not None:
            attrs.setdefault("checked", in_(value, self.values))
        else:
            attrs.setdefault("checked", type_boolean(self.value))
        html_attrs = get_html_attrs(attrs, show_error=bool(self.error))

        html = "<input {}>".format(html_attrs)
        if label:
            kwargs = {"for": None, "classes": attrs.get("classes", "radio")}
            html = self.label(label, html=html, **kwargs)

        return Markup(html)

    def as_select_tag(
        self,
        *,
        label: str | None = None,
        **attrs,
    ) -> Markup:
        """Renders *just* the opening `<select>` tag for a field, not any options
        nor the closing "</select>".

        This is intended to be used with `<option>` tags writted by hand or genereated
        by other means.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        attrs.setdefault("multiple", self.multiple)
        html_attrs = get_html_attrs(attrs, show_error=bool(self.error))

        html = "<select {}>".format(html_attrs)
        if label:
            kwargs = {"for": attrs.get("id", self.name)}
            html = self.label(label, **kwargs) + "\n" + html

        return Markup(html)

    def as_select(
        self,
        items: tuple[str, tuple[t.Any, ...]],
        *,
        label: str | None = None,
        **attrs,
    ) -> Markup:
        """Renders the field as a `<select>` tag.

        items (list):
            ...

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """

        html = [str(self.as_select_tag(label=label, **attrs))]

        for item in items:
            ilabel, value = item[:2]
            if isinstance(value, (list, tuple)):
                tags = self.render_optgroup(ilabel, value)
            else:
                opattrs = item[2] if len(item) > 2 else {}
                assert isinstance(opattrs, dict)
                tags = self.render_option(ilabel, value, **opattrs)
            html.append(str(tags))

        html.append("</select>")
        return Markup("\n".join(html))

    def render_optgroup(
        self,
        label: str,
        items,
        **attrs,
    ) -> Markup:
        """Renders an <optgroup> tag with <options>.

        label (str):
            ...

        items (list):
            ...

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs["label"] = escape_silent(str(label))
        html_attrs = get_html_attrs(attrs, show_error=bool(self.error))
        html = ["<optgroup {}>".format(html_attrs)]

        for item in items:
            oplabel, opvalue = item[:2]
            opattrs = item[2] if len(item) > 2 else {}
            tag = self.render_option(oplabel, opvalue, **opattrs)
            html.append(str(tag))

        html.append("</optgroup>")
        return Markup("\n".join(html))

    def render_option(
        self,
        label: str,
        value: str | None = None,
        **attrs,
    ) -> Markup:
        """Renders an <option> tag

        label:
            Text of the option

        value:
            Value for the option (sames as the label by default).

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        values = self.values or []
        value = label if value is None else value
        attrs.setdefault("value", value)
        attrs["selected"] = in_(value, values)
        label = escape_silent(str(label))
        html_attrs = get_html_attrs(attrs, show_error=bool(self.error))
        tag = "<option {}>{}</option>".format(html_attrs, label)
        return Markup(tag)

    def render_error(self, tag: str = "div", **attrs) -> Markup:
        return render_error(self.error, tag=tag, **attrs)

    # Private

    def _reset(self) -> None:
        self.error = None
        self.error_value = None
        self.updated = False

    def _pre(self, values: list[str]) -> list[str]:
        if self.collection:
            rxsep = r"\s*%s\s*" % re.escape(self.sep.strip())
            all_values = []
            for value in values:
                all_values += re.split(rxsep, value)
            return all_values
        return values

    def _post(self, values: list[str]) -> list[str] | str | None:
        if self.collection:
            return self.sep.join(values)
        elif self.multiple:
            return values
        else:
            return values[0] if values else None

    def _typecast_values(self, values: list[str]) -> list[t.Any]:
        pyvalues = []
        for value in values:
            try:
                pyvalue = self.type(value, **self.extra)
            except (ValueError, TypeError, IndexError):
                pyvalue = None

            if pyvalue is None:
                if self.strict:
                    self._set_error(TYPE)
                    self.error_value = value
                    return []
                continue  # pragma: no cover
            pyvalues.append(pyvalue)
        return pyvalues

    def _validate_values(self, pyvalues: list[t.Any]) -> None:
        num_values = len(pyvalues)

        if self.min_num is not None and self.min_num > num_values:
            self._set_error(MIN_NUM, num=self.min_num)
            return

        if self.max_num is not None and self.max_num < num_values:
            self._set_error(MAX_NUM, num=self.max_num)
            return

        for validator in self.validators:
            message = INVALID
            valid = validator(pyvalues)
            if valid not in (True, False):
                valid, message = valid

            if not valid:
                self.error = message
                return

    def _set_error(self, name: str, **kwargs) -> None:
        msg = self.error_messages.get(name) or default_error_messages.get(name) or ""
        self.error = msg.format_map(SafeDict(kwargs)) or name
