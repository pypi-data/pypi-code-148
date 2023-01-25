"""
    Exceptions used with Quantnet.

    The base exception class is :class:`. QuantnetException`.
    Exceptions which are raised are all subclasses of it.

"""

# from rucio.common.constraints import AUTHORIZED_VALUE_TYPES


class QuantnetException(Exception):
    """
    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """

    def __init__(self, *args, **kwargs):
        super(QuantnetException, self).__init__(*args, **kwargs)
        self._message = "An unknown exception occurred."
        self.args = args
        self.kwargs = kwargs
        self.error_code = 1
        self._error_string = None

    def __str__(self):
        try:
            self._error_string = self._message % self.kwargs
        except Exception:
            # at least get the core message out if something happened
            self._error_string = self._message
        if len(self.args) > 0:
            # If there is a non-kwarg parameter, assume it's the error
            # message or reason description and tack it on to the end
            # of the exception message
            # Convert all arguments into their string representations...
            args = ["%s" % arg for arg in self.args if arg]
            self._error_string = (self._error_string + "\nDetails: %s" % '\n'.join(args))
        return self._error_string.strip()