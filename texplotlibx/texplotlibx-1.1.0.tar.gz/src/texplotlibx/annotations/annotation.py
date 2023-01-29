from ..attribute import _tpl_attribute_flag
from ..strutils import _normalize_directions


class _tpl_annotation(_tpl_attribute_flag):
  @staticmethod
  def __opposite_directions(pos: str) -> str:
    opposite = []
    for word in pos.split(' '):
      if word == 'north':
        opposite.append('below')
      elif word == 'east':
        opposite.append('left')
      elif word == 'south':
        opposite.append('above')
      elif word == 'west':
        opposite.append('right')
      elif word in ('outer', 'inner'):
        pass
      else:
        raise Exception('Cannot deduce opposite of direction %s' % word)
    return ' '.join(opposite)

  def __init__(self, pos: str, label: str, axis: str, xshift: str = None, yshift: str = None):
    pos = _normalize_directions(pos)
    if xshift is None:
      if 'west' in pos:
        xshift = '5mm'
      elif 'east' in pos:
        xshift = '-5mm'
      else:
        xshift = '0mm'
    if yshift is None:
      if 'south' in pos:
        yshift = '5mm'
      elif 'north' in pos:
        yshift = '-5mm'
      else:
        yshift = '0mm'
    relative_pos = self.__class__.__opposite_directions(pos)
    cmd = f'\\node[{relative_pos},xshift={xshift},yshift={yshift}] at ({axis}.{pos}) {{{label}}};'
    super().__init__(cmd, True)
