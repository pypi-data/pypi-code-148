from logging import Formatter, LogRecord
from traceback import TracebackException


class WebexFormatter(Formatter):
    """WebexFormatter is the default formatter for web ex notifications feel
    """

    EMOJI_MAPPING = {
         "CRITICAL": "🚨",
         "ERROR": "⛔",
         "WARNING": "⚠️",
         "INFO": "ℹ️",
         "DEBUG": "🐳",
         None: "😽"
      }

    def format(self, record: LogRecord) -> str:
        """format formats the logging LogRecord to a markdown string which
        will be plotted in webex teams. In case that a exception

        :param record: the log entry
        :type record: LogRecord
        :return: returns the formatted string
        :rtype: str
        """
        emoji = self.EMOJI_MAPPING.get(
            record.levelname, self.EMOJI_MAPPING[None])

        stack_trace = (("".join(
            TracebackException.from_exception(record.exc_info[1]).format()))
            if record.exc_info else "")

        return (
            f"{emoji} **Name** {record.name} "
            f"**File** {record.filename} ({record.lineno}) "
            f"**{record.levelname}** {record.msg}"
            + (f"\n```\n{stack_trace}\n```\n" if stack_trace else "")
        )
        