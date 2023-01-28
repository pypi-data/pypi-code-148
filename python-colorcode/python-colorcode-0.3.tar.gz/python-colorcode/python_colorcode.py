import random
from webcolors import name_to_rgb, CSS3_NAMES_TO_HEX


def generate_color_shades(color_name, rgb=False):
  """Generates a list of 20 shades of a specified color."""
  try:
    color_rgb = name_to_rgb(color_name)
    color_shades = []
    for i in range(20):
      shade = []
      for j in range(3):
        c = int(color_rgb[j] + (255 - color_rgb[j]) * (i / 20))
        shade.append(c)
      color_shades.append(tuple(shade))
    if rgb:
      return color_shades
    else:
      hex_color_shades = []
      for shade in color_shades:
        hex_shade = '#'
        for c in shade:
          hex_shade += hex(c)[2:].zfill(2)
        hex_color_shades.append(hex_shade)
      return hex_color_shades
  except ValueError:
    if color_name not in CSS3_NAMES_TO_HEX:
      raise ValueError(f"{color_name} is not a valid color name.")
