import logging
import signal

logger = logging.getLogger(__name__)


class Signal:
    """
    Signal with handler and count.
    """

    # -----------------------------------------------------------------
    def __init__(self, signum):
        """
        Create an signal.  Remember which accumulation it belongs to.
        If syncable_signal is given, then use it for the signal's values.
        """

        self._signum = signum
        self._auto_deactivate_count = None
        self._original = None
        self._count = 0

    # ---------------------------------------------------------------------------------
    def _signal_handler(self, sig, frame):
        self._count += 1
        logger.debug(
            "signum %d happened, count is now %d" % (self._signum, self._count)
        )
        if (
            self._auto_deactivate_count is not None
            and self._count >= self._auto_deactivate_count
        ):
            logger.debug(
                "signum %d auto deactivate count %d reached"
                % (self._signum, self._auto_deactivate_count)
            )
            self.deactivate()

    # -----------------------------------------------------------------
    def activate(self, auto_deactivate_count=None):
        self._auto_deactivate_count = auto_deactivate_count
        self._original = signal.signal(self._signum, self._signal_handler)
        # logger.debug("signum %d original handler %s replaced by %s" % (self._signum, id(self._original), id(self._signal_handler)))
        if self._auto_deactivate_count is None:
            logger.debug("signum %d activated" % (self._signum))
        else:
            logger.debug(
                "signum %d activated to auto deactivate at count %s"
                % (self._signum, self._auto_deactivate_count)
            )

    # -----------------------------------------------------------------
    def deactivate(self):
        if self._original is not None:
            # original_id = id(self._original)
            signal.signal(self._signum, self._original)
            self._original = None
            # logger.debug("signum %d deactivated, restoring original handler %s" % (self._signum, original_id))

    # -----------------------------------------------------------------
    def is_active(self):
        return self._original is not None

    # -----------------------------------------------------------------
    def __del__(self):
        self.deactivate()

    # -----------------------------------------------------------------
    def count(self, count=None):
        """
        Get/clear the count.
        """
        if count is not None:
            self._count = count

        return self._count
