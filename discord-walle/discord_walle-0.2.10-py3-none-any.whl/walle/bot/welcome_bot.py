import re
from .base import BaseBot
import asyncio

__all__ = [
    "WelcomeBot",
]


class WelcomeBot(BaseBot):
    """Welcome Bot

    The purpose of this welcome bot
    will be a endpoint for any interaction involving
    events and/or actions that are associated with
    welcome to servers/channels/clans/groups/etc

    Parameters
    ----------

    action_config : ActionConfig(Config)
        A typed/defined action config that will
        have a predefined set of supported Primitive OPs

    event_config : EventConfig(Config)
        A typed/defined event config that will
        have a predefined set of supported Primitive OPs

    name : str
        the name of this specific bot

    Usage
    -----

    ```python

    from walle.configs import ActionConfig, EventConfig
    from walle.bot import WelcomeBot

    action_cfg = ActionConfig("welcome-actions")
    event_cfg = EventConfig("welcome-events")
    welcome_bot = WelcomeBot(
        action_config=action_cfg,
        event_cfg=event_cfg,
        name=name,
    )
    ```

    Notes
    -----

        The idea of config classes may change as we develop
            the basic idea seems sounds, but could be an entire rewrite

        We dont have a firm grasp on the scope of each bot, this is
            one direction we can go with it
    """

    def __init__(
        self,
        config,
        guild,
        client,
        name="welcome-bot",
        ask_move_msg="Would you like to move to the interview room? yes/no",
        channel_pattern="(welcome|entry)",
        channel_move_name="Test-Channel",
    ):
        super().__init__(
            config=config,
            name=name,
        )
        self.client = client
        self.guild = guild
        self.ask_move_msg = ask_move_msg
        self.channel_pattern = channel_pattern
        self.channel_move_name = channel_move_name

    async def greet(self, member):
        if self.guild:
            # from the guild name attempt to get a channel name
            channel = None
            regex = re.compile(self.channel_pattern)
            for t in self.guild.text_channels:
                if regex.match(t.name):
                    channel = t
            channel = member if not channel else channel
            # from channel attempt to mention a member
            msg = await channel.send(str(self.config))
            self._ask_move(member, channel)

            return msg
        else:
            raise Exception("greeting failure guild not found")

    async def _ask_move(self, member, channel=None):
        await channel.send(self.ask_move_msg)

        def check_auth_content(m):
            if m.author == member.author:
                if re.match("(?i)^(yes|y|n|no)( |)", m.content):
                    return True
                else:
                    asyncio.ensure_future(channel.send(' "yes" or "no" '))
            return False

        msg = await self.client.wait_for("message", check=check_auth_content)
        if re.match("(?i)^(yes|y)( |)", msg.content):
            for c in self.guild.voice_channels:
                if c.name == self.channel_move_name:
                    invite = await c.create_invite()
                    await channel.send("awsome.hella lit. check your DMs")
                    invite_msg = f"""Thankyou {member.name} for joining 
                    {self.guild.name} 
                    please follow the link below for interview channel\n\n"""
                    invite_msg += invite.url
                    await member.send(invite_msg)
        else:
            await channel.send("wow ok . not cool. @everyone look at this guy")
