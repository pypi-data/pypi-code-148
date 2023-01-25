import re


def create_initials(s: str) -> str:
    """
    Return the initial letter of each word in `s`, capitalized and strung together

    Example:
        >>> create_initials("John Smith") == "JS"

    :param s: String to create initials out of
    :return: Initials of `s`, capitalized
    """
    return "".join(s[0] if s else '' for s in re.split(r"[\W_]+", s)).upper()
