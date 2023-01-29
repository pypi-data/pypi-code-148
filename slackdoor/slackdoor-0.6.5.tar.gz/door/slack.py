from __future__ import annotations  # will be default in 3.10

import asyncio
import logging
import re

from dataclasses import asdict
from logging import Logger
from typing import Any, cast

from case_insensitive_dict import CaseInsensitiveDict

from slack_sdk.errors import SlackApiError

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_sdk.socket_mode.async_client import AsyncBaseSocketModeClient
from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.version import __version__ as bolt_version

from door import __version__ as slackdoor_version
from door.models import Channel, User
from door.utils import Singleton, Plural, LoggingContext
from sentry_sdk import start_transaction, start_span


class Slack(metaclass=Singleton):
    __slots__ = "_settings", "_logger", "_proxy_url", "_client", "_app", "_handler", "_bot_info", "_users", "_channels"

    _settings: CaseInsensitiveDict
    _logger: Logger
    _proxy_url: str | None
    _client: AsyncWebClient
    _app: AsyncApp
    _handler: AsyncSocketModeHandler | None
    _bot_info: dict[str, Any]
    _users: dict[str, User]
    _channels: dict[str, Channel]

    def __init__(
        self,
        settings: CaseInsensitiveDict | None = None,
        logger: logging.Logger | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        if not logger:
            logger = logging.getLogger(__name__)
            logger.info("Using default logger")

        if not settings:
            logger.warning("No settings!")
            settings = CaseInsensitiveDict()

        if not loop:
            loop = asyncio.get_event_loop()

        self._settings = settings

        self._logger = logger

        self._proxy_url = settings.get("HTTPS_PROXY") or settings.get("HTTP_PROXY")

        if token := settings.get("SLACK_BOT_TOKEN"):
            # NOTE: AsyncWebClient (and AsyncApp) uses the "xoxb-..." token
            self._client = AsyncWebClient(
                token=token,
                user_agent_prefix=f"Bolt-Async/{bolt_version} SlackDoor/{slackdoor_version}",
                proxy=self._proxy_url,
                # can override the default logging framework:
                # logger=logging.getLogger("WebClient")
            )

            self._app = AsyncApp(
                client=self._client,
                ignoring_self_events_enabled=False,
                # can override the default logging framework:
                # logger=logging.getLogger("App")
            )
        else:
            logger.warning("Skipping Slack initialization!")
            # FIXME: Come up with a way to mock these for local testing of plugins?
            self._client = None  # type: ignore
            self._app = None  # type: ignore

        self._handler = None

        self._bot_info = {}
        self._users = {}
        self._channels = {}

    async def init_async_handler(self, settings: CaseInsensitiveDict) -> None:
        # NOTE: The app-level token ("xapp-...") is used for establishing a connection
        self._handler = AsyncSocketModeHandler(
            app=self._app,
            app_token=settings["SLACK_APP_TOKEN"],
            proxy=self._proxy_url,
            # can override the default logging framework here with:
            # logger=logging.getLogger("SocketHandler")
        )

        # manually tap in to the message listeners to catch "hello" from the Events API
        # so we know we're connected and can start grabbing info about ourself/workspace
        self._handler.client.message_listeners.append(self._hello_handler)

    async def _hello_handler(self, client: AsyncBaseSocketModeClient, message: dict[str, Any], raw_message: str | None) -> None:
        if message.get("type") == "hello":
            if self.bot_user_id:
                # if we've already got our user ID, that means we already have the data we need
                # (our channel and user info caches are already populated), so just log a message
                # that our connection with Slack has been re-established
                self.logger.info("Connection established with Slack")
            else:
                with start_transaction(op="http.client", name="hello") as txn:
                    try:
                        api_response = await client.web_client.auth_test()
                        self._logger.debug("auth.test: %s", api_response)
                    except SlackApiError as err:
                        raise RuntimeError(f"auth.test: {err.response}") from err

                    if not (bot_id := api_response.get("bot_id")):
                        raise RuntimeError("'bot_id' not found in 'auth.test' API response")

                    with start_span(op="http.client", description="bots.info") as span:
                        try:
                            api_response = await client.web_client.bots_info(bot=bot_id)
                        except SlackApiError as err:
                            span.set_status("internal_error")
                            raise RuntimeError(f"bots.info: {err.response}") from err
                        else:
                            self._logger.info("bots.info: %s", api_response)
                            span.set_status("ok")

                    if bot_info := api_response.get("bot"):
                        self._bot_info = {
                            "id": bot_id,  # starts with "B"
                            "name": bot_info["name"],
                            "user_id": bot_info["user_id"],  # starts with "U"
                        }
                    else:
                        raise RuntimeError("'bot' object not found in 'bots.info' API response")

                    self.logger.info("Getting users...")
                    with start_span(op="http.client", description="users.list") as span:
                        try:
                            # this API call generates way too much output in debug mode, so temporarily bump the level
                            with LoggingContext(client.web_client._logger, level=logging.WARNING):
                                async for page in await client.web_client.users_list(limit=500):
                                    if members := page.get("members"):
                                        for user in members:
                                            self._parse_user_object(user)
                                    else:
                                        span.set_status("internal_error")
                                        self._logger.error("users.list: API response did not include 'members' object")
                                        break
                                else:
                                    span.set_status("ok")
                        except SlackApiError as err:
                            span.set_status("internal_error")
                            raise RuntimeError(f"users.list: {err.response}") from err

                    self.logger.info("Getting channels...")
                    with start_span(op="http.client", description="conversations.list") as span:
                        try:
                            # this API call generates way too much output in debug mode, so temporarily bump the level
                            with LoggingContext(client.web_client._logger, level=logging.WARNING):
                                # the docs say "Returns a list of limited channel-like conversation objects" it includes
                                # 'num_members' (but unfortunately bots are included in the count; plus the field doesn't
                                # get populated for old-school "G"roup channels created before March 2021)
                                # see https://api.slack.com/methods/conversations.list
                                async for page in await client.web_client.conversations_list(
                                    limit=500, types="public_channel,private_channel,im,mpim"
                                ):
                                    if channels := page.get("channels"):
                                        for channel in channels:
                                            self._parse_channel_object(channel)
                                    else:
                                        span.set_status("internal_error")
                                        self._logger.error("conversations.list: API response did not include 'channels' object")
                                        break
                                else:
                                    span.set_status("ok")
                        except SlackApiError as err:
                            span.set_status("internal_error")
                            raise RuntimeError(f"users.list: {err.response}") from err

                    txn.set_status("ok")

            member_channels = len([chan.id for chan in self._channels.values() if chan.is_member])
            self._logger.info(
                f"{Plural(len(self._users)):N user/s}; bot is in {member_channels} of {Plural(len(self._channels)):N channel/s}"
            )

    @property
    def settings(self) -> CaseInsensitiveDict:
        return self._settings

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def app(self) -> AsyncApp:
        return self._app

    @property
    def handler(self) -> AsyncSocketModeHandler:
        return cast(AsyncSocketModeHandler, self._handler)

    @property
    def client(self) -> AsyncWebClient:
        return self._client

    @property
    def bot_info(self) -> dict:
        return self._bot_info or {}

    @property
    def bot_user_id(self) -> str:
        return self.bot_info.get("user_id", "")

    @property
    def bot_name(self) -> str:
        return self.bot_info.get("name", "")

    @property
    def users(self) -> dict[str, User]:
        return self._users

    @property
    def channels(self) -> dict[str, Channel]:
        return self._channels

    @property
    def proxy_url(self) -> str | None:
        return self._proxy_url

    @staticmethod
    def get_instance() -> Slack:
        return Slack()

    # Helper functions to get User and Channel data from the cache (and fill them if they are missing)

    async def get_user_info(self, user_id: str | None) -> User:
        if not user_id:
            return User()

        # strip off leading non-alphanumeric character
        user_id = re.sub(r"^[^A-Z0-9]", "", user_id)

        if (user := self._users.get(user_id)) and user.ok:
            # found valid user in our cache
            return user

        self.logger.warning("User not found in user cache")
        with start_span(op="http.client", description="users.info") as span:
            try:
                api_response = await self.client.users_info(user=user_id)
            except SlackApiError as err:
                span.set_status("internal_error")
                span.set_data("user_id", user_id)
                self.logger.error(f"users.info: {err.response}", exc_info=True)
                return User()

            if not (user_obj := api_response.get("user")):
                span.set_data("api_response", api_response)
                span.set_status("not_found")
                return User()

            span.set_status("ok")
            return self._parse_user_object(user_obj)

    async def get_channel_info(self, channel_id: str | None, *, with_members: bool = False) -> Channel:
        if not channel_id:
            return Channel()

        # strip off leading non-alphanumeric character
        channel_id = re.sub(r"^[^A-Z0-9]", "", channel_id)

        if (channel := self._channels.get(channel_id)) and channel.ok:
            # a valid channel is present in the channel cache
            if not with_members or channel.members is not None:
                # if caller doesn't need member count, OR the member list is populated, use cache
                return channel

        # channel is not in the cache, or the member list needs updating
        return await self._update_channel(channel_id, get_members=with_members)

    def _parse_user_object(self, user_object: dict[str, Any] | None) -> User:
        """Parse "User" object from Slack API responses and update our user cache"""
        if user_object:
            user = User.parse_api_user_key(user_object)
            self._users[user.id] = user
            return user
        else:
            return User()

    def _parse_channel_object(self, channel_object: dict[str, Any] | None) -> Channel:
        """Parse "Channel" object from Slack API responses and update our channel cache"""
        if channel_object:
            channel = Channel.parse_api_channel_key(channel_object)
            self._channels[channel.id] = channel
            return channel
        else:
            return Channel()

    async def _get_channel_members(self, channel_id: str) -> list[str] | None:
        """
        Get a list of non-bot User IDs in the channel (requires self._users to
        already be populated to do that!)
        """
        self._logger.debug("_get_channel_members: %r", channel_id)

        with start_span(op="http.client", description="conversations.members") as span:
            members = []

            try:
                # this API call can generate a lot of output in debug mode, so temporarily bump the level
                with LoggingContext(self.client._logger, level=logging.WARNING):
                    async for page in await self.client.conversations_members(channel=channel_id, limit=500):
                        if members_obj := page.get("members"):
                            # go through each member in the channel and skip any that are bots
                            members.extend([u for u in members_obj if not self._users.get(u, User()).is_bot])
                        else:
                            span.set_status("internal_error")
                            span.set_data("data", {"channel_id": channel_id, "members_obj": members_obj})
                            self._logger.error("conversations.members: API response did not include 'members' object")
                            break
                    else:
                        span.set_status("ok")
            except SlackApiError as err:
                span.set_status("internal_error")
                span.set_data("channel_id", channel_id)
                self.logger.error(f"conversations.members: {err.response}", exc_info=True)
                return None

        return members

    async def _update_channel(
        self, channel_id: str, *, get_members: bool = False, clear_members: bool = False, force_update: bool = False
    ) -> Channel:
        self._logger.debug("_update_channel: %r (get=%r clear=%r force=%r)", channel_id, get_members, clear_members, force_update)

        if not force_update and (channel := self._channels.get(channel_id)) and channel.ok:
            # we already have valid information about the channel, but possibly NOT the members
            if not clear_members and not get_members:
                # don't need to clear or get members... nothing to update, return the data we already have
                self.logger.debug("_update_channel: no update, using channel cache for %r", channel_id)
                return channel

            # since our Channel dataclass is frozen, convert it to a dict so we can add (or clear) members list
            channel_obj = asdict(channel)
        else:
            channel_obj = None

        if not channel_obj:
            # channel is missing from cache (or there's a forced update), so request information about the channel
            self.logger.debug("_update_channel: calling conversations.info for %r", channel_id)
            with start_span(op="http.client", description="conversations.info") as span:
                try:
                    # we don't ask for the number of members because we may ask for the actual member list
                    api_response = await self.client.conversations_info(channel=channel_id, include_num_members=False)
                except SlackApiError as err:
                    span.set_data("channel_id", channel_id)
                    if err.response.get("error", "") == "channel_not_found":
                        # trying to call conversations.info on something like a "direct message"
                        # results in "channel_not_found", so not really an error?
                        span.set_status("not_found")
                    else:
                        span.set_status("internal_error")
                        self.logger.error(f"conversations.info: {err.response}", exc_info=True)
                    return Channel()

                if not (channel_obj := api_response.get("channel")):
                    span.set_data("api_response", api_response)
                    span.set_status("not_found")
                    return Channel()

                span.set_status("ok")

        if get_members and (members := await self._get_channel_members(channel_id)):
            self.logger.debug("_update_channel: got members for %r (len=%d)", channel_id, len(members))
            channel_obj["members"] = members
        else:
            self.logger.debug("_update_channel: clearing members for %r", channel_id)
            channel_obj["members"] = None

        return self._parse_channel_object(channel_obj)

    # Event processors to keep the User and Channel caches up-to-date

    async def _process_user_change(self, event: dict[str, Any], ack: AsyncAck) -> None:
        with start_transaction(op="event", name=event["type"]) as txn:
            with start_span(op="http.client", description="ack") as span:
                await ack()
                span.set_status("ok")
            self._logger.debug("user_change: %s", event)
            user = self._parse_user_object(event["user"])
            self._logger.debug("User changed: %s", user)
            txn.set_status("ok")

    async def _process_team_join(self, event: dict[str, Any], ack: AsyncAck) -> None:
        with start_transaction(op="event", name=event["type"]) as txn:
            with start_span(op="http.client", description="ack") as span:
                await ack()
                span.set_status("ok")
            self._logger.debug("team_join: %s", event)
            user = self._parse_user_object(event["user"])
            self._logger.debug("User joined team: %s", user)
            txn.set_status("ok")

    async def _process_channel_created(self, event: dict[str, Any], ack: AsyncAck) -> None:
        with start_transaction(op="event", name=event["type"]) as txn:
            with start_span(op="http.client", description="ack") as span:
                await ack()
                span.set_status("ok")
            self._logger.debug("channel_created: %s", event)
            channel = await self._update_channel(channel_id=event["channel"]["id"], force_update=True)
            self._logger.debug("Channel created: %s", channel)
            txn.set_status("ok")

    async def _process_channel_changed(self, event: dict[str, Any], ack: AsyncAck) -> None:
        with start_transaction(op="event", name=event["type"]) as txn:
            with start_span(op="http.client", description="ack") as span:
                await ack()
                span.set_status("ok")
            self._logger.debug('channel "changed": %s', event)
            channel_id = event["channel"]["id"] if isinstance(event["channel"], dict) else event["channel"]
            # note: once a channel is archived, 'conversations.members' won't include a "members" object
            channel = await self._update_channel(channel_id=channel_id, force_update=True)
            self._logger.debug("Channel changed: %s", channel)
            txn.set_status("ok")

    async def _process_channel_deleted(self, event: dict[str, Any], ack: AsyncAck) -> None:
        with start_transaction(op="event", name=event["type"]) as txn:
            with start_span(op="http.client", description="ack") as span:
                await ack()
                span.set_status("ok")
            self._logger.debug("channel_deleted: %s", event)
            channel_id = event["channel"]
            if channel_id in self._channels:
                self._logger.debug("Deleting channel: %s", self._channels[channel_id])
                del self._channels[channel_id]
            else:
                self._logger.error("Channel was deleted, but not in channel list")
            txn.set_status("ok")

    async def _process_member_left_channel(self, event: dict[str, Any], ack: AsyncAck) -> None:
        with start_transaction(op="event", name=event["type"]) as txn:
            with start_span(op="http.client", description="ack") as span:
                await ack()
                span.set_status("ok")
            self._logger.debug("member_left_channel: %s", event)
            channel = await self._update_channel(channel_id=event["channel"], clear_members=True)
            self._logger.debug("Left channel: %s", channel)
            txn.set_status("ok")

    # this is called from _dispatch_member_joined_channel (along with any other plugin-registered handlers)
    # which is why it DOESN'T have an await ack()
    async def _process_member_joined_channel(self, event: dict[str, Any]) -> None:
        with start_span(op="_process_member_joined_channel", description="internal") as span:
            self._logger.debug("member_joined_channel: %s", event)

            channel = await self._update_channel(channel_id=event["channel"], clear_members=True)
            self._logger.debug("Joined channel: %s", channel)
            span.set_status("ok")

    async def _process_channel_id_changed(self, event: dict[str, Any], ack: AsyncAck) -> None:
        with start_transaction(op="event", name=event["type"]) as txn:
            with start_span(op="http.client", description="ack") as span:
                await ack()
                span.set_status("ok")
            self._logger.debug("channel_id_changed: %s", event)
            old_channel = self._channels[event["old_channel_id"]]
            self._channels[event["new_channel_id"]] = old_channel
            del self._channels[event["old_channel_id"]]
            txn.set_status("ok")
