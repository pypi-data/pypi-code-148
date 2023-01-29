import logging

from json import dumps
from typing import Any, Sequence
from urllib.parse import quote

from slack_bolt.context.async_context import AsyncBoltContext

from slack_sdk.errors import SlackApiError
from slack_sdk.models import extract_json
from slack_sdk.models.attachments import Attachment, BlockAttachment
from slack_sdk.models.basic_objects import JsonObject, JsonValidator
from slack_sdk.models.blocks import Block
from slack_sdk.models.blocks.blocks import DividerBlock
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse

from sentry_sdk import start_span

logger = logging.getLogger(__name__)


class Message(JsonObject):
    attachments_max_length: int = 100
    blocks_max_length: int = 50
    # the set of attributes that will make up its JSON structure
    attributes: set[str] = {
        "text",
        "attachments",
        "blocks",
        "markdown",
        "thread_ts",
        "channel",
        "user",
        "unfurl_links",
        "parse",
    }

    def __init__(
        self,
        *,
        text: str | None = None,
        attachments: Sequence[Attachment] | None = None,
        blocks: Sequence[Block] | None = None,
        markdown: bool | None = None,
        thread_ts: str | None = None,
        channel: str | None = None,
        user: str | None = None,
        unfurl_links: bool | None = None,
        parse: bool | None = None,
        # https://api.slack.com/reference/surfaces/formatting
        # unfurl media?
        # reply_broadcast?
        # metadata?
        context: AsyncBoltContext | None = None,
        ephemeral: bool | None = None,
    ) -> None:
        """
        Create a message
        https://api.slack.com/messaging/composing#message-structure

        Args:
            text: Plain or Slack Markdown-like text to display in the message.
            attachments: A list of Attachment objects to display after the rest of
                the message's content. More than 20 is not recommended, but the actual
                limit is 100
            blocks: A list of Block objects to attach to this message. If
                specified, the 'text' property is ignored (more specifically, it's used
                as a fallback on clients that can't render blocks)
            markdown: Whether to parse markdown into formatting such as
                bold/italics, or leave text completely unmodified.
            thread_ts: When specified, replies to the thread instead of a new message
            channel: Override the channel when the message should be sent
            ephemeral: Whether or not this message should be sent ephemerally
            user: For an ephemeral message, the user_id the message is for
        """
        if not context:
            context = AsyncBoltContext()
        self.context = context

        self.text = text
        self.attachments = attachments or []
        self.blocks = blocks or []
        self.markdown = markdown
        # override the values from 'context', if specified
        if thread_ts:
            self.thread_ts = thread_ts
        if channel:
            self.channel = channel
        if user:
            self.user = user
        self.unfurl_links = unfurl_links
        self.parse = parse
        self.ephemeral = ephemeral

    @property
    def context(self) -> AsyncBoltContext:
        return self._context

    @context.setter
    def context(self, context: AsyncBoltContext) -> None:
        """When updating the 'context' of a Message, update thread_ts, channel and user"""
        self._context = context
        self.thread_ts = context.get("conditional_thread_ts")
        self.channel = context.channel_id
        self.user = context.user_id

    def __bool__(self) -> bool:
        return bool(self.has_content or self.ephemeral)

    @property
    def has_content(self) -> bool:
        return bool(self.text or self.attachments or self.blocks)

    @JsonValidator(f"'attachments' attribute cannot exceed {attachments_max_length} items")
    def attachments_length(self) -> bool:
        return self.attachments is None or len(self.attachments) <= self.attachments_max_length

    @JsonValidator(f"'blocks' attribute cannot exceed {blocks_max_length} items")
    def blocks_length(self) -> bool:
        return self.blocks is None or len(self.blocks) <= self.blocks_max_length

    async def post_ephemeral(self, client: AsyncWebClient) -> AsyncSlackResponse | None:
        with start_span(op="slack-api", description="chat.postEphemeral") as span:
            try:
                api_response = await client.chat_postEphemeral(**self.to_dict())
            except SlackApiError as err:
                span.set_status("internal_error")
                logger.error(f"chat.postEphemeral: {err.response}", exc_info=True)
                return None
            else:
                span.set_status("ok")
        return api_response

    def to_dict(self) -> dict:
        json = super().to_dict()
        if self.text:
            if len(self.text) > 40000:
                logger.error("Message over 40,000 characters (will be truncated by Slack)")
        if self.parse is False:
            # "full" (which we refer to as True) is the default, so don't set unless it's False
            json["parse"] = "none"
        return json

    def to_blockkit_builder(self) -> str:
        """Extracts "blocks" from Message object and creates Block Kit Builder link"""
        builder_url = "https://app.slack.com/block-kit-builder/#"
        if self.blocks:
            blocks = {"blocks": extract_json(self.blocks)}
            return quote(builder_url + dumps(blocks), safe="/:?=&#")
        else:
            return "No blocks found"

    def __repr__(self) -> str:
        return super().__repr__()


