import re

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class User:
    """
    Representation of a user based on parts of the Slack API user type
    https://api.slack.com/types/user
    """

    id: str = ""  # noqa: A003
    # NOTE: shouldn't use 'name'; see https://api.slack.com/changelog/2017-09-the-one-about-usernames
    name: str = ""
    sanitized_name: str = ""
    real_name: str = ""
    display_name: str = ""
    first_name: str = ""
    is_deleted: bool = False
    is_bot: bool = False
    is_stranger: bool = False
    ok: bool = False  # default to false so 'User()' can be returned in error situations

    @staticmethod
    def parse_api_user_key(user: dict[str, Any]) -> "User":
        """Parse the "user" section of the Slack API 'user' type"""
        if user and (user_id := user.get("id")):
            unknown_default = f"@{user_id}"
            profile = user.get("profile", {})
            real_name = profile.get("real_name_normalized") or user.get("real_name", unknown_default)
            first_name = profile.get("first_name") or real_name.split()[0]
            name = user.get("name", unknown_default)
            sanitized_name = re.sub(r"__+", "_", re.sub(r"[^\w.]", "_", name)).strip("_.")
            display_name = profile.get("display_name_normalized", unknown_default)
            deleted = user.get("deleted", False)
            is_bot = user.get("is_bot", False) or user_id == "USLACKBOT"  # Slackbot doesn't set is_bot!
            # is_stranger is false (or field is not present) when user is from the same workspace as our
            # app's token OR from a different workspace but in a shared channel our app has access to
            is_stranger = user.get("is_stranger", False)

            return User(
                id=user_id,
                name=name,
                sanitized_name=sanitized_name,
                real_name=real_name,
                display_name=display_name,
                first_name=first_name,
                is_deleted=deleted,
                is_bot=is_bot,
                is_stranger=is_stranger,
                ok=True,
            )
        else:
            return User()


@dataclass(frozen=True, slots=True)
class Channel:
    """
    Representation of a channel based on parts of the Slack API for "channel like" types
    https://api.slack.com/types/channel
    https://api.slack.com/types/group
    https://api.slack.com/types/mpim
    https://api.slack.com/types/im
    """

    id: str = ""  # noqa: A003
    name: str = ""
    is_channel: bool = False
    is_member: bool = False
    is_private: bool = False
    is_im: bool = False
    is_mpim: bool = False
    is_group: bool = False
    _member_count: int = 0
    members: list[str] | None = None
    ok: bool = False  # default to false so 'Channel()' can be returned in error situations

    @property
    def member_count(self) -> int:
        return len(self.members) if self.members else self._member_count

    @staticmethod
    def parse_api_channel_key(channel: dict[str, Any]) -> "Channel":
        """Parse the "channel" section of the Slack API 'user' type"""
        if channel and (channel_id := channel.get("id")):
            is_member = channel.get("is_member", False)
            members = channel.get("members")
            member_count = (0 if members is None else len(members)) or channel.get("num_members") or 0

            if channel.get("is_im"):
                # is_im means the conversation is a direct message between two individuals
                # or a user and a bot
                name = channel_id
                member_count = 2 if member_count == 0 else member_count
                is_im = is_private = True
                is_channel = is_mpim = is_group = False
            elif channel.get("is_channel") or channel.get("is_group"):
                # NOTE: for our purposes, this does NOT indicate it's a _public_ channel
                # (we also consider old-school groups [aka private channels with a "G"] to be a "channel")
                # For reference, from the docs at https://api.slack.com/types/conversation:
                # is_channel indicates whether a conversation is a channel. Private channels created
                # before March 2021 (with IDs that begin with G) will return false, instead is_group
                # will be true (along with is_private). Use is_private to determine whether a channel
                # is private or public.
                name = channel.get("name_normalized") or channel.get("name") or "?????"
                is_channel = True  # for our purposes
                is_group = channel.get("is_group", False)
                is_private = channel.get("is_private", False)
                is_im = is_mpim = False
            elif channel.get("is_mpim"):
                # is_mpim represents an _unnamed_ private conversation between multiple users
                name = channel_id
                is_mpim = is_private = True
                is_channel = is_im = is_group = False
            else:
                # not sure what kind of channel this is...
                return Channel()

            return Channel(
                id=channel_id,
                name=name,
                is_channel=is_channel,
                is_member=is_member,
                is_private=is_private,
                is_im=is_im,
                is_mpim=is_mpim,
                is_group=is_group,
                members=members,
                _member_count=member_count,
                ok=True,
            )
        else:
            return Channel()
