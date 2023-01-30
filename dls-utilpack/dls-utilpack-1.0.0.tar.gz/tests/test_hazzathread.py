import logging
import time

import pytest

# Class under test.
from dls_utilpack.hazzathread import Hazzathread

logger = logging.getLogger(__name__)


class TestHazzathread:

    # ----------------------------------------------------------------------------------------
    def test(
        self,
        logging_setup,
    ):
        """
        Test hazzathread simple use.
        """

        failure_message = None
        try:
            my_thread = MyThread()

            assert not my_thread.is_running(), "not running after constructor"
            assert my_thread.my_state == "constructed"

            my_thread.start()

            # My thread dwells for 0.5 before it indicates ready.
            assert my_thread.my_state == "starting"
            assert my_thread.is_running(), "running after start and before ready"

            # Wait for thread to say it is ready.
            my_thread.wait_ready()

            assert my_thread.my_state == "started"

            # Request thread to stop.
            my_thread.stop()

            # Thread dwells for 0.5 after stop request.
            assert my_thread.my_state == "started"
            assert my_thread.is_running(), "still running after stop request"

            # Wait for thread to be stopped.
            my_thread.wait_stopped()
            assert not my_thread.is_running(), "not running after waited stop"
            assert my_thread.my_state == "stopped"

        except Exception as exception:
            logger.exception("unexpected exception during the test", exc_info=exception)
            failure_message = str(exception)

        finally:
            # Request thread to stop.
            my_thread.stop()

        if failure_message is not None:
            pytest.fail(failure_message)


# ----------------------------------------------------------------------------------------
class MyThread(Hazzathread):
    def __init__(self):
        Hazzathread.__init__(self, "my_thread")

        self.my_state = "constructed"

    def _run(self):
        self.my_state = "starting"

        # Dwell before we signal we are ready.
        time.sleep(0.5)

        self.my_state = "started"
        self._set_ready()

        while not self._should_stop():
            time.sleep(0.010)

        # Dwell after stop request and before we actually exit.
        time.sleep(0.5)
        self.my_state = "stopped"
