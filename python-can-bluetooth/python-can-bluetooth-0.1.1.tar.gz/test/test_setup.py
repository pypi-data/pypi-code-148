"""
configs and helper class for Bluetooth test case
"""

from copy import copy
import platform

# get test configuration
_sys = platform.system().lower()
IS_WINDOWS = "windows" in _sys or ("win" in _sys and "darwin" not in _sys)
IS_LINUX = "linux" in _sys
IS_OSX = "darwin" in _sys
IS_UNIX = IS_LINUX or IS_OSX
del _sys
IS_PYPY = platform.python_implementation() == "PyPy"

# Mentioned in python-can #1010
TIMEOUT = 0.5 if IS_PYPY else 0.1  # 0.1 is the default set in SerialBus


class ComparingMessagesTestCase:
    """
    Must be extended by a class also extending a unittest.TestCase.

    .. note:: This class does not extend unittest.TestCase so it does not get
              run as a test itself.
    """

    def __init__(self, allowed_timestamp_delta=0.0, preserves_channel=True):
        """
        :param float or int or None allowed_timestamp_delta: directly passed to :meth:`can.Message.equals`
        :param bool preserves_channel: if True, checks that the channel attribute is preserved
        """
        self.allowed_timestamp_delta = allowed_timestamp_delta
        self.preserves_channel = preserves_channel

    def assertMessageEqual(self, message_1, message_2):
        """
        Checks that two messages are equal, according to the given rules.
        """

        if message_1.equals(message_2, timestamp_delta=self.allowed_timestamp_delta):
            return
        elif self.preserves_channel:
            print(f"Comparing: message 1: {message_1!r}")
            print(f"           message 2: {message_2!r}")
            self.fail("messages are unequal with allowed timestamp delta {}".format(self.allowed_timestamp_delta))
        else:
            message_2 = copy(message_2)  # make sure this method is pure
            message_2.channel = message_1.channel
            if message_1.equals(message_2, timestamp_delta=self.allowed_timestamp_delta):
                return
            else:
                print(f"Comparing: message 1: {message_1!r}")
                print(f"           message 2: {message_2!r}")
                self.fail(
                    "messages are unequal with allowed timestamp delta {} even when ignoring channels".format(
                        self.allowed_timestamp_delta
                    )
                )

    def assertMessagesEqual(self, messages_1, messages_2):
        """
        Checks the order and content of the individual messages pairwise.
        Raises an error if the lengths of the sequences are not equal.
        """
        self.assertEqual(len(messages_1), len(messages_2), "the number of messages differs")

        for message_1, message_2 in zip(messages_1, messages_2):
            self.assertMessageEqual(message_1, message_2)


class SerialDummy:
    """
    Dummy to mock the serial communication
    """

    msg = None

    def __init__(self):
        self.msg = bytearray()

    def read(self, size=1):
        return_value = bytearray()
        for _ in range(size):
            return_value.append(self.msg.pop(0))
        return bytes(return_value)

    def write(self, msg):
        self.msg = bytearray(msg)

    def reset(self):
        self.msg = None
