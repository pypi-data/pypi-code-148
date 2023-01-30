import logging
import threading

logger = logging.getLogger(__name__)


class Hazzathread:
    """
    Base class which has a thread.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, thread_name):
        self._thread_name = thread_name
        self._thread = None
        self._ready_event = threading.Event()
        self._stop_event = threading.Event()
        logger.debug(
            "%s thread: instantiated but not started yet" % (self._thread_name)
        )

    # ----------------------------------------------------------------------------------------
    def start(self):
        """
        Start the thread.
        """

        if self.is_running():
            raise RuntimeError(
                "%s thread: cannot start a second thread while first is running"
                % (self._thread_name)
            )

        self._ready_event.clear()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run)
        self._thread.name = self._thread_name

        # Terminate thread abruptly when process dies.
        self._thread.daemon = True

        logger.debug("%s thread: starting" % (self._thread_name))

        # Start the thread running.
        self._thread.start()

    # ----------------------------------------------------------------------------------------
    def wait_ready(self):
        """
        Waits for the thread to be set it's state to ready
        If the thread runs some kind of service this flag is expected to signal
        that the service is now ready to accept requests.
        """

        logger.debug("%s thread: waiting for started event" % (self._thread_name))
        self._ready_event.wait()

    # ----------------------------------------------------------------------------------------
    def stop(self):
        """
        Ask the runner to stop
        """

        if self.is_running():
            logger.debug("%s thread: setting stop_event" % (self._thread_name))
            self._stop_event.set()

    # ----------------------------------------------------------------------------------------
    def wait_stopped(self, timeout=None):
        """
        Joins the thread
        """

        if self._thread is None:
            return

        if timeout is None:
            logger.debug("%s thread: waiting for join (forever)" % (self._thread_name))
        else:
            logger.debug(
                "%s thread: waiting for join, timeout in %s seconds"
                % (self._thread_name, timeout)
            )

        self._thread.join(timeout)

        if not self.is_running():
            self._thread = None
            logger.debug("%s thread: thread joined" % (self._thread_name))

    # ----------------------------------------------------------------------------------------
    def wait_joined(self, timeout=None):
        """
        An alias for wait_stopped
        """

        return self.wait_stopped(timeout=timeout)

    # ----------------------------------------------------------------------------------------
    def is_running(self):
        """
        Returns True if the thread is up and running
        """

        if self._thread is None:
            return False

        return self._thread.is_alive()

    # ----------------------------------------------------------------------------------------
    def _set_ready(self):
        """
        Indicate thread is ready.
        """

        logger.debug("%s thread: started" % (self._thread_name))
        self._ready_event.set()

    # ----------------------------------------------------------------------------------------
    def _run(self):
        """
        Thread run method.
        """

        raise RuntimeError("%s thread: must override run method" % (self._thread_name))

    # ----------------------------------------------------------------------------------------
    def _should_stop(self):
        """
        Return true if this thread should stop what it is doing and return from the thread method.
        """

        return self._stop_event.is_set()
