"""Common code for discord bots"""
import random
import typing
from ._utils import _check_required_modules, _INSTALLED_MODULES

try:
    import discord
    from discord.ext import commands

    _INSTALLED_MODULES["discord.py"] = True
except ModuleNotFoundError:
    pass


@_check_required_modules("discord.py")
async def error_embed(ctx: "commands.Context", message: str, title: str = "Error:", **kwargs):
    """
    Makes and send an error embed

    **Requires discord.py**

    **Asynchronous Function**

    :raises ModuleNotFoundError: Will raise a ModuleNotFoundError if discord.py module \
    is not installed

    :param ctx: Command context
    :type ctx: discord.ext.commands.Context
    :param message: Message description
    :type message: str
    :param title: Error message title
    :type title: str
    """
    await make_embed(ctx, color="FF0000", send=True, description=message, title=title, **kwargs)


@_check_required_modules("discord.py")
async def make_embed(
    ctx: "commands.Context",
    color: typing.Union[str, int, "discord.Color"] = None,
    send: typing.Union[bool, str] = True,
    as_reply: bool = False,
    **kwargs,
) -> typing.Optional["discord.Embed"]:
    """
    Makes and defaults to sending a discord.Embed


    **Asynchronous Function**

    :raises ModuleNotFoundError: Will raise a ModuleNotFoundError if discord.py module \
    is not installed

    :param ctx: Discord context
    :type ctx: discord.ext.commands.Context
    :param color: Color of the embed
    :type color: [str, int, discord.Color]
    :param send: Send the message instead of returning
    :type send: bool
    :param as_reply: Reply to the message instead of sending
    :type as_reply: bool
    :param kwargs: Keyword arguments to pass to embed
    :return: Filled out embed if send is False
    """

    if not color:
        kwargs["color"] = random.randint(0, 16777215)  # nosec
    elif isinstance(color, str):
        kwargs["color"] = discord.Color(int(color, 16))

    footer = kwargs.pop("footer", None)
    embed = discord.Embed(timestamp=ctx.message.created_at, **kwargs)

    if footer:
        embed.set_footer(text=footer)
    if send:
        if as_reply:
            await ctx.reply(embed=embed)
        else:
            await ctx.send(embed=embed)
    else:
        return embed


@_check_required_modules("discord.py")
async def error_message(
    ctx: "commands.Context", message: str, title: str = "Error:", **kwargs
) -> None:
    """Error Message
    Generate an error embed

    **Requires discord.py**

    **Asynchronous Function**

    :param ctx: Discord Context
    :type ctx: discord.ext.commands.Context
    :param message: Message of the error
    :param title: Title of error embed
    :param kwargs: Keyword arguments to pass to Embed
    """
    await make_embed(ctx, "FF0000", True, description=message, title=title, **kwargs)


@_check_required_modules("discord.py")
async def list_message(ctx: "commands.Context", message: list, title: str, **kwargs) -> None:
    """List Message

    Breaks up messages that contain a list and sends the parts of them. Shared function between
    multiple commands.

    **Requires discord.py**

    **Asynchronous Function**

    I'm sorry for everyone dealing with this function. It is not clean and I have commented to
    the best that I can.

    :param ctx: Context of command.
    :type ctx: discord.ext.commands.Context
    :param message: list of items to send.
    :type message: list
    :param title: Title of the message to send.
    :type title: str
    :param kwargs: keyword arguments
    :type kwargs: dict
    :return: All embeds are sent
    ":rtype: None
    """
    joined_message = len("".join(message))
    list_of_embeds = []
    part = 1
    item = 0
    amount_of_embeds = len(range(0, joined_message, 1500))
    for _ in range(amount_of_embeds):
        # Each embed can only be 6000 characters so if the length is over that more are created
        embed = await make_embed(ctx, title=title, send=False, **kwargs)
        for _ in range(2):
            temp_msg = ""
            while len(temp_msg) < 1024:
                # Each field can only be 1024 characters
                try:
                    if len(temp_msg + f"- {message[item]}\n") > 1024:
                        # If the new item is going to make it over the 1024 limit then skip it.
                        break
                    temp_msg += f"- {message[item]}\n"
                    item += 1
                except IndexError:
                    # Error happens when there the length of temp_msg is still under 1000 but
                    # no items left.
                    break
            if len(temp_msg) > 0:
                # Blank messages can occur and this filters them out
                embed.add_field(name=f"Part: {part}", value=temp_msg, inline=True)
                part += 1
        list_of_embeds.append(embed)

    for item in list_of_embeds:
        if len(item.fields) > 0:
            await ctx.send(embed=item)
