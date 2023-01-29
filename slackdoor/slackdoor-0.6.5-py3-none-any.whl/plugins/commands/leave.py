import asyncio
from door.utils import Plural

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError

from slack_bolt.context.async_context import AsyncBoltContext

from door.decorators import message
from door.plugins.base import DoorBasePlugin

from sentry_sdk import start_span


# NOTE: this plugin requires the bot to have the "channels:manage" scope
class LeaveChannelPlugin(DoorBasePlugin):
    """Ask the bot to leave a channel when mentioned"""

    @message(r"^leave$")
    async def listen_for_leave(self, message: dict, client: AsyncWebClient, context: AsyncBoltContext) -> str | None:
        """Leave a channel when specifically @-mentioned and told to 'leave'"""

        if not context.get("bot_mentioned"):
            return None

        with start_span(op="listen_for_leave", description="handler") as span:
            user_info, chan_info = await asyncio.gather(
                self.slack.get_user_info(message["user"]), self.slack.get_channel_info(message["channel"])
            )

            if chan_info.is_im:
                return "How am I supposed to leave a direct message? :thinking_face:"

            with start_span(op="say"):
                await context.say(
                    f"OK {user_info.first_name}, I'm leaving... :disappointed: Feel free to */invite* me back any time."
                )

            # Wait a few seconds for the message to be "delivered". This action requires the
            # bot to be explicitly mentioned, so leaving immediately can result in a message
            # from Slackbot saying: "You mentioned @botname, but they're not in this channel."
            with start_span(op="sleep"):
                await asyncio.sleep(3)

            with start_span(op="slack-api", description="leave") as inner_span:
                try:
                    await client.conversations_leave(channel=message["channel"])
                except SlackApiError as err:
                    inner_span.set_status("internal_error")
                    self.logger.error(f"conversations.leave: {err.response}", exc_info=True)
                    return None
                else:
                    inner_span.set_status("ok")

            span.set_status("ok")

            self.logger.warning(
                f"Leaving '{chan_info.name}' (had {Plural(chan_info.member_count):N member/s}) "
                f"at the request of @{user_info.display_name} ({user_info.id})"
            )

        return None
