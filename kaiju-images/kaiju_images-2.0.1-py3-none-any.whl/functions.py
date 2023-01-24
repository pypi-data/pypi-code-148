"""

Available operations (builtin)
------------------------------

`Documentation <http://willow.readthedocs.org/en/latest/reference.html#builtin-operations>`_

=================================== ==================== ==================== ====================
Operation                           Pillow               Wand                 OpenCV
=================================== ==================== ==================== ====================
``resize(size)``                    ✓                    ✓
``crop(rect)``                      ✓                    ✓
``rotate(angle)``                   ✓                    ✓
``set_background_color_rgb(color)`` ✓                    ✓
``auto_orient()``                   ✓                    ✓
=================================== ==================== ==================== ====================

Available operations (custom)
-----------------------------

Probably they will work with PIL type images only.

===================================
Operation
===================================
``scale(factor)``
``abs_scale(size)``
``aspect_crop(ratio, rel_point)``
``blur(size)``
``flip_horizontal()``
``flip_vertical()``
===================================

"""

from fractions import Fraction
from typing import *

import PIL.Image
from willow.registry import registry
from willow.plugins.pillow import PillowImage
from willow.plugins.wand import WandImage

import kaiju_tools.jsonschema as schema

__all__ = [
    'aspect_crop', 'wand_blur', 'pillow_blur', 'scale', 'abs_scale',
    'pillow_flip_horizontal', 'pillow_flip_vertical', 'pillow_to_buffer_rgb', 'willow_to_buffer_rgb'
]


def pillow_flip_horizontal(image):
    image = image.image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
    return PillowImage(image)


def pillow_flip_vertical(image):
    image = image.image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
    return PillowImage(image)


def pillow_to_buffer_rgb(image):
    if image.image.mode != 'RGB':
        image = image.image.convert('RGB')
        return PillowImage(image)

    return PillowImage(image.image)


def willow_to_buffer_rgb(image):
    if image.image.mode != 'RGB':
        image = image.image.convert('RGB')
        return WandImage(image)

    return WandImage(image)


willow_to_buffer_rgb.__json_spec__ = None
pillow_to_buffer_rgb.__json_spec__ = None
pillow_flip_horizontal.__json_spec__ = None
pillow_flip_vertical.__json_spec__ = None
registry.register_operation(PillowImage, 'to_buffer_rgb', pillow_to_buffer_rgb)
registry.register_operation(WandImage, 'to_buffer_rgb', willow_to_buffer_rgb)
registry.register_operation(PillowImage, 'flip_horizontal', pillow_flip_horizontal)
registry.register_operation(PillowImage, 'flip_vertical', pillow_flip_vertical)


def abs_scale(image, size: int):
    """Scales image so the longest dimension will become equal to `size`
    and the aspect ratio stays the same.

    :param image:
    :param size: size in px
    """

    size = max(1, int(size))
    x, y = image.get_size()
    x, y = int(x), int(y)
    aspect = Fraction(x, y)
    if x > y:
        x = size
        y = round(x / aspect)
    else:
        y = size
        x = round(y * aspect)
    image = image.resize((x, y))
    return image


abs_scale.__json_spec__ = schema.Object(
    size=schema.Integer(
        minimum=1, maximum=10000,
        title='Longest dimension final size (px).'
    ),
    required=['size'],
    additionalProperties=False
)
registry.register_operation(PillowImage, 'abs_scale', abs_scale)
registry.register_operation(WandImage, 'abs_scale', abs_scale)


def scale(image, scale: float):
    """Scale image.

    :param image:
    :param scale: new scale scale
    """

    x, y = image.get_size()
    new_x, new_y = round(x * scale), round(y * scale)
    image = image.resize((new_x, new_y))
    return image


scale.__json_spec__ = schema.Object(
    scale=schema.Number(
        exclusiveMinimum=0, maximum=10,
        title='Relative scale value.'
    ),
    required=['ratio'],
    additionalProperties=False
)
registry.register_operation(PillowImage, 'scale', scale)
registry.register_operation(WandImage, 'scale', scale)


