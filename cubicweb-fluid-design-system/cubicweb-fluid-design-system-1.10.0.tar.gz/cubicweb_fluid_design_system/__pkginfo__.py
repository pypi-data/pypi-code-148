# pylint: disable=W0622
"""cubicweb-fluid-design-system application packaging information"""

modname = "fluid_design_system"
distname = "cubicweb-fluid-design-system"

numversion = (1, 10, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = ""
web = ""

__depends__ = {
    "cubicweb": ">= 3.38.0, < 3.39.0",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
