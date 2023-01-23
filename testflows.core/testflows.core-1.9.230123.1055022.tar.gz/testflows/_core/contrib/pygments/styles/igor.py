# -*- coding: utf-8 -*-
"""
    pygments.styles.igor
    ~~~~~~~~~~~~~~~~~~~~

    Igor Pro default style.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from testflows._core.contrib.pygments.style import Style
from testflows._core.contrib.pygments.token import Keyword, Name, Comment, String


class IgorStyle(Style):
    """
    Pygments version of the official colors for Igor Pro procedures.
    """
    default_style = ""

    styles = {
        Comment:                'italic #FF0000',
        Keyword:                '#0000FF',
        Name.Function:          '#C34E00',
        Name.Decorator:         '#CC00A3',
        Name.Class:             '#007575',
        String:                 '#009C00'
    }
