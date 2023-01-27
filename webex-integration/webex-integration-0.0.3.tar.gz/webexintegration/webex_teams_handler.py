from logging import Handler, LogRecord

from webexintegration.webex_teams import WebexTeams
from webexintegration.webex_formatter import WebexFormatter


class WebexHandler(Handler):
    """WebexHandler is a logging handler which consumes log records and sends
    them to a specified webex chat room

    :param webex_teams: A requests session which handle webex messages
    :type webex_teams: WebexTeams
    """
    
    def __init__(self, webex_teams: WebexTeams, **kwargs) -> None:
        super().__init__(**kwargs)
        self.webex_teams = webex_teams
        self.formatter = WebexFormatter()

    def emit(self, record: LogRecord) -> None:
        try:
            response = self.webex_teams.send_message(self.format(record))
            response.raise_for_status()
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)
        