class MultiMessage:
    def __init__(self) -> None:
        self.texts: list[str] = []
        self.blocks: list[tuple[str | None, Sequence[Block]]] = []
        self.attachments: list[Sequence[Attachment]] = []
        self.ephemeral_texts: list[str] = []
        self.ephemeral_blocks: list[tuple[str | None, Sequence[Block]]] = []
        self.ephemeral_attachments: list[Sequence[Attachment]] = []
        self.thread_ts: str | None = None
        self.channel: str | None = None
        self.user: str | None = None

    def add(self, *, message: Message | None) -> None:
        if not message:
            return

        # Log warnings about situations that should not happen
        if message.thread_ts:
            if self.thread_ts:
                if message.thread_ts != self.thread_ts:
                    logger.warning("MultiMessage.add() called with 'thread_ts' not matching previous 'thread_ts'")
            else:
                self.thread_ts = message.thread_ts
        if message.channel:
            if self.channel:
                if message.channel != self.channel:
                    logger.warning("MultiMessage.add() called with 'channel' not matching previous 'channel'")
            else:
                self.channel = message.channel
        if message.user:
            if self.user:
                if message.user != self.user:
                    logger.warning("MultiMessage.add() called with 'user' not matching previous 'user'")
            else:
                self.user = message.user

        if message.ephemeral:
            if message.attachments:
                self.ephemeral_attachments.append(message.attachments)
            if message.blocks:
                # text is the fallback for a block...
                self.ephemeral_blocks.append((message.text, message.blocks))
            elif message.text:
                self.ephemeral_texts.append(message.text)
        else:
            if message.attachments:
                self.attachments.append(message.attachments)
            if message.blocks:
                # text is the fallback for a block...
                self.blocks.append((message.text, message.blocks))
            elif message.text:
                self.texts.append(message.text)

    @property
    def has_content(self) -> bool:
        return bool(self.texts or self.blocks or self.attachments)

    @property
    def has_ephemeral_content(self) -> bool:
        return bool(self.ephemeral_texts or self.ephemeral_blocks or self.ephemeral_attachments)

    @staticmethod
    def _join(
        texts_in: list[str],
        blocks_in: list[tuple[str | None, Sequence[Block]]],
        attachments_in: list[Sequence[Attachment]],
        divide_blocks: bool | None,
    ) -> tuple[str | None, Sequence[Block], Sequence[Attachment]]:
        # FIXME: try to de-dupe things? (probably easier to leave that up to the plugins...)

        blocks: list[Block] = []
        attachments: list[Attachment] = []

        # combine all the text parts
        texts = "\n".join(texts_in)

        # combine blocks, optionally with a divider between them, and deal with their "text"
        if blocks_in:
            # process the first block
            block_text, block = blocks_in.pop(0)
            if block_text is None:
                block_text = ""
            blocks.extend(block)
            # then process any additional blocks
            for text, block in blocks_in:
                block_text += f"\n{text}"
                if divide_blocks:
                    blocks.append(DividerBlock())
                blocks.extend(block)

            if texts:
                # we have "bare" text messages AND blocks. Since the "text" element of a Block
                # is considered the "fallback", we have to convert the blocks to an attachment
                # (and hope Slack doesn't deprecate those!) FIXME: For now, the fallback text from
                # the blocks are ignored, since BlockAttachment doesn't accept a fallback arg.
                attachments = [BlockAttachment(blocks=blocks)]
                blocks = []
            else:
                # no non-block text messages to deal with, so simply combine the texts from the
                # blocks (which are the "fallback" portion) and leave the blocks as blocks
                texts = block_text

        # combine the attachments (no dividers available)
        for attachment in attachments_in:
            attachments.extend(attachment)

        return texts, blocks, attachments

    def join(self, *, divide_blocks: bool | None = False, **kwargs: Any) -> Message | None:
        texts, blocks, attachments = self._join(self.texts, self.blocks, self.attachments, divide_blocks)

        if texts or blocks or attachments:
            message = Message(text=texts, blocks=blocks, attachments=attachments, **kwargs)

            if message.thread_ts:  # thread_ts was explicitly set via kwargs
                if self.thread_ts and message.thread_ts != self.thread_ts:
                    logger.warning("MultiMessage.join: 'thread_ts' kwarg does not match existing thread_ts")
            elif self.thread_ts:
                message.thread_ts = self.thread_ts

            if message.user:  # user was explicitly set via kwargs
                if self.user and message.user != self.user:
                    logger.warning("MultiMessage.join: 'user' kwarg does not match existing user")
            elif self.user:
                message.user = self.user

            if message.channel:  # channel was explicitly set via kwargs
                if self.channel and message.channel != self.channel:
                    logger.warning("MultiMessage.join: 'channel' kwarg does not match existing channel")
            elif self.channel:
                message.channel = self.channel

            return message

        return None

    def join_ephemeral(self, *, divide_blocks: bool | None = False, **kwargs: Any) -> Message | None:
        texts, blocks, attachments = self._join(
            self.ephemeral_texts, self.ephemeral_blocks, self.ephemeral_attachments, divide_blocks
        )

        if texts or blocks or attachments:
            # FIXME: do we need to be concerned about a user passing `ephemeral` in kwargs?
            message = Message(text=texts, blocks=blocks, attachments=attachments, ephemeral=True, **kwargs)

            if message.thread_ts:  # thread_ts was explicitly set via kwargs
                if self.thread_ts and message.thread_ts != self.thread_ts:
                    logger.warning("MultiMessage.join_ephemeral: 'thread_ts' kwarg does not match existing thread_ts")
            elif self.thread_ts:
                message.thread_ts = self.thread_ts

            if message.user:  # user was explicitly set via kwargs
                if self.user and message.user != self.user:
                    logger.warning("MultiMessage.join_ephemeral: 'user' kwarg does not match existing user")
            elif self.user:
                message.user = self.user

            if message.channel:  # channel was explicitly set via kwargs
                if self.channel and message.channel != self.channel:
                    logger.warning("MultiMessage.join_ephemeral: 'channel' kwarg does not match existing channel")
            elif self.channel:
                message.channel = self.channel

            return message

        return None
