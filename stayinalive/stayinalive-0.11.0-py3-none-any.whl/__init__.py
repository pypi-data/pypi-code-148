import argparse
import functools
import signal
import subprocess
import threading
from pathlib import Path
from typing import List, Callable, Optional

from .util import TESTS_DIRECTORY_DEFAULT, MODE_FILE_DEFAULT, STATUS_FILE_DEFAULT, DELAY_DEFAULT, FIXING, OK, KO, TEST, ORDER, FIX, SP_KWARGS, print_output, write, is_ko
from .watch import Watcher


def test_and_fix(tests: List[dict], update_status: Callable, delay: float = DELAY_DEFAULT, top_call: bool = True) -> None:
    f"""
    This function will go through the given tests and run their condition one by one.
    On failure, it will attempt to apply the corresponding fix.

    Since the fix may take a while, after a given delay the function will call itself to keep the tests running.
    Only the previous (i.e. successful) tests will be given as parameter to the recursive call.

    After the fix, the test will be run again and, if successful, the loop will resume.
    Should it fail an exception will be raised, interrupting the loop and any ongoing recursion.

    Along the way, the given update_status() function will be called to inform on the healing status ({FIXING}, {OK} or {KO}).

    :param tests: list of tests to be run
    :param update_status: function that will be called to communicate on the healing status ({FIXING}, {OK} or {KO})
    :param delay: in case of a long fix, time to wait before recursing, defaults to {DELAY_DEFAULT} seconds
    :param top_call: whether it's the top-most call in the recursion, defaults to True
    :raises ChildProcessError: when a fix failed and the system is unstable
    """

    for index, test in enumerate(tests):
        # running the condition
        cp = subprocess.run(["/bin/bash", "-l", "-c", test.get(TEST)], **SP_KWARGS)
        if cp.returncode == 0:
            continue  # test successful, moving on to the next one

        # on failure, first we print the result and output, just in case
        prefix = "[" + str(test.get(ORDER)) + "]"
        print_output(test.get(TEST), "failed", cp.stdout.splitlines(), prefix)

        # then we try to fix the problem
        update_status(FIXING)
        sp = subprocess.Popen(["/bin/bash", "-l", "-c", test.get(FIX)], **SP_KWARGS)
        threading.Thread(target=print_output, args=(test.get(FIX), FIXING, sp.stdout, prefix)).start()  # we print the output in another thread so that it doesn't block
        while True:  # this part is a little weird but allows to keep the checks running if the fix takes too long
            try:
                sp.wait(delay)  # if the subprocess takes more than $delay seconds, this will raise a TimeoutExpired exception
                break
            except subprocess.TimeoutExpired:  # catched here, so that we can recurse
                test_and_fix(tests[:index], update_status, delay, top_call=False)

        # after the fix, we run the condition once again to ensure everything's back to normal
        cp = subprocess.run(["/bin/bash", "-l", "-c", test.get(TEST)], **SP_KWARGS)
        if cp.returncode != 0:  # failing at this point is bad: the system stays broken, the fix is lacking
            print_output(test.get(TEST), "failed again", cp.stdout.splitlines(), prefix)
            update_status(KO)
            raise ChildProcessError()
        print(prefix, "fix successful")

    # if this is the top-most call of the recursion, then at this point the problem is fixed, and we're back to normal
    # if not, then the top-most call is actually still trying to fix the problem
    update_status(OK if top_call else FIXING)


def stayinalive(tests_directory: Path, mode_file: Path, status_file: Path, event: threading.Event, delay: float = DELAY_DEFAULT) -> None:
    f"""
    Starts the tests directory's and mode file's monitoring, then the self-healing loop.

    An Event must be provided to properly interrupt the loop.
    It must be sent (set()) from another thread or by setting up the capture of a system signal such as SIGINT or SIGTERM.

    :param tests_directory: Path to the tests directory
    :param mode_file: Path to the mode file
    :param status_file: Path to the file that will store the healing status ({FIXING}, {OK} or {KO}) and other metadata
    :param event: Event that will interrupt the healing loop
    :param delay: time to wait between two iterations of the healing loop, defaults to {DELAY_DEFAULT} seconds
    """

    if is_ko(status_file):
        print("exiting: ko status found in", status_file)
        return

    if not tests_directory.is_dir():
        print("exiting:", tests_directory, "must exist and be a directory")
        return

    print(f"watching: {tests_directory}, {mode_file}")
    watcher = Watcher(tests_directory, mode_file)

    try:
        while not event.is_set():
            watcher.refresh_active_tests_if_necessary()  # the configuration is now up-to-date
            update_status = functools.partial(write, status_file, watcher.active_mode)  # here we create a partial function to write the metadata to the status file
            test_and_fix(watcher.active_tests, update_status, delay)  # the actual self-healing happens here
            event.wait(delay)  # interruptable pause before the next iteration

        print("exiting: loop-ending signal")
    except ChildProcessError:  # raised by test_and_fix() is a fix failed
        print("exiting: fatal error")


def main(args: Optional[List[str]] = None) -> None:
    argparser = argparse.ArgumentParser(description="Minimalist self-healing.")
    argparser.add_argument("-t", "--tests-directory", type=Path, default=Path(TESTS_DIRECTORY_DEFAULT), help=f"path to the tests directory, defaults to {TESTS_DIRECTORY_DEFAULT}", metavar="<path>")
    argparser.add_argument("-m", "--mode-file", type=Path, default=Path(MODE_FILE_DEFAULT), help=f"path to the mode file, defaults to {MODE_FILE_DEFAULT}", metavar="<path>")
    argparser.add_argument("-s", "--status-file", type=Path, default=Path(STATUS_FILE_DEFAULT), help=f"path to the status file, defaults to {STATUS_FILE_DEFAULT}", metavar="<path>")
    argparser.add_argument("-d", "--delay", type=float, default=DELAY_DEFAULT, help=f"in seconds, time between two rounds of checks, defaults to {DELAY_DEFAULT}", metavar="<duration>")
    args = argparser.parse_args(args)

    # turning SIGINT and SIGTERM into an event
    event = threading.Event()
    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, lambda signum, frame: event.set())

    stayinalive(args.tests_directory, args.mode_file, args.status_file, event, args.delay)
