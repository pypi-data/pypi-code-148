from logging import Logger
from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.respond.async_respond import AsyncRespond

from slack_sdk.models.blocks.basic_components import MarkdownTextObject, PlainTextObject
from slack_sdk.models.blocks.block_elements import ButtonElement
from slack_sdk.models.blocks.blocks import SectionBlock

from door.models.messages.message import Message

from sentry_sdk import start_transaction, start_span


async def ephemeral_notification(text: str, context: AsyncBoltContext, client: AsyncWebClient, button: str = "OK") -> None:
    """
    Convenience helper function to send an ephemeral message to a user (such
    as an error message) that has a button (defaults to "OK", but could be
    "Dismiss", etc.) that removes the ephemeral message.
    """
    await Message(
        text=text,
        blocks=[
            SectionBlock(
                text=MarkdownTextObject(text=text),
                accessory=ButtonElement(
                    text=PlainTextObject(text=button), style="primary", action_id="generic_dismiss_message_button"
                ),
            ),
        ],
        context=context,
    ).post_ephemeral(client)


# NOTE: the handler for this action is registered in dispatch:start()
async def generic_dismiss_message_button(ack: AsyncAck, respond: AsyncRespond, logger: Logger) -> None:
    with start_transaction(op="event", name="generic_dismiss_message_button"):
        # NOTE: since this is an action, it must be explicitly acknowledged, or Slack will retry
        await ack()

        with start_span(op="slack-api", description="respond") as span:
            try:
                await respond(delete_original=True)
            except SlackApiError as err:
                span.set_status("internal_error")
                logger.error(f"respond: {err.response}", exc_info=True)
            else:
                span.set_status("ok")


# NOTE: the handler for this action is registered in dispatch:start()
async def ack_open_url_button(ack: AsyncAck, respond: AsyncRespond, logger: Logger) -> None:
    with start_transaction(op="event", name="ack_open_url_button") as txn:
        # NOTE: URL buttons still need to be acknowledged
        await ack()

        txn.set_status("ok")
