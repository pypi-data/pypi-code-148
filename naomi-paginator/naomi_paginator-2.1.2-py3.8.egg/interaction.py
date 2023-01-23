"""
MIT License

Copyright (c) 2020-present The-Naomi-Developers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from discord import Embed, Interaction
from discord.ui import View
from typing import Union, Tuple, List
from .buttons import NextPageButton, CloseButton, PreviousPageButton, ButtonProperties


class InteractionPaginator(View):
    def __init__(
        self,
        interaction: Interaction,
        pages: Union[Tuple[Embed], List[Embed]],
        button_styles: List[ButtonProperties] = None,
        timeout: int = 120,
    ) -> None:
        """Initialize a new interaction paginator instance.

        Parameters
        ----------
        interaction: discord.Interaction
            Current interaction object.
        pages: Union[List[Embed]]
            A tuple or list of discord.Embed objects.
        button_styles: List
        timeout: int
            Timeout in seconds (default: 120)
        """
        if len(button_styles) != 3:
            raise ValueError(
                "You should not set a 'button_styles' attribute or pass 3 'ButtonProperties' objects.")
        super().__init__(timeout=timeout)
        self.i = interaction
        self.pages = pages
        self.timeout = timeout
        self.current = 0
        for b in (
            PreviousPageButton(self, button_styles[0]),
            CloseButton(self, button_styles[1]),
            NextPageButton(self, button_styles[2])
        ):
            self.add_item(b)

    async def on_timeout(self) -> None:
        await self._close()

    async def _close(self) -> None:
        """Close the paginator session and delete the message."""
        try:
            await self.i.delete_original_message()
        except:
            pass

    async def _move(self, i: Interaction, num: int):
        """Go to the ``current_page - num`` page."""
        self.current += num if self.current + num < len(
            self.pages) and self.current + num >= 0 else 0
        await i.response.edit_message(embed=self.pages[self.current])
