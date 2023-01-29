from slack_sdk.errors import SlackApiError
from slack_sdk.models.blocks.basic_components import MarkdownTextObject, PlainTextObject
from slack_sdk.models.blocks.block_elements import ButtonElement
from slack_sdk.models.blocks.blocks import SectionBlock
from slack_sdk.models.messages import ObjectLink
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.say.async_say import AsyncSay

from door.decorators import message
from door.models.messages.message import Message
from door.plugins.base import DoorBasePlugin

from sentry_sdk import start_transaction, start_span


class PingPongPlugin(DoorBasePlugin):
    """The "Hello World" of bot features"""

    @message(r"^ping$")
    async def listen_for_ping(self, message: dict, client: AsyncWebClient, context: AsyncBoltContext) -> Message | None:
        """ping: Listen for "ping" and respond with a reaction"""

        self.logger.debug("Ping received")

        if not context.channel_id:
            self.logger.error("Unable to react to ping: no channel in context!")
            return

        with start_span(op="slack-api", description="reactions.add") as span:
            try:
                await client.reactions_add(channel=context.channel_id, timestamp=context["message_ts"], name="eyes")
            except SlackApiError as err:
                span.set_status("internal_error")
                self.logger.error(f"reactions.add: {err.response}", exc_info=True)
            else:
                span.set_status("ok")

    @message(r"^pong$")
    async def listen_for_pong(self, message: dict, context: AsyncBoltContext) -> Message | None:
        """pong: Listen for "pong" and respond with an ephemeral reply"""

        self.logger.debug("Pong received")

        return Message(text="Ping!", ephemeral=True, context=context)


class HelloPlugin(DoorBasePlugin):
    """Example plugin demonstrating how to use interactive features"""

    # Use 'init' to register for other event types (actions, etc.) directly
    def init(self, app: AsyncApp) -> None:
        app.action("hello_click_me_button_clicked")(self.action_hello_click_me_button_clicked)

    @message(r"^(?P<greeting>h(?:i|ello))")
    async def message_hello(self, message: dict, context: AsyncBoltContext) -> Message | None:
        """Be friendly and respond to to a "hi" or "hello" message"""
        self.logger.debug("'hello' received")

        text = f"Hey there {ObjectLink(object_id=message['user'])}! :wave:"
        return Message(
            thread_ts=context["conditional_thread_ts"],
            text=text,
            blocks=[
                SectionBlock(
                    text=MarkdownTextObject(text=text),
                    accessory=ButtonElement(text=PlainTextObject(text="Click Me"), action_id="hello_click_me_button_clicked"),
                )
            ],
        )

    async def action_hello_click_me_button_clicked(
        self, body: dict, ack: AsyncAck, say: AsyncSay, context: AsyncBoltContext
    ) -> None:
        # When somebody clicks the button, add a reply as a thread
        with start_transaction(op="event", name="hello_click_me_button_clicked") as transaction:
            # NOTE: since this is an action, it must be explicitly acknowledged, or Slack will retry sending it!
            await ack()

            try:
                await say(text=f"<@{body['user']['id']}> clicked the button!", thread_ts=context["always_thread_ts"])
            except SlackApiError as err:
                transaction.set_status("internal_error")
                self.logger.error(f"chat.postMessage: {err.response}", exc_info=True)
            else:
                transaction.set_status("ok")