def aspect_crop(image, ratio: Tuple[int, int], rel_shift=(0.5, 0.5)):
    """Crop image to a new aspect ratio.

    :param image:
    :param ratio: an integer ratio of new X:Y
    :param rel_shift: default - centered, i.e. 0.5, 0.5
    """

    new_aspect = Fraction(int(ratio[0]), int(ratio[1]))
    x, y = image.get_size()
    x, y = int(x), int(y)
    old_aspect = Fraction(x, y)

    if old_aspect < new_aspect:
        x1 = x
        y1 = y * old_aspect / new_aspect
    else:
        x1 = x * new_aspect / old_aspect
        y1 = y

    dx, dy = x - x1, y - y1
    shift_x, shift_y = rel_shift
    x0, y0 = int(dx * float(shift_x)), int(dy * float(shift_y))
    x1, y1 = x0 + x1, y0 + y1
    image = image.crop((x0, y0, x1, y1))
    return image


aspect_crop.__json_spec__ = schema.Object(
    ratio=schema.Array(
        items=[
            schema.Integer(
                minimum=1, maximum=100,
                title='Width relative value (numerator)'
            ),
            schema.Integer(
                minimum=1, maximum=100,
                title='Height relative value (denominator)'
            )
        ],
        title='New width/height integer ratio.',
        additionalItems=False,
        minItems=2, maxItems=2
    ),
    rel_shift=schema.Array(
        items=[
            schema.Number(
                minimum=0, maximum=1,
                title='Width relative'
            ),
            schema.Integer(
                minimum=0, maximum=1,
                title='Height relative'
            )
        ],
        title='Crop center position relative to the center of the original image.',
        additionalItems=False,
        minItems=2, maxItems=2
    ),
    required=['ratio'],
    additionalProperties=False
)
registry.register_operation(PillowImage, 'aspect_crop', aspect_crop)
registry.register_operation(WandImage, 'aspect_crop', aspect_crop)


def pillow_blur(image):
    from PIL import ImageFilter
    blurred_image = image.image.filter(ImageFilter.BLUR)
    return PillowImage(blurred_image)


def wand_blur(image):
    blurred_image = image.image.clone()
    blurred_image.gaussian_blur()
    return WandImage(blurred_image)


pillow_blur.__json_spec__ = wand_blur.__json_spec__ = None
registry.register_operation(PillowImage, 'blur', pillow_blur)
registry.register_operation(WandImage, 'blur', wand_blur)

pillow_resize = registry.get_operation(PillowImage, 'resize')
wand_resize = registry.get_operation(WandImage, 'resize')
pillow_resize.__json_spec__ = wand_resize.__json_spec__ = schema.Object(
    size=schema.Array(
        items=[
            schema.Integer(
                minimum=1, maximum=10000,
                title='Width (px)'
            ),
            schema.Integer(
                minimum=1, maximum=10000,
                title='Height (px)'
            )
        ],
        title='New dimensions.',
        additionalItems=False,
        minItems=2, maxItems=2
    ),
    required=['size'],
    additionalProperties=False
)

pillow_crop = registry.get_operation(PillowImage, 'crop')
wand_crop = registry.get_operation(WandImage, 'crop')
wand_crop.__json_spec__ = wand_crop.__json_spec__ = schema.Object(
    rect=schema.Array(
        items=[
            schema.Integer(
                minimum=0, maximum=10000,
                title='Left'
            ),
            schema.Integer(
                minimum=0, maximum=10000,
                title='Top'
            ),
            schema.Integer(
                minimum=0, maximum=10000,
                title='Right'
            ),
            schema.Integer(
                minimum=0, maximum=10000,
                title='Bottom'
            )
        ],
        title='New cropped image rectangle coordinates.',
        additionalItems=False,
        minItems=4, maxItems=4
    ),
    required=['rect'],
    additionalProperties=False
)

pillow_rotate = registry.get_operation(PillowImage, 'rotate')
wand_rotate = registry.get_operation(WandImage, 'rotate')
pillow_rotate.__json_spec__ = wand_rotate.__json_spec__ = schema.Object(
    angle=schema.Integer(
        minimum=90, maximum=360, multipleOf=90,
        title='Left'
    ),
    required=['angle'],
    additionalProperties=False
)
