from ..attribute import _tpl_attribute_variable
from ..strutils import _normalize_directions


class _tpl_legend:
  def __init__(self):
    self.pos = _tpl_attribute_variable(token="legend pos")

  def _set_position(self, value: str):
    value = _normalize_directions(value)
    self.pos.set_value(value)
