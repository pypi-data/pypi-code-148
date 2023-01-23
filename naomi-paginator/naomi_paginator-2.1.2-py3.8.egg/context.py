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

from discord import Embed, errors
from discord.ext.commands import Context

from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio import wait as asyncioWait
from asyncio import FIRST_COMPLETED as ASYNCIO_FIRST_COMPLETED
from typing import Optional, Union, Tuple, List


class Paginator:
    def __init__(
        self,
        ctx: Context,
        reactions: Optional[Union[Tuple[str], List[str]]] = None,
        timeout: int = 120,
    ) -> None:
        """Init a new paginator instance.

        Parameters
        ----------
        ctx : commands.Context
            Current command context.
        reactions : Optional[List[str]]
            Custom reaction emojis for the paginator.
            [previous_page, destroy_embed, next_page] - an array with 3 emojis.
        timeout : int
            Timeout in seconds (default: 120)
        """
        self.reactions = reactions or ("◀️", "🛑", "▶️")
        self.pages = []
        self.current = 0
        self.ctx = ctx
        self.timeout = timeout

    async def _close_session(self) -> None:
        """Close the paginator session and delete the message."""
        try:
            await self.controller.delete()
        except errors.NotFound:
            pass

        del self.pages
        del self.reactions
        del self.current
        del self.ctx

    def add_page(self, embed: Embed) -> None:
        """Add a new page to the paginator.

        Parameters
        ----------
        embed : discord.Embed
            discord.Embed object for the new page.
        """
        self.pages.append(embed)

    async def call_controller(self, start_page: int = 0) -> None:
        """Call the paginator.

        Parameters
        ----------
        start_page : int
            Start paginator from the given page (default: 0 - first page)
        """
        if start_page > len(self.pages) - 1:
            raise IndexError(
                f"Currently added {len(self.pages)} pages, but you"
                f" tried to call controller with start_page = {start_page}"
            )

        self.controller = await self.ctx.send(embed=self.pages[start_page])

        for emoji in self.reactions:
            await self.controller.add_reaction(emoji)

        def author_check(r, u):
            return (
                u.id == self.ctx.author.id
                and r.emoji in self.reactions
                and r.message.id == self.controller.id
            )

        while True:
            try:
                tasks = [
                    self.ctx.bot.wait_for(
                        "reaction_add", timeout=self.timeout, check=author_check
                    ),
                    self.ctx.bot.wait_for(
                        "reaction_remove", timeout=self.timeout, check=author_check
                    ),
                ]

                tasks_result, tasks = await asyncioWait(
                    tasks, return_when=ASYNCIO_FIRST_COMPLETED
                )

                for task in tasks:
                    task.cancel()
                for task in tasks_result:
                    response = await task

            except AsyncioTimeoutError:
                break

            try:
                await self.controller.remove_reaction(response[0], response[1])
            except Exception:
                pass

            if response[0].emoji == self.reactions[0]:
                self.current = (
                    self.current -
                    1 if self.current > 0 else len(self.pages) - 1
                )
                await self.controller.edit(embed=self.pages[self.current])

            if response[0].emoji == self.reactions[1]:
                break

            if response[0].emoji == self.reactions[2]:
                self.current = (
                    self.current +
                    1 if self.current < len(self.pages) - 1 else 0
                )
                await self.controller.edit(embed=self.pages[self.current])

        await self._close_session()
