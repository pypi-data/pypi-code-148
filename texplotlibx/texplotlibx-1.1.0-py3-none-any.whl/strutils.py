def _compactify(s: str, level: int = 2):
  if level == 0:
    return s
  s = s.strip()
  if level == 1:
    return s
  s = "\n".join([x for x in s.split("\n") if x.strip() != ""])
  if level == 2:
    return s
  s = "\n".join([x for x in s.split("\n") if not x.strip().startswith("%")])
  if level == 3:
    return s


def _savetext(filename: str, text: str):
  with open(filename, "w") as f:
    f.writelines(text)


def _escape_characters(s: str, chars_to_escape: list[str] = None):
  if s is None:
    return s
  if chars_to_escape is None:
    chars_to_escape = ['%', '#']
  for ch in chars_to_escape:
    s = s.replace(ch, "\\" + ch)
  return s


def _normalize_directions(dirs: str) -> str:
  def __expand_directions(short: str) -> str:
    def __expand(s: str) -> str:
      if s == 'n':
        return 'north'
      if s == 's':
        return 'south'
      if s == 'e':
        return 'east'
      if s == 'w':
        return 'west'
      if s == 'o':
        return 'outer'
      raise Exception('Cannot deduce direction \"%s\"' % s)
    return ' '.join(__expand(s) for s in short)
  if len(dirs) <= 3:
    dirs = __expand_directions(dirs)
  return dirs
