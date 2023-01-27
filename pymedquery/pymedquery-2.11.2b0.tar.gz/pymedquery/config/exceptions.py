from pymedquery.config.logger_object import Logger

log = Logger(__name__)

class NoRecordsFound(Exception):
    log.error('No records were found')


class CommitBouncedError(Exception):
    log.error('Your commit did not go through')
