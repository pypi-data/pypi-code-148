from .base_parsing_step import BaseParsingStep
from . import mixins


# class ParsingStep(mixins.EventletPerformMixin,
class ParsingStep(mixins.MultiThreadPerformMixin,
                  mixins.RequestsDownloadingMixin,
                  mixins.SafePerformMixin,
                  mixins.RepeatRecursivelyOnExceptionMixin,
                  BaseParsingStep):
    """
    Class for parsing data step by step.
    The class represents one parsing step.

    input_data is required on initializing.
    To start parsing, call the "perform" method.

    This class uses multithreading, "requests" module,
    and tries to execute the code again if an exception occurs
    during the execution of the perform method.
    """

    is_save_data_step = False
    next_step_class = None
    countdown_on_exception = 1
    max_repeats_on_exception = None  # None for no limit
