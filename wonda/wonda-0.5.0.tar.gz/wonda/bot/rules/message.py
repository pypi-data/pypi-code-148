import re

from difflib import SequenceMatcher
from typing import Any, Callable, Iterable, List, Union, Tuple

import vbml

from wonda.bot.rules.abc import ABCRule
from wonda.bot.updates import MessageUpdate
from wonda.types.enums import ChatType, MessageEntityType


class Command(ABCRule[MessageUpdate]):
    """
    A rule that handles bot commands. It takes in a list of
    valid command texts and checks if the message
    contains one of those commands.
    """

    def __init__(
        self,
        texts: Union[str, List[str]],
        prefixes: Union[str, List[str]] = "/",
        arg_map_func: Callable[[str], Any] = str,
    ) -> None:
        self.texts = texts if isinstance(texts, list) else [texts]
        self.prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
        self.arg_map_func = arg_map_func

    async def check(self, msg: MessageUpdate) -> Union[bool, dict]:
        if text := msg.text or msg.caption:
            prefix, text, tag, args = self._parse(text)

            if msg.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                bot = await msg.ctx_api.get_me()

                if tag and tag.lower() != bot.username.lower():
                    return False

            if prefix not in self.prefixes or text not in self.texts:
                return False

            return {"args": list(map(self.arg_map_func, args))}

    @staticmethod
    def _parse(text: str) -> Tuple[str]:
        head, *tail = text.split()
        pfx, (cmd, _, tag) = head[0], head[1:].partition("@")
        return pfx, cmd, tag, tail


class FromChat(ABCRule[MessageUpdate]):
    """
    Checks if the message was sent from a specified chat.
    If not, the rule return False and the message will be ignored.
    """

    def __init__(self, chats: Union[int, List[int]]) -> None:
        self.chats = chats if isinstance(chats, list) else [chats]

    async def check(self, msg: MessageUpdate) -> bool:
        return msg.chat.id in self.chats


class IsReply(ABCRule[MessageUpdate]):
    """
    Checks if the message is a reply.
    """

    async def check(self, msg: MessageUpdate) -> bool:
        return msg.reply_to_message is not None


class IsForward(ABCRule[MessageUpdate]):
    """
    Checks if the message was forwarded.
    """

    async def check(self, msg: MessageUpdate) -> bool:
        return msg.forward_date is not None


class IsGroup(ABCRule[MessageUpdate]):
    """
    Checks if the message was sent in the chat.
    """

    async def check(self, msg: MessageUpdate) -> bool:
        return msg.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]


class IsPrivate(ABCRule[MessageUpdate]):
    """
    Checks if the message is private.
    """

    async def check(self, msg: MessageUpdate) -> bool:
        return msg.chat.type == ChatType.PRIVATE


class Length(ABCRule[MessageUpdate]):
    """
    Checks if the message is longer than or equal to the given length.
    """

    def __init__(self, min_length: int) -> None:
        self.min_length = min_length

    async def check(self, msg: MessageUpdate) -> bool:
        text = msg.text or msg.caption

        if not text:
            return False

        return len(text) >= self.min_length


class Fuzzy(ABCRule[MessageUpdate]):
    """
    Compares message text with the given text
    and returns the closest match.
    """

    def __init__(self, texts: Union[str, List[str]], min_ratio: int = 1) -> None:
        self.texts = texts if isinstance(texts, list) else [texts]
        self.min_ratio = min_ratio

    async def check(self, msg: MessageUpdate) -> bool:
        text = msg.text or msg.caption

        if not text:
            return False

        closest = max(SequenceMatcher(None, t, text).ratio() for t in self.texts)
        return closest >= self.min_ratio


class Mention(ABCRule[MessageUpdate]):
    """
    Parses message entities and checks if the message contains mention(-s).
    Returns a list of mentioned usernames.
    """

    async def check(self, msg: MessageUpdate) -> Union[bool, dict]:
        if not msg.entities:
            return False

        mentions = [
            msg.text[e.offset : e.offset + e.length].strip("@")
            for e in msg.entities
            if e.type == MessageEntityType.MENTION
        ]

        return {"mentions": mentions} if mentions else False


class Regex(ABCRule[MessageUpdate]):
    """
    Checks if the message text matches the given regex.
    """

    PatternLike = Union[str, re.Pattern]

    def __init__(self, expr: Union[PatternLike, List[PatternLike]]) -> None:
        if isinstance(expr, re.Pattern):
            expr = [expr]
        elif isinstance(expr, str):
            expr = [compile(expr)]
        else:
            expr = [compile(expr) if isinstance(expr, str) else expr for expr in expr]

        self.expr = expr

    async def check(self, msg: MessageUpdate) -> bool:
        text = msg.text or msg.caption

        if not text:
            return False

        for e in self.expr:
            if result := re.match(e, text):
                return {"match": result.groups()}

        return False


class Text(ABCRule[MessageUpdate]):
    """
    Checks if the message text is equal to the given text.
    """

    def __init__(self, texts: Union[str, List[str]], ignore_case: bool = False) -> None:
        if not isinstance(texts, list):
            texts = [texts]

        self.texts = texts
        self.ignore_case = ignore_case

    async def check(self, msg: MessageUpdate) -> bool:
        text = msg.text or msg.caption

        if not text:
            return False

        return (
            text in self.texts
            if not self.ignore_case
            else text.lower() in list(map(str.lower, self.texts))
        )


class VBML(ABCRule[MessageUpdate]):
    """
    Matches message text against a list of markup patterns.
    See more details at https://github.com/tesseradecade/vbml
    """

    PatternLike = Union[str, vbml.Pattern]

    def __init__(
        self,
        patterns: Union[PatternLike, Iterable[PatternLike]],
        patcher: vbml.Patcher = vbml.Patcher(),
        flags: re.RegexFlag = re.RegexFlag(0),
    ) -> None:
        if not isinstance(patterns, list):
            patterns = [patterns]

        self.patterns = [
            vbml.Pattern(pattern, flags=flags) if isinstance(pattern, str) else pattern
            for pattern in patterns
        ]
        self.patcher = patcher

    async def check(self, msg: MessageUpdate) -> Union[bool, dict]:
        text = msg.text or msg.caption

        if not text:
            return False

        for pattern in self.patterns:
            match = self.patcher.check(pattern, text)

            if match not in (None, False):
                return match
