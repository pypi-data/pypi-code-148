import asyncio
import logging
import re

from dataclasses import dataclass
from logging import Logger
from typing import Any, Awaitable, Callable, Mapping, Match, Sequence, NamedTuple

from case_insensitive_dict import CaseInsensitiveDict

from slack_bolt import BoltResponse
from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.say.async_say import AsyncSay

from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient

from door.plugins import PluginHandler
from door.utils.interactive import ephemeral_notification, generic_dismiss_message_button, ack_open_url_button
from door.models.files.file import File
from door.models.messages.message import Message, MultiMessage
from door.sentry import adjust_start
from door.slack import Slack
from door.utils import Plural, partial_mask

from sentry_sdk import start_transaction, start_span, set_user, set_tag, capture_exception


@dataclass(frozen=True, slots=True)
class MessageHandlerResponse:
    message: Message | None = None
    files: Sequence[File] | None = None

    def __bool__(self) -> bool:
        return self.message is not None or self.files is not None


# @dataclass(frozen=True, slots=True)
class Handler(NamedTuple):
    function: Awaitable[Any]
    fn_name: str


class EventDispatcher:
    """Process Slack events, and dispatch them to plugins as necessary"""

    def __init__(self, plugin_events: Mapping[str, list[PluginHandler]], settings: CaseInsensitiveDict) -> None:
        self._plugin_events = plugin_events

        self.slack = Slack.get_instance()
        self.logger = self.slack.logger
        self.app = self.slack.app

        if aliases := settings.get("ALIASES"):
            self.logger.info("Setting aliases to {aliases}")
            alias_regex = rf"|(?P<alias>{'|'.join([re.escape(s) for s in aliases.split(',')])})"
        else:
            self.logger.info("Not configuring any bot aliases")
            alias_regex = ""

        # This RE matches the beginning of a message, looking for:
        # - a "real" Slack @-mention (optionally followed by a [space] colon) -> bot_id
        # - some word characters followed by a colon (in case it's the bot's username) -> bot_name
        # - specific bot aliases -> alias
        # - the reminder of text after a mention -> text
        self.MENTION_MATCHER_RE = re.compile(
            rf"^\s*(?:<@(?P<bot_id>\w+)> ?:?|(?P<bot_name>\w+):{alias_regex}) ?(?P<text>.*)$", re.DOTALL
        )

    def start(self) -> None:
        # NOTE: the order these events are registered is the order they are evaluated

        self.logger.debug("Listening for '%s' events", "', '".join([*self._plugin_events]))

        # Register global middleware handlers
        # NOTE: Be careful with global middleware... they have to deal with ALL event types!
        self.app.middleware(self._skip_self_events)
        self.app.middleware(self._ignore_bot_message_events)
        self.app.middleware(self._add_door_context)

        # Register our special dispatchers with Bolt for new, deleted and changed  messages
        self.app.event({"type": "message", "subtype": (None, "me_message")}, middleware=[self._bot_mentioned])(
            self._dispatch_message
        )
        self.app.event({"type": "message", "subtype": "message_deleted"})(self._dispatch_message_deleted)
        self.app.event({"type": "message", "subtype": "message_changed"})(self._dispatch_message_changed)
        self.app.event({"type": "message", "subtype": "file_share"})(self._dispatch_file_share)
        # This _message_ handler needs to be last: it acknowledges all the message subtypes we _don't_ care about
        self.app.event("message", middleware=[self._extract_subtype])(self._ack_other_message_subtypes)

        self.app.event("link_shared")(self._dispatch_link_shared)

        # we need to process all these events so we can keep our local caches up-to-date :grimacing:
        # TODO: as of now, plugins cannot subscribe to these events; would need to "synthesize" them
        #       like we do for other events so multiple plugins are able to process them individually
        self.app.event("user_change")(self.slack._process_user_change)
        self.app.event("team_join")(self.slack._process_team_join)
        self.app.event("channel_created")(self.slack._process_channel_created)
        self.app.event(re.compile(r"^(channel|group)_deleted"))(self.slack._process_channel_deleted)
        self.app.event(re.compile(r"^(channel|group)_(rename|archive|unarchive)"))(self.slack._process_channel_changed)
        self.app.event("channel_id_changed")(self.slack._process_channel_id_changed)
        self.app.event("member_left_channel")(self.slack._process_member_left_channel)
        # this one is special because plugins may want to trigger on this event
        # self.slack._process_member_joined_channel is called directly from _dispatch_member_joined_channel
        self.app.event("member_joined_channel")(self._dispatch_member_joined_channel)

        # register a couple actio handlers for convenience
        self.app.action("generic_dismiss_message_button")(generic_dismiss_message_button)
        self.app.action("ack_open_url_button")(ack_open_url_button)

        # Finally register any events the plugins want
        for event_type, handler in self._plugin_events.items():
            self.logger.info(
                f"""'{event_type}' has {Plural(len(handler)):N listener/s}: '{"', '".join([h.fn_name for h in handler])}'"""
            )
            if event_type not in (
                "message",
                "link_shared",
                "message_deleted",
                "message_changed",
                "file_share",
                "member_joined_channel",
            ):
                # it's not one of our "synthetic" event dispatchers, register the (first, and only) handler directly
                # with Bolt (enforcement of a single handler is done in core._register_plugin_listeners)
                self.app.event(event_type)(handler[0].function)

        # Configure a custom error handler
        self.app.error(self._custom_error_handler)

    @staticmethod
    async def _custom_error_handler(error: Exception, body: dict, logger: Logger) -> None:
        logger.exception("Uncaught exception: %s", error)
        capture_exception(error)

    # Middleware methods start here

    @staticmethod
    async def _skip_self_events(body: dict, context: AsyncBoltContext, logger: Logger, next_: Callable) -> BoltResponse:
        """
        Global middleware that replaces default "self event skip" middleware to allow customizing events to pass
        """
        keep_events = ["member_joined_channel", "member_left_channel"]
        keep_message_subtypes = ["message_deleted", "file_share"]

        auth_result = context.authorize_result
        # message events can have event.bot_id while not having the bot's user_id
        bot_id = body.get("event", {}).get("bot_id")
        if (
            auth_result is not None
            and (
                (context.user_id is not None and context.user_id == auth_result.bot_user_id)
                or (bot_id is not None and bot_id == auth_result.bot_id)  # for bot_message events
            )
            and body.get("event") is not None
            and body.get("event", {}).get("type") not in keep_events
            and (
                body.get("event", {}).get("type") != "message" or body.get("event", {}).get("subtype") not in keep_message_subtypes
            )
        ):
            logger.debug("Skipping self-event: %r", body)
            return await context.ack()
        else:
            return await next_()

    @staticmethod
    async def _ignore_bot_message_events(body: dict, context: AsyncBoltContext, logger: Logger, next_: Callable) -> BoltResponse:
        """
        Global middleware to skip events from other bots
        """
        event = body.get("event", {})
        if event.get("type") == "message":
            # we want to see our own own "message_deleted" events
            is_bot_message = event.get("subtype") != "message_deleted" and (
                event.get("bot_id") is not None or event.get("message", {}).get("bot_id") is not None
            )
            is_slackbot_message = event.get("user") == "USLACKBOT"
            is_classic_bot_message = event.get("subtype") == "bot_message"
            if is_bot_message or is_classic_bot_message or is_slackbot_message:
                # just acknowledge the event
                logger.debug("Skipped 'message' event from bot user: %r", event)
                with start_transaction(op="event", name="ignored_bot_message") as txn:
                    txn.set_status("ok")
                    return BoltResponse(status=200, body="")
        return await next_()

    @staticmethod
    async def _add_door_context(body: dict, context: AsyncBoltContext, logger: Logger, next_: Callable) -> BoltResponse:
        """
        Global middleware to augment 'context' on every event

        FIXME: There are a lot of places that try to extract a channel or user ID that could/should
        probably just rely on getting the info from "the context" so it is consistent.

        The default context also contains 'authorize_result', which is exposed as properites:
        context.user_id, context.bot_token, context.bot_id, context.bot_user_id, context.user_token
        among other things
        """

        event = body.get("event", {})

        # from https://api.slack.com/events/message.channels (and other types),
        # 'channel_type' can be: channel, group, mpim, im
        context["channel_type"] = event.get("channel_type")

        # 'user_id' is set in the context by extract_user_id() (see slack_bolt/request/internals.py)
        set_user({"id": context.user_id})
        set_tag("channel", context.channel_id)

        if event and context.user_id is None and event.get("type") not in ("channel_created", "channel_rename", "file_deleted"):
            with start_transaction(op="event", name=event.get("type")):
                with start_span(op="debug", description="context missing user_id") as span:
                    span.set_data("event", event)
                logger.warning("Context does not contain 'user_id'")

        # timestamps
        if message := event.get("message"):  # FIXME: or (message := body.get("message") ???
            # if there's "message" data included, use that for ts/thread_ts data
            # (e.g. for "message_changed" events, interactive events, etc.)
            ts = message.get("ts")
            thread_ts = message.get("thread_ts")
        elif event.get("type") == "message":
            ts = event.get("ts")
            thread_ts = event.get("thread_ts")
        else:
            ts = event.get("message_ts")
            thread_ts = ts

        # useful for adding reactions to a message
        context["message_ts"] = ts
        # don't make a new thread, but reply in thread if that's where the message was
        context["conditional_thread_ts"] = thread_ts
        # create a new thread (or reply in existing thread)
        context["always_thread_ts"] = thread_ts or ts

        logger.debug(
            "Context: (type=%r) user_id=%r channel=%r message_ts=%r conditional_thread_ts=%r",
            event.get("type", "???") + ("/" + event["subtype"] if event.get("subtype") else ""),
            context.user_id,
            context.channel_id,
            context["message_ts"],
            context["conditional_thread_ts"],
        )

        # context["is_thread"] = bool(thread_ts)
        # context["is_parent"] = bool(ts and thread_ts and ts == thread_ts)
        # context["is_reply"] = bool(ts and thread_ts and ts != thread_ts)
        return await next_()

    @staticmethod
    async def _extract_subtype(body: dict, context: AsyncBoltContext, next_: Callable) -> BoltResponse:
        """
        Middleware used by the "catch all" message handler to ack subtypes we don't care about
        """
        context["subtype"] = body.get("event", {}).get("subtype")
        return await next_()

    # Example: "text":"<@U01AB12XYZ> pong" or "text":"botname: pong"
    async def _bot_mentioned(self, message: dict, context: AsyncBoltContext, logger: Logger, next_: Callable) -> BoltResponse:
        """
        Middleware for 'message' events that checks if the bot was "mentioned",
        as defined by "MENTION_MATCHER_RE
        """
        # assume the bot was not mentioned
        mentioned = False

        mentioned_match = self.MENTION_MATCHER_RE.match(message.get("text", ""))
        if mentioned_match:
            matches = mentioned_match.groupdict()
            bot_id_match = matches.get("bot_id")
            bot_name_match = matches.get("bot_name")
            alias_match = matches.get("alias")
            text_without_mention = matches.get("text", "")

            if alias_match:
                bot_id_match = context.bot_user_id

            if bot_id_match == context.bot_user_id or bot_name_match == self.slack.bot_name:
                message["text"] = text_without_mention

            mentioned = True

        # a DM with the bot can be assumed to be "mentioned"
        context["bot_mentioned"] = context["channel_type"] == "im" or mentioned
        return await next_()

    # Event handler methods start here

    @staticmethod
    def _preprocess_message_text(text: str | None) -> tuple[str, list[str], list[str]]:
        """
        Pre-process the text portion of a Slack message, removing codeblocks and backticks
        """
        if not text:
            return "", [], []

        codeblocks: list[str] = []
        backticks: list[str] = []

        def _get_next_code_block(m: Match[str]) -> str:
            codeblocks.append(m.group(1))
            return ""

        def _get_next_backtick_block(m: Match[str]) -> str:
            backticks.append(m.group(1))
            return ""

        # strip any leading/trailing spaces
        text = text.strip()

        # delete anything in code blocks and backticks (a good way to prevent the bot from "seeing" things!)
        text = re.sub(r"```(.+?)```", _get_next_code_block, text, flags=re.DOTALL)
        text = re.sub(r"`(.+?)`", _get_next_backtick_block, text)

        # Slack encodes &, < and > because they are used internally... which means we can't match on "&"
        # FIXME: what could go wrong by doing this?
        text = text.replace("&amp;", "&")

        return text, codeblocks, backticks

    async def _process_message_handlers(
        self, text: str, message: dict[str, Any], client: AsyncWebClient, context: AsyncBoltContext, logger: Logger
    ) -> MessageHandlerResponse | None:
        """
        Given a message event, process it for triggers and return the response(s)
        """

        handlers: list[Handler] = []
        for listener in self._plugin_events["message"]:
            matcher = listener.regex
            if not matcher:
                logger.error(f"message handler {listener.class_name}:{listener.fn_name} has no regex")
                continue

            # logger.debug(f"Checking if {text=} matches r'{matcher.pattern}'")
            if "(?P<" in matcher.pattern:
                # if there's one named capture group, assume all the capture groups are named
                if match := [m.groupdict() for m in matcher.finditer(text)]:
                    if "(?#Multi)" in matcher.pattern:
                        # multiple occurrences of the matches in "text" are accepted by
                        # the plugin, so sent down an array named "matches"
                        # (no need to send down duplicates, so remove any first!)
                        kwargs = {"matches": list({frozenset(m.items()): m for m in match}.values())}
                    else:
                        # multiples not expected by the plugin, so pass first set as named kwargs
                        kwargs = match[0]
                else:
                    kwargs = {}
            else:
                # no named patterns, get a tuple of the matching element(s) and pass to
                # listener as "match" or "matches"
                if match := matcher.search(text):
                    groups = match.groups()
                    if len(groups) == 0:
                        # no capture groups
                        kwargs = {}
                    elif len(groups) == 1:
                        # one unnamed capture group
                        kwargs = {"match": groups[0]}
                    else:
                        # multiple, unnamed capture groups
                        kwargs = {"matches": groups}
                else:
                    kwargs = {}

            if match:
                # add the listener that had a matching regex, passing the named regex groups
                # logger.debug(f"{text} matched r'{matcher.pattern}', adding handler '{listener.fn_name}'")
                handlers.append(
                    Handler(
                        function=listener.function(message=message, client=client, context=context, **kwargs),
                        fn_name=listener.fn_name,
                    )
                )

        if not handlers:
            # nothing to do, no message handlers matched
            return

        message_responses: list[Message] = []
        file_responses: list[File] = []

        # call all the listeners that matched
        with start_span(op="process_message", description="handlers") as span:
            plugin_responses = await asyncio.gather(*[h.function for h in handlers])
            span.set_data(
                "data",
                {
                    "handlers": [h.fn_name for h in handlers],
                    "text": text,
                    "plugin_response_count": len([resp for resp in plugin_responses if resp]),
                },
            )

            # separate response into messages and files
            for response in plugin_responses:
                if isinstance(response, Message):
                    message_responses.append(response)
                elif isinstance(response, File):
                    file_responses.append(response)
                elif response is None:  # noqa: RET507
                    # A handler didn't have anything to return
                    continue
                else:
                    span.set_data("message", response)
                    logger.warning(f"Unexpected message handler response type: {type(response)}")

        # process Message(s), including joining multiple Message responses into one, if necessary
        if not any(message_responses):
            # listeners were triggered, but none had anything to send as a response
            message_response = None
            message_response_count = 0
        elif len(message_responses) == 1:
            # a single message response is quite common, use it "as is"
            message_response = message_responses[0]
            message_response_count = 1
        else:
            # need to merge multiple message responses
            message_response_count = 0
            mm = MultiMessage()
            for msg in message_responses:
                message_response_count += 1
                mm.add(message=msg)

            # FIXME: how to handle this during an edit? :grimacing:
            if mm.has_ephemeral_content:
                ephemeral_response = mm.join_ephemeral(divide_blocks=True, context=context)
                if ephemeral_response:
                    await ephemeral_response.post_ephemeral(client)

            message_response = mm.join(divide_blocks=True) if mm.has_content else None

        # If we got this far, we have one message (possibly joined from multiple messages), and
        # possibly one (or more) files

        user_info, chan_info = await asyncio.gather(
            self.slack.get_user_info(context.user_id), self.slack.get_channel_info(context.channel_id)
        )

        # All this code for a nice one-line log message!
        if logger.isEnabledFor(logging.INFO):
            if message_response_count:
                messages_log_msg = f"{Plural(message_response_count):N message/s}"
            else:
                messages_log_msg = "no messages"

            if files_response_count := len(file_responses):
                files_log_msg = f"{Plural(files_response_count):N file/s} uploaded"
            else:
                files_log_msg = None

            if message_response_count and files_log_msg:
                results_log_msg = f"{messages_log_msg} and {files_log_msg}"
            elif files_log_msg:
                results_log_msg = files_log_msg
            else:
                results_log_msg = messages_log_msg

            logger.info(
                f"message event in #{chan_info.name} from @{user_info.display_name} triggered "
                f"""'{"'+'".join([h.fn_name for h in handlers])}' with {text=}; resulted in """
                f"{results_log_msg}"
            )

        # a single (possibly joined from multiple handlers) message, but possibly multiple files
        return MessageHandlerResponse(message=message_response, files=file_responses)

    async def _post_new_message(
        self,
        trigger_text: str,
        response: str | dict[str, Any] | Message,
        ts: str,
        say: AsyncSay,
        client: AsyncWebClient,
        context: AsyncBoltContext,
        logger: Logger,
    ) -> None:
        """
        Helper function to post a message, and call any 'message_callback' handlers
        """

        # Notes on sending messages via "say()":
        #     text: Union[str, dict] = "",
        #     blocks: Optional[Sequence[Union[dict, Block]]] = None,
        #     attachments: Optional[Sequence[Union[dict, Attachment]]] = None,
        #     channel: Optional[str] = None,
        #     thread_ts: Optional[str] = None,
        # if "text" is a string, say passes the text, blocks & attachments to chat.postMessage
        # if "text" is a dict, say passes unpacks the dict and sends it to chat.postMessage
        # (channel is honored if included, otherwise defaults to "self.channel")

        api_response = None
        if isinstance(response, (str, dict)):
            api_call = "chat.postMessage"
            with start_span(op="slack-api", description=api_call):
                api_response = await say(text=response, thread_ts=ts)
        elif isinstance(response, Message):
            if response.ephemeral:
                api_call = "chat.postEphemeral"
                api_response = await response.post_ephemeral(client)
            elif response.has_content:
                # unpack the Message into text, block, attachments, thread_ts...
                message_as_dict = response.to_dict()
                api_call = "chat.postMessage"
                with start_span(op="slack-api", description=api_call) as span:
                    if context["conditional_thread_ts"] and "thread_ts" not in message_as_dict:
                        span.set_data("message_as_dict", message_as_dict)
                        logger.warning("Message response in a thread didn't include 'thread_ts'")
                        message_as_dict["thread_ts"] = ts
                    logger.debug("chat.postMessage called with %s", message_as_dict)
                    api_response = await say(**message_as_dict)
            else:
                api_call = None
        else:
            logger.error("Unexpected 'message' plugin response, not sending")
            return

        if api_response:
            # FIXME: what if a handler didn't return anything? :thinking_face:
            for handler in self._plugin_events.get("message_callback", []):
                # call any message_callback handlers
                await handler.function(api_call, trigger_text, api_response, context)

    async def _upload_new_files(
        self,
        trigger_text: str,
        files: Sequence[File],
        ts: str,
        client: AsyncWebClient,
        context: AsyncBoltContext,
        logger: Logger,
    ) -> None:
        """
        Helper function to upload file(s), and call any 'message_callback' handlers
        """

        file_uploads = []
        initial_comments = []

        for file in files:
            if not isinstance(file, File):
                logger.error("Unexpected file upload type")
                continue

            # make a list of files to upload
            file_uploads.append(
                {
                    "filename": file.filename,
                    "content": file.content,
                    "file": file.file,
                    "title": file.title,
                    "snippet_type": file.snippet_type,
                }
            )
            if file.initial_comment:
                initial_comments.append(file.initial_comment)

        with start_span(op="slack-api", description="files.upload_v2") as span:
            try:
                # NOTE: `files_upload_v2` exists because of reliability problems with `file_upload`
                # (but DOES NOT reliably return `files.info` data when complete so don't bother)
                api_response = await client.files_upload_v2(
                    file_uploads=file_uploads,
                    channel=context.channel_id,
                    thread_ts=ts,
                    initial_comment=" • ".join(initial_comments),
                    request_file_info=False,
                )
            except SlackApiError as err:
                span.set_status("internal_error")
                logger.error(f"files.upload_v2: {err.response}", exc_info=True)
                return
            else:
                span.set_status("ok")

        if api_response:
            # FIXME: what if a handler didn't return anything? :thinking_face:
            for handler in self._plugin_events.get("message_callback", []):
                # call any message_callback handlers
                await handler.function("files.upload_v2", trigger_text, api_response, context)

    async def _update_old_message(
        self,
        trigger_text: str,
        message: str | dict[str, Any] | Message,
        chan_id: str,
        ts: str,
        client: AsyncWebClient,
        context: AsyncBoltContext,
        logger: Logger,
    ) -> None:
        """
        Helper function to update a message, and call any 'message_callback' handlers
        """
        api_response = None

        def fix_up_message(message: dict[str, Any]) -> dict[str, Any]:
            # 'channel' and 'ts' are required for chat.update
            if "channel" not in message:
                message["channel"] = chan_id
            if "ts" not in message:
                message["ts"] = ts
            # explicitly "empty" these so they are removed
            if message.get("text") is None:
                message["text"] = ""
            if message.get("attachments") is None:
                message["attachments"] = []
            if message.get("blocks") is None:
                message["blocks"] = []
            return message

        if isinstance(message, str):
            with start_span(op="slack-api", description="chat.update"):
                api_response = await client.chat_update(channel=chan_id, text=message, ts=ts)
        elif isinstance(message, dict):
            message = fix_up_message(message)
            with start_span(op="slack-api", description="chat.update"):
                api_response = await client.chat_update(**message)
        elif isinstance(message, Message):
            if message.ephemeral:
                await message.post_ephemeral(client)
            elif message.has_content:
                # unpack the Message into text, block, attachments, thread_ts...
                message_as_dict = fix_up_message(message.to_dict())
                with start_span(op="slack-api", description="chat.update"):
                    logger.debug("chat.update called with %s", message_as_dict)
                    api_response = await client.chat_update(**message_as_dict)
        else:
            logger.error("Unexpected 'message' plugin response, not sending")

        if api_response:
            # FIXME: what if a handler didn't return anything? :thinking_face:
            for handler in self._plugin_events.get("message_callback", []):
                # call any message_callback handlers
                await handler.function("chat.update", trigger_text, api_response, context)

    async def _dispatch_message(
        self, message: dict[str, Any], say: AsyncSay, client: AsyncWebClient, context: AsyncBoltContext, logger: Logger
    ) -> None:
        """
        Process 'message' events (including the 'me_message" subtype)
        See https://api.slack.com/events/message
        """

        with start_transaction(op="event", name="message") as txn:
            if message.get("event_ts"):
                # Set the transaction start to the event timestamp to track Slack latency
                adjust_start(message["event_ts"], txn)

            # FIXME: save codeblocks and backticks in "context"?
            # TODO: add code to warn user (via ephemeral message) when they have an excessively long codeblocks/backticks
            extracted_text, codeblocks, backticks = self._preprocess_message_text(message.get("text"))

            if extracted_text:
                # found some text to look at, call the registered message handlers and see if we get anything we need post/upload
                if response := await self._process_message_handlers(
                    text=extracted_text, message=message, client=client, context=context, logger=logger
                ):
                    if response.message:
                        # process the (possibly merged) message from the message handlers
                        # include 'conditonal_thread_ts' in case response is 'str' (or 'dict' that doesn't include a 'ts')
                        await self._post_new_message(
                            extracted_text, response.message, context["conditional_thread_ts"], say, client, context, logger
                        )

                    if response.files:
                        # process the file(s) from the message handlers
                        await self._upload_new_files(
                            extracted_text, response.files, context["conditional_thread_ts"], client, context, logger
                        )

            txn.set_status("ok")

    async def _dispatch_message_deleted(
        self,
        event: dict[str, Any],
        client: AsyncWebClient,
        context: AsyncBoltContext,
        logger: Logger,
    ) -> None:
        """
        Process 'message_deleted' message subtype events
        See https://api.slack.com/events/message/message_deleted
        """

        with start_transaction(op="event", name="message_deleted") as txn:
            if event.get("event_ts"):
                # Set the transaction start to the event timestamp to track Slack latency
                adjust_start(event["event_ts"], txn)

            handlers: list[Handler] = []
            for listener in self._plugin_events.get("message_deleted", []):
                handlers.append(
                    Handler(function=listener.function(event=event, client=client, context=context), fn_name=listener.fn_name)
                )

            if not handlers:
                logger.debug("No handlers defined for 'message_deleted' event")
                txn.set_status("unknown")
                return

            with start_span(op="process_message_deleted", description="handlers") as span:
                # call all the listeners that matched
                plugin_responses = await asyncio.gather(*[h.function for h in handlers])
                span.set_data(
                    "data",
                    {
                        "handlers": [h.fn_name for h in handlers],
                        "plugin_response_count": len([resp for resp in plugin_responses if resp]),
                    },
                )

            txn.set_status("ok")

    async def _dispatch_file_share(
        self,
        event: dict[str, Any],
        client: AsyncWebClient,
        context: AsyncBoltContext,
        logger: Logger,
    ) -> None:
        """
        Process 'file_share' message subtype events
        See https://api.slack.com/events/message/file_share
        """

        with start_transaction(op="event", name="file_share") as txn:
            if event.get("event_ts"):
                # Set the transaction start to the event timestamp to track Slack latency
                adjust_start(event["event_ts"], txn)

            handlers: list[Handler] = []
            for listener in self._plugin_events.get("file_share", []):
                handlers.append(
                    Handler(function=listener.function(event=event, client=client, context=context), fn_name=listener.fn_name)
                )

            if not handlers:
                logger.debug("No handlers defined for 'file_share' event")
                txn.set_status("unknown")
                return

            with start_span(op="process_file_share", description="handlers") as span:
                # call all the listeners that matched
                plugin_responses = await asyncio.gather(*[h.function for h in handlers])
                span.set_data(
                    "data",
                    {
                        "handlers": [h.fn_name for h in handlers],
                        "plugin_response_count": len([resp for resp in plugin_responses if resp]),
                    },
                )

            txn.set_status("ok")

    async def _message_count_since_original(self, event: dict[str, Any], client: AsyncWebClient) -> int | None:
        """
        get the number of messages that have been sent to the channel (or
        thread) since the user's original message
        """

        api_args = {
            "channel": event["channel"],
            "limit": 5,
            "oldest": event["message"]["ts"],
            "include_all_metadata": False,
        }
        if thread_ts := event["message"].get("thread_ts"):
            api_variant = "replies"
            api_method = client.conversations_replies
            api_args["ts"] = thread_ts
        else:
            api_variant = "history"
            api_method = client.conversations_history

        with start_span(op="http.client", description=f"conversations.{api_variant}") as span:
            try:
                # request the number of messages in the channel or thread since the edited message
                api_response = await api_method(**api_args)
            except SlackApiError as err:
                span.set_status("internal_error")
                self.logger.error(f"conversations.{api_variant} {err.response}", exc_info=True)
                api_response = None
            else:
                span.set_status("ok")

        if api_response and api_response.get("ok"):
            if (messages := api_response.get("messages")) is not None:
                count = len(messages)
                # account for conversatons.replies including the parent message
                return count - 1 if thread_ts else count

        return None

    async def _dispatch_message_changed(
        self,
        event: dict[str, Any],
        say: AsyncSay,
        client: AsyncWebClient,
        context: AsyncBoltContext,
        logger: Logger,
    ) -> None:
        """
        Process 'message_changed' message subtype events
        See https://api.slack.com/events/message/message_changed
        """

        with start_transaction(op="event", name="message_changed") as txn:
            if event.get("event_ts"):
                # Set the transaction start to the event timestamp to track Slack latency
                adjust_start(event["event_ts"], txn)

            if not (message := event.get("message")) or not event.get("previous_message") or not (chan_id := event.get("channel")):
                with start_span(op="debug", description="malformed event") as span:
                    span.set_data("event", event)
                self.logger.error("Received malformed 'message_changed' event")
                return

            prev_text, prev_codeblocks, prev_backticks = self._preprocess_message_text(event["previous_message"].get("text"))
            new_text, codeblocks, backticks = self._preprocess_message_text(message.get("text"))

            # don't call 'message_changed' handlers when before/after "text" is the same (most likely from an unfurl)
            if prev_text == new_text:
                logger.debug("Skipping 'message_changed' event because 'text' didn't change")
                txn.set_status("ok")
                return

            # generate a list of handlers that want to know when a message was changed
            handlers: list[Handler] = []
            for listener in self._plugin_events.get("message_changed", []):
                handlers.append(
                    Handler(function=listener.function(event=event, client=client, context=context), fn_name=listener.fn_name)
                )

            if not handlers:
                # if there's nothing to handle message_changed events, skip any further processing
                # (such as processing the edited message)
                logger.debug("No handlers defined to process 'message_changed' event")
                txn.set_status("unknown")
                return

            # call the message changed handler(s)
            with start_span(op="process_message_changed", description="handlers") as span:
                # call all the listeners that matched
                # NOTE: message_changed handlers can return a dict
                plugin_responses = await asyncio.gather(*[h.function for h in handlers])
                span.set_data(
                    "data",
                    {
                        "handlers": [h.fn_name for h in handlers],
                        "plugin_response_count": len([resp for resp in plugin_responses if resp]),
                    },
                )

            # merge any dicts returned from the message_changed plugins, skipping any that didn't return anything
            plugin_response_dict = {k: v for d in plugin_responses if d for k, v in d.items()}

            # if message was changed... call the 'message' handlers to (possibly) build up a replacement message
            # note: don't want to call this _earlier_ because these handlers could have side effects, and we want
            # the 'message_changed' handlers above to see the "before" state of any changes
            if new_text and (
                response := await self._process_message_handlers(
                    text=new_text, message=message, client=client, context=context, logger=logger
                )
            ):
                self.logger.debug(
                    "Edited message (processed as new message) resulted in message response: %r and file responses: %r",
                    response.message,
                    response.files,
                )
            else:
                # set an empty response
                response = MessageHandlerResponse()

            if previous_response_ts := plugin_response_dict.get("previous_response_ts"):
                # we had previously generated a response to the original message, so we can just update it
                if response.message:
                    # the edited message generated a response; update the existing message
                    await self._update_old_message(
                        new_text, response.message, chan_id, previous_response_ts, client, context, logger
                    )
                else:
                    # the edited message did not generate a response, but we previously did, so delete it
                    with start_span(op="http.client", description="chat.delete") as span:
                        try:
                            await client.chat_delete(channel=chan_id, ts=previous_response_ts)
                        except SlackApiError as err:
                            span.set_status("internal_error")
                            self.logger.error(f"chat.delete: {err.response}", exc_info=True)
                        else:
                            span.set_status("ok")

                if response.files:
                    message_count = await self._message_count_since_original(event, client)
                    if message_count is not None and message_count <= 3:
                        # process the file(s) from the message handlers
                        await self._upload_new_files(
                            new_text, response.files, context["conditional_thread_ts"], client, context, logger
                        )
                    else:
                        text = (
                            "There have been too many messages since your original message, "
                            "so I'm not going to respond with the files from your edited message. "
                            "(If you really want my reply, you can delete your original message, and "
                            "re-post it as a new message.)"
                        )
                        await ephemeral_notification(text, context=context, client=client)

            elif response:  # the user's edit would mean a brand-new bot message

                message_count = await self._message_count_since_original(event, client)
                if message_count is not None and message_count <= 3:
                    # there's been 3 or less messages added to the channel since the edit, so add the new reply/files
                    # we pass 'conditional_thread_ts' in case the response is a 'str' (or 'dict' that doesn't include a 'ts')
                    if response.message:
                        # process the (possibly merged) message from the message handlers
                        # include 'conditonal_thread_ts' in case response is 'str' (or 'dict' that doesn't include a 'ts')
                        await self._post_new_message(
                            new_text, response.message, context["conditional_thread_ts"], say, client, context, logger
                        )

                    if response.files:
                        # process the file(s) from the message handlers
                        await self._upload_new_files(
                            new_text, response.files, context["conditional_thread_ts"], client, context, logger
                        )
                else:
                    text = (
                        "There have been too many messages since your original message, "
                        "so I'm not going to respond to your edited version. (If you really "
                        "want my reply, you can delete your edited message, and re-post it "
                        "as a new message.)"
                    )
                    await ephemeral_notification(text, context=context, client=client)

            txn.set_status("ok")

    async def _dispatch_member_joined_channel(
        self, event: dict[str, Any], say: AsyncSay, client: AsyncWebClient, context: AsyncBoltContext, logger: Logger, ack: AsyncAck
    ) -> None:
        """
        Process 'member_joined_channel' events (including when the bot gets invited to a channel)
        See https://api.slack.com/events/member_joined_channel
        """

        with start_transaction(op="event", name="member_joined_channel") as txn:
            if event.get("event_ts"):
                # Set the transaction start to the event timestamp to track Slack latency
                adjust_start(event["event_ts"], txn)

            # need to acknowledge all non-message events
            with start_span(op="http.client", description="ack") as span:
                await ack()
                span.set_status("ok")

            # always call our "internal" listener
            await self.slack._process_member_joined_channel(event)

            handlers: list[Handler] = []
            for listener in self._plugin_events.get("member_joined_channel", []):
                handlers.append(
                    Handler(
                        function=listener.function(event=event, client=client, context=context, say=say), fn_name=listener.fn_name
                    )
                )

            if not handlers:
                logger.debug("No handlers defined for 'member_joined_channel' event")
                txn.set_status("unknown")
                return

            with start_span(op="process_member_joined_channel", description="handlers") as span:
                # call all the listeners that matched
                plugin_responses = await asyncio.gather(*[h.function for h in handlers])
                span.set_data(
                    "data",
                    {
                        "handlers": [h.fn_name for h in handlers],
                        "plugin_response_count": len([resp for resp in plugin_responses if resp]),
                    },
                )

            txn.set_status("ok")

            if not any(plugin_responses):
                # listeners were triggered, but none had anything to send as a response
                return

    async def _dispatch_link_shared(
        self, event: dict[str, Any], client: AsyncWebClient, context: AsyncBoltContext, logger: Logger, ack: AsyncAck
    ) -> None:
        """
        Process 'link_shared' events
        See https://api.slack.com/events/link_shared
        """

        with start_transaction(op="event", name="link_shared") as txn:
            # NOTE: from https://api.slack.com/changelog/2021-08-changes-to-unfurls
            # The link_shared event will now be sent when a user types a link into the message composer,
            # in addition to when the message is sent to a channel. As part of this change, two new fields
            # will be included:
            #
            # `unfurl_id` which identifies the link and can be used to supply the chat.unfurl method
            # `source`, an enumerated string that tells you whether the event happened in composer
            # ("source": "composer") or in a sent message ("source": "conversations_history)
            #
            # chat.unfurl will continue to accept the combination of `channel` and `ts` you find in
            # link_shared events, even though they're not strictly channels or timestamps. You can
            # ALSO use the `unfurl_id` and `source` parameters (if you use one, you must use both
            # together) to call chat.unfurl

            if event.get("message_ts"):
                # Set the transaction start to the timestamp of the original message to track Slack latency
                adjust_start(event["message_ts"], txn)

            # need to acknowledge all non-message events
            with start_span(op="http.client", description="ack") as span:
                await ack()
                span.set_status("ok")

            links = event.get("links", [])

            handlers: list[Handler] = []
            for link in links:
                url = link.get("url", "")
                # note: URLs encode & to &amp ... if necessary could call html.unescape(url)
                for listener in self._plugin_events.get("link_shared", []):
                    matcher = listener.url_regex
                    if not matcher:
                        logger.error(f"link_shared handler {listener.class_name}:{listener.fn_name} has no URL regex")
                        continue

                    if match := matcher.search(url):
                        kwargs = match.groupdict()
                        # add the listener that had a matching regex, passing the named regex groups
                        handlers.append(
                            Handler(function=listener.function(url=url, context=context, **kwargs), fn_name=listener.fn_name)
                        )

            if not handlers:
                with start_span(op="handlers", description="unmatched") as span:
                    urls = []
                    for link in links:
                        urls.append(
                            re.sub(
                                r"^([^:/?#]+://[^/?#]+?(?:[/?#]|$))(.*)$",
                                lambda m: m.group(1) + partial_mask(m.group(2)),
                                link["url"],
                            )
                        )
                    span.set_data("unmatched_urls", urls)
                logger.info(f"No handlers matched for 'link_shared' event in #{event['channel']}: {urls=}")
                txn.set_status("unknown")
                return

            # link_shared handlers are expected to return a dict entry for the "unfurls" parameter
            # as described here: https://api.slack.com/reference/messaging/link-unfurling#unfurls_parameter
            with start_span(op="process_link_shared", description="handlers") as span:
                # call all the listeners that matched
                plugin_responses = await asyncio.gather(*[h.function for h in handlers])
                span.set_data(
                    "data",
                    {
                        "handlers": [h.fn_name for h in handlers],
                        "matched_urls": [link["url"] for link in links],
                        "unfurl_count": len([resp for resp in plugin_responses if resp]),
                    },
                )

            # merge all the unfurl responses from the handlers into a single dict, keyed on URL
            raw_unfurls = {}
            for response in plugin_responses:
                if response:
                    raw_unfurls.update(response)

            chan_id = event["channel"]

            log_msg = (
                f"'link_shared' in #{chan_id} triggered {Plural(len(handlers)):N handler/s}: "
                f"{' + '.join([h.fn_name for h in handlers])}; {links=}"
            )

            if not raw_unfurls:
                # listeners got triggered, but none had anything to send as a response
                txn.set_status("not_found")
                logger.info(f"{log_msg} (No unfurls returned)")
                return

            logger.info(f"{log_msg} ({Plural(len(raw_unfurls)):N unfurl/s} returned)")

            # The content of unfurls is limited compared to a message. From the API docs:
            #   Unlike chat.postMessage's attachments parameter, it does NOT expect a JSON
            #   array but instead, a hash keyed on the specific URLs you're offering an
            #   unfurl for. Each URL can have a SINGLE attachment, including message
            #   buttons. [But an array of "blocks" seems fine...]
            # Go through the responses from the plugins and finesse as necessary
            unfurls = {}
            for url, unfurl in raw_unfurls.items():
                if isinstance(unfurl, dict):
                    if blocks := unfurl.get("blocks"):
                        # ensure there's nothing else in the dict, such as a top-level "text" entry
                        unfurls[url] = {"blocks": blocks}
                    elif attachments := unfurl.get("attachments"):
                        unfurls[url] = attachments[0] if isinstance(attachments, list) else attachments
                    else:
                        # assume it's a "raw" attachment dict
                        unfurls[url] = unfurl
                else:
                    logger.error("Unrecognized unfurl content")

            with start_span(op="slack-api", description="chat.unfurl") as span:
                try:
                    await client.chat_unfurl(channel=chan_id, ts=event["message_ts"], unfurls=unfurls)
                except SlackApiError as err:
                    logger.info(f"chat.unfurl failed in {chan_id}")
                    span.set_status("internal_error")
                    capture_exception(err)
                else:
                    txn.set_status("ok")

    @staticmethod
    async def _ack_other_message_subtypes(context: AsyncBoltContext, logger: Logger) -> None:
        """Since we're subscribed to 'message' events, we get a bunch of message events with
        a 'subtype' we don't care about. These still need to be "processed" by our app so Bolt
        doesn't consider them an "unhandled request".
        """
        subtype = context.get("subtype", "???")
        with start_transaction(op="event", name=f"subtype_{subtype}") as txn:
            logger.debug("Ignoring message subtype %r event", subtype)
            txn.set_status("ok")
