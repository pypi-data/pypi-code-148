import logging

from slack_bolt.context.async_context import AsyncBoltContext

logger = logging.getLogger(__name__)


class File:
    def __init__(
        self,
        filename: str,
        title: str,
        file: str | None = None,
        content: str | None = None,
        snippet_type: str = "auto",
        initial_comment: str | None = None,
        channel: str | None = None,
        thread_ts: str | None = None,
        context: AsyncBoltContext | None = None,
    ) -> None:
        """
        Prepare a file for uploading
        """
        if file and content:
            raise ValueError("Specify either a file, or content, but not both")

        if not context:
            context = AsyncBoltContext()
        self.context = context

        self.filename = filename
        self.file = file
        self.content = content
        self.title = title
        self.snippet_type = snippet_type
        self.initial_comment = initial_comment
        # override the values from 'context', if specified
        if channel:
            self.channel = channel
        if thread_ts:
            self.thread_ts = thread_ts

    @property
    def context(self) -> AsyncBoltContext:
        return self._context

    @context.setter
    def context(self, context: AsyncBoltContext) -> None:
        """When updating the 'context' of a File, update thread_ts and channel"""
        self._context = context
        self.thread_ts = context.get("conditional_thread_ts")
        self.channel = context.get("channel_id")

    def __repr__(self) -> str:
        return f"<{__class__.__name__}: {self.filename}>"
