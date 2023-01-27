# SPDX-FileCopyrightText: Copyright (c) 2021 Jose David M.
#
# SPDX-License-Identifier: MIT
"""

`scales`
================================================================================

Allows display data in a graduated level


* Author(s): Jose David M.

Implementation Notes
--------------------

This library is closely related with Cartesian. The Cartesian library was developed first.
After this, new granular classes were created for Axes. and new methods to calculate the
conversion between range, pixels and values given

"""

################################
# A scales library for CircuitPython, using `displayio`` and `vectorio``
#
# Features:
#  - Customizable range and divisions
#  - Vertical and Horizontal direction
#  - Animation to use with different sensor
#
# Future options to consider:
# ---------------------------
# Different pointers
# Pointer using real values

import displayio
import terminalio
from adafruit_display_text.bitmap_label import Label
from vectorio import Polygon, Rectangle

try:
    from typing import Tuple
except ImportError:
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_scales.git"


# pylint: disable=too-many-instance-attributes, too-many-arguments, too-few-public-methods


class Axes(displayio.Group):
    """
    :param int x: pixel position. Defaults to :const:`0`
    :param int y: pixel position. Defaults to :const:`0`

    :param int,int limits: tuple of value range for the scale. Defaults to (0, 100)
    :param int divisions: Divisions number

    :param str direction: direction of the scale either :attr:`horizontal` or :attr:`vertical`
     defaults to :attr:`horizontal`

    :param int stroke: width in pixels of the scale axes. Defaults to :const:`3`

    :param int length: scale length in pixels. Defaults to :const:`100`

    :param int color: 24-bit hex value axes line color, Defaults to Purple :const:`0x990099`

    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        limits: Tuple[int, int] = (0, 100),
        divisions: int = 10,
        direction: str = "horizontal",
        stroke: int = 3,
        length: int = 100,
        color: int = 0x990099,
    ):

        super().__init__()

        self.x = x
        self.y = y
        self.limits = limits

        self.divisions = divisions

        if direction == "horizontal":
            self.direction = True
        else:
            self.direction = False

        self.stroke = stroke
        self.length = length

        self._palette = displayio.Palette(2)
        self._palette.make_transparent(0)
        self._palette[1] = color

        self._tick_length = None
        self._tick_stroke = None
        self.ticks = None
        self.text_ticks = None

    def _draw_line(self):
        """Private function to draw the Axe.
        :return: None
        """
        if self.direction:
            self.append(rectangle_draw(0, 0, self.stroke, self.length, self._palette))
        else:
            self.append(
                rectangle_draw(0, -self.length, self.length, self.stroke, self._palette)
            )

    # pylint: disable=invalid-unary-operand-type
    def _draw_ticks(self, tick_length: int = 10, tick_stroke: int = 4):
        """Private function to draw the ticks
        :param int tick_length: tick length in pixels
        :param int tick_stroke: tick thickness in pixels
        :return: None
        """
        self._tick_length = tick_length
        self._tick_stroke = tick_stroke
        self._conversion()

        if self.direction:
            for val in self.ticks[:-1]:
                self.append(
                    rectangle_draw(
                        val - 1, -self._tick_length, self._tick_length, 3, self._palette
                    )
                )
        else:
            for val in self.ticks[:-1]:
                self.append(
                    rectangle_draw(0, -val, 3, self._tick_length, self._palette)
                )

    def _conversion(self):
        """Private function that creates the ticks distance and text.
        :return: None
        """
        self.ticks = []
        self.text_ticks = []
        espace = round(self.length / self.divisions)
        rang_discrete = self.limits[1] - self.limits[0]
        factorp = self.length / rang_discrete
        for i in range(espace, self.length + 1, espace):
            self.ticks.append(i)
            self.text_ticks.append(str(int(self.limits[0] + i * 1 / factorp)))

    def _draw_text(self):
        """Private function to draw the text, uses values found in ``_conversion``
        :return: None
        """
        index = 0
        separation = 20
        font_width = 12
        if self.direction:
            for tick_text in self.text_ticks[:-1]:
                dist_x = self.ticks[index] - font_width // 2
                dist_y = separation // 2
                tick_label = Label(terminalio.FONT, text=tick_text, x=dist_x, y=dist_y)
                self.append(tick_label)
                index = index + 1
        else:
            for tick_text in self.text_ticks[:-1]:
                dist_x = -separation
                dist_y = -self.ticks[index]
                tick_label = Label(terminalio.FONT, text=tick_text, x=dist_x, y=dist_y)
                self.append(tick_label)
                index = index + 1


class Scale(Axes):
    """
    :param int x: pixel position. Defaults to :const:`0`
    :param int y: pixel position. Defaults to :const:`0`

    :param str direction: direction of the scale either :attr:`horizontal` or :attr:`vertical`
     defaults to :attr:`horizontal`

    :param int stroke: width in pixels of the scale axes. Defaults to 3

    :param int length: scale length in pixels. Defaults to 100
     that extends the touch response boundary, defaults to 0

    :param int color: 24-bit hex value axes line color, Defaults to purple :const:`0x990099`

    :param int width: scale width in pixels. Defaults to :const:`50`

    :param limits: tuple of value range for the scale. Defaults to :const:`(0, 100)`
    :param int divisions: Divisions number

    :param int back_color: 24-bit hex value axes line color.
     Defaults to Light Blue :const:`0x9FFFFF`

    :param int tick_length: Scale tick length in pixels. Defaults to :const:`10`
    :param int tick_stroke: Scale tick width in pixels. Defaults to :const:`4`


    **Quickstart: Importing and using Scales**

    Here is one way of importing the `Scale` class so you can use it as
    the name ``my_scale``:

    .. code-block:: python

        from Graphics import Scale

    Now you can create an vertical Scale at pixel position x=50, y=180 with 3 divisions and a range
    of 0 to 80 using:

    .. code-block:: python

        my_scale = Scale(x=50, y=180, direction="vertical", divisions=3, limits=(0, 80))

    Once you setup your display, you can now add ``my_scale`` to your display using:

    .. code-block:: python

        display.show(my_scale)

    If you want to have multiple display elements, you can create a group and then
    append the scale and the other elements to the group. Then, you can add the full
    group to the display as in this example:

    .. code-block:: python

        my_scale= Scale(x=20, y=30)
        my_group = displayio.Group(max_size=10) # make a group that can hold 10 items
        my_group.append(my_scale) # Add my_slider to the group

        #
        # Append other display elements to the group
        #

        display.show(my_group) # add the group to the display


    **Summary: Slider Features and input variables**

    The `Scale` class has some options for controlling its position, visible appearance,
    and value through a collection of input variables:

        - **position**: :attr:`x``, :attr:`y`

        - **size**: :attr:`length` and :attr:`width`

        - **color**: :attr:`color`, :attr:`back_color`

        - **linewidths**: :attr:`stroke` and :attr:`tick_stroke`

        - **value**: Set :attr:`value` to the initial value (`True` or `False`)

        - **range and divisions**: :attr:`limits` and :attr:`divisions`


    .. figure:: scales.png
      :scale: 100 %
      :align: center
      :alt: Diagram of scales

      Diagram showing a simple scale.


    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        direction: str = "horizontal",
        stroke: int = 3,
        length: int = 100,
        color: int = 0x990099,
        width: int = 50,
        limits: Tuple[int, int] = (0, 100),
        divisions: int = 10,
        back_color: int = 0x9FFFFF,
        tick_length: int = 10,
        tick_stroke: int = 4,
    ):

        super().__init__(
            x=x,
            y=y,
            direction=direction,
            stroke=stroke,
            length=length,
            limits=limits,
            divisions=divisions,
            color=color,
        )

        self._width = width
        self._back_color = back_color
        self._draw_background()
        self._draw_line()
        self._draw_ticks()

        self._tick_length = tick_length
        self._tick_stroke = tick_stroke

        self.pointer = None

        self._draw_text()

        self._draw_pointer()

    def _draw_background(self):
        """Private function to draw the background for the scale
        :return: None
        """
        back_palette = displayio.Palette(2)
        back_palette.make_transparent(0)
        back_palette[1] = self._back_color

        if self.direction:
            self.append(
                rectangle_draw(0, -self._width, self._width, self.length, back_palette)
            )
        else:
            self.append(
                rectangle_draw(0, -self.length, self.length, self._width, back_palette)
            )

    def _draw_pointer(
        self,
        color: int = 0xFF0000,
        val_ini: int = 15,
        space: int = 3,
        pointer_length: int = 20,
        pointer_stroke: int = 6,
    ):
        """Private function to initial draw the pointer.

        :param int color: 24-bit hex value axes line color. Defaults to red :const:`0xFF0000`
        :param int val_ini: initial value to draw the pointer
        :param int space: separation in pixels from the ticker to the pointer.
         Defaults to :const:`3`
        :param int pointer_length: length in pixels for the point. Defaults to :const:`20`
        :param int pointer_stroke: pointer thickness in pixels. Defaults to :const:`6`

        :return: None

        """

        pointer_palette = displayio.Palette(2)
        pointer_palette.make_transparent(0)
        pointer_palette[1] = color

        self._pointer_length = pointer_length
        self._space = space
        self._pointer_stroke = pointer_stroke

        if self.direction:
            points = [
                (
                    self.x - self._pointer_stroke // 2 + val_ini,
                    self.y - self.stroke - self._tick_length - self._space,
                ),
                (
                    self.x - self._pointer_stroke // 2 + val_ini,
                    self.y
                    - self.stroke
                    - self._tick_length
                    - self._space
                    - self._pointer_length,
                ),
                (
                    self.x + self._pointer_stroke // 2 + val_ini,
                    self.y
                    - self.stroke
                    - self._tick_length
                    - self._space
                    - self._pointer_length,
                ),
                (
                    self.x + self._pointer_stroke // 2 + val_ini,
                    self.y - self.stroke - self._tick_length - self._space,
                ),
            ]

        else:
            points = [
                (
                    self.stroke + self._tick_length + space,
                    self.y + self._pointer_stroke // 2 - val_ini,
                ),
                (
                    self.stroke
                    + self._tick_length
                    + self._space
                    + self._pointer_length,
                    self.y + self._pointer_stroke // 2 - val_ini,
                ),
                (
                    self.stroke
                    + self._tick_length
                    + self._space
                    + self._pointer_length,
                    self.y - self._pointer_stroke // 2 - val_ini,
                ),
                (
                    self.stroke + self._tick_length + self._space,
                    self.y - self._pointer_stroke // 2 - val_ini,
                ),
            ]

        self.pointer = Polygon(
            pixel_shader=pointer_palette,
            points=points,
            x=0,
            y=-self.y,
            color_index=1,
        )

        self.append(self.pointer)

    def animate_pointer(self, value):
        """Public function to animate the pointer

        :param value: value to draw the pointer
        :return: None

        """

        if self.direction:
            self.pointer.points = [
                (
                    self.x - self._pointer_stroke // 2 + value,
                    self.y - self.stroke - self._tick_length - self._space,
                ),
                (
                    self.x - self._pointer_stroke // 2 + value,
                    self.y
                    - self.stroke
                    - self._tick_length
                    - self._space
                    - self._pointer_length,
                ),
                (
                    self.x + self._pointer_stroke // 2 + value,
                    self.y
                    - self.stroke
                    - self._tick_length
                    - self._space
                    - self._pointer_length,
                ),
                (
                    self.x + self._pointer_stroke // 2 + value,
                    self.y - self.stroke - self._tick_length - self._space,
                ),
            ]
        else:
            self.pointer.points = [
                (
                    self.stroke + self._tick_length + self._space,
                    self.y + self._pointer_stroke // 2 - value,
                ),
                (
                    self.stroke
                    + self._tick_length
                    + self._space
                    + self._pointer_length,
                    self.y + self._pointer_stroke // 2 - value,
                ),
                (
                    self.stroke
                    + self._tick_length
                    + self._space
                    + self._pointer_length,
                    self.y - self._pointer_stroke // 2 - value,
                ),
                (
                    self.stroke + self._tick_length + self._space,
                    self.y - self._pointer_stroke // 2 - value,
                ),
            ]


# pylint: disable=invalid-name
def rectangle_draw(x0: int, y0: int, height: int, width: int, palette):
    """rectangle_draw function

    Draws a rectangle using or `vectorio.Rectangle`

    :param int x0: rectangle lower corner x position
    :param int y0: rectangle lower corner y position

    :param int width: rectangle upper corner x position
    :param int height: rectangle upper corner y position

    :param `~displayio.Palette` palette: palette object to be used to draw the rectangle

    """

    return Rectangle(
        pixel_shader=palette, width=width, height=height, x=x0, y=y0, color_index=1
    )
