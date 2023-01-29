from logging import Logger

from case_insensitive_dict import CaseInsensitiveDict

from slack_bolt.app.async_app import AsyncApp

from door.slack import Slack


class DoorBasePlugin:
    """Base class for all SlackDoor plugins

    Acts as a marker-class so SlackDoor can recognize plugins, and provides
    convenience methods for plugins.

    :var settings: SlackDoor settings object that contains all settings that
        were defined through ``local_settings.py`` Plugin developers can use any
        settings that are defined by the user, and ask users to add new settings
        specifically for their plugin.
    """

    def __init__(self) -> None:
        self._fq_name = f"{self.__module__}.{self.__class__.__name__}"

        slack = Slack.get_instance()
        self.settings: CaseInsensitiveDict = slack.settings
        self.logger: Logger = slack.logger
        self.app: AsyncApp = slack.app
        # NOTE: can't set self.handler here, since it's not known until later

    def init(self, app: AsyncApp) -> None:
        """Initialize plugin

        This method can be implemented by instantianted plugin classes. It is
        called once for each plugin during initialization. You can refer to
        settings via ``self.settings`` and access storage through ``self.storage``.
        The connection to Slack has not been started, so you cannot send or process
        messages!

        This method can be specified as either synchronous or asynchronous,
        depending on the needs of the plugin.

        :return: None
        """
        pass

    @property
    def slack(self) -> Slack:
        return Slack.get_instance()
