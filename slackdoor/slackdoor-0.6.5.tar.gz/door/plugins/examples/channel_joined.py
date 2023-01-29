import asyncio


from slack_sdk.errors import SlackApiError
from slack_sdk.models.messages import ObjectLink
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.context.say.async_say import AsyncSay

from door.decorators import event
from door.plugins.base import DoorBasePlugin


class RestrictChannelInvitationsPlugin(DoorBasePlugin):
    """Restrict channels invites for the bot to just admins"""

    def init(self, app: AsyncApp) -> None:
        self.bot_admin_user_ids = self.settings.get("BOT_ADMIN_USER_IDS")
        if not self.bot_admin_user_ids:
            raise RuntimeError("No bot admins defined; disable plugin or add some in settings")
        if not isinstance(self.bot_admin_user_ids, (tuple, list)):
            raise RuntimeError("BOT_ADMIN_USER_IDS must be a tuple (or list)")

    @event("member_joined_channel")
    async def restrict_channel_invites(self, event: dict, say: AsyncSay, client: AsyncWebClient) -> None:
        # Only care when "we" join a channel
        if event.get("user") != self.slack.bot_user_id:
            return

        # run these two API requests together
        user_info, chan_info = await asyncio.gather(
            self.slack.get_user_info(event["inviter"]), self.slack.get_channel_info(event["channel"])
        )

        self.logger.info(f"Invited to #{chan_info.name} by @{user_info.name} ({user_info.id})")

        # allow bot admins to do the inviting
        if event["inviter"] in self.bot_admin_user_ids:
            return

        user_link = ObjectLink(object_id=event["inviter"])
        await say(f"Thanks for the invite {user_link}, but I'm not ready to join this channel! :wave:")

        await asyncio.sleep(1)

        try:
            await client.conversations_leave(channel=event["channel"])
        except SlackApiError as err:
            self.logger.error(f"conversations.leave: {err.response}", exc_info=True)
            return

        self.logger.warning(f"Leaving #{chan_info.name} after being invited by @{user_info.name} ({user_info.id})")
