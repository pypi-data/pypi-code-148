from string import Template


class RecursionDepth(RuntimeError):
    pass


class DottedTemplate(Template):
    """
    Allow tokens to have "." in them.
    """

    idpattern = r"(?a:[_.a-z][_.a-z0-9]*)"


# ----------------------------------------------------------------------------------------
def substitute_string(target, substitutions, what=None):
    """
    Replace the replacements in the current string.
    Tokens in string should use ${token}.
    Replacements is a list key-value-pairs (token: value).
    Tokens may have "." in them.
    """

    template_string = target
    old_template_string = None
    max_depth = 10
    depth = 0
    while template_string != old_template_string:
        old_template_string = template_string
        template = DottedTemplate(template_string)
        template_string = template.safe_substitute(substitutions)
        depth = depth + 1
        if depth > max_depth:
            if what is None:
                raise RecursionDepth("template substitution recursion depth exceeded")
            else:
                raise RecursionDepth(
                    f"template substitution of {what} recursion depth exceeded"
                )

    return template_string


# ----------------------------------------------------------------------------------------
def substitute_dict(target, substitutions, what=None):
    for key, value in target.items():
        if what is None:
            what2 = key
        else:
            what2 = f"{what} {key}"
        if isinstance(value, dict):
            substitute_dict(value, substitutions, what=what)
        # Don't bother to substitute for any value that is not a string.
        elif isinstance(value, str):
            target[key] = substitute_string(value, substitutions, what=what2)


# ----------------------------------------------------------------------------------------
def substitute(target, substitutions, what=None):
    """
    Deprecated in favor of substitute_dict."""
    substitute_dict(target, substitutions, what=what)
