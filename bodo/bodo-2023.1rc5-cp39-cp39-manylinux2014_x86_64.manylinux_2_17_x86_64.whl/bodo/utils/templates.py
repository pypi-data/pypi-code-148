"""
Helper functions and classes to simplify Template Generation
for Bodo classes.
"""
import numba
from numba.core.typing.templates import AttributeTemplate


class OverloadedKeyAttributeTemplate(AttributeTemplate):
    _attr_set = None

    def _is_existing_attr(self, attr_name):
        if self._attr_set is None:
            yba__shz = set()
            wmokp__nlwfl = list(self.context._get_attribute_templates(self.key)
                )
            vzxab__wtbp = wmokp__nlwfl.index(self) + 1
            for tjro__mrii in range(vzxab__wtbp, len(wmokp__nlwfl)):
                if isinstance(wmokp__nlwfl[tjro__mrii], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    yba__shz.add(wmokp__nlwfl[tjro__mrii]._attr)
            self._attr_set = yba__shz
        return attr_name in self._attr_set
