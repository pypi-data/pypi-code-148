"""
Shared utility functions
"""

# pylint: disable=consider-using-with,global-statement,too-many-arguments,too-many-locals,fixme,too-many-statements,chained-comparison

import subprocess
import sys
from threading import Thread, Event
from tempfile import TemporaryFile
from colorama import just_fix_windows_console  # type: ignore

just_fix_windows_console()  # Fixes color breakages in win32


SKIP_CONFIRMATION = False


def set_global_skip_confirmation(val: bool) -> None:
    """Set the global skip confirmation flag"""
    global SKIP_CONFIRMATION
    SKIP_CONFIRMATION = val
    print(f"**** Setting SKIP_CONFIRMATION to {SKIP_CONFIRMATION} ****")


class StreamPumpThread(Thread):
    """Thread to read stdout"""

    def __init__(self, stream):
        super().__init__(daemon=True)
        self.stream = stream
        self.start()

    def run(self):
        def read_one() -> str:
            # Needed for flutter install on MacOS, othrwise it hangs.
            char = self.stream.read(1)  # type: ignore
            return char

        for char in iter(read_one, ""):
            try:
                # print(char, end="")
                sys.stdout.write(char)
                sys.stdout.flush()
            except UnicodeEncodeError as exc:
                print("UnicodeEncodeError:", exc)


def execute(
    command,
    cwd=None,
    send_confirmation=None,
    ignore_errors=False,
    timeout=60 * 10,
    encoding="utf-8",
) -> int:
    """Execute a command"""
    if not SKIP_CONFIRMATION:
        send_confirmation = None
    print("####################################")
    print(f"Executing\n  {command}")
    if send_confirmation is not None:
        conf_str = send_confirmation.replace("\n", "\\n")
        print(f'Sending confirmation: "{conf_str}"')
    print("####################################")
    if cwd:
        print(f"  CWD={cwd}")

    if send_confirmation is None:
        completed_process = subprocess.run(
            command, cwd=cwd, shell=True, check=not ignore_errors
        )
        return completed_process.returncode

    with TemporaryFile(encoding="utf-8", mode="a") as stdin_string_stream:
        if send_confirmation:
            stdin_string_stream.write(send_confirmation)
        # temporary buffer for stderr
        proc = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True,
            stdin=stdin_string_stream,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding=encoding,
            # 5 MB buffer
            bufsize=1024 * 1024 * 5,
            universal_newlines=True,
        )
        stdout_stream = proc.stdout
        stderr_stream = proc.stderr
        assert stdout_stream is not None
        assert stderr_stream is not None
        thread_stdout = StreamPumpThread(stream=stdout_stream)
        thread_stderr = StreamPumpThread(stream=stderr_stream)

        event = Event()

        def watchdog():
            val = event.wait(timeout=timeout)
            if not val:
                sys.stdout.write(
                    f"Command {command} timed out after {timeout} seconds.\n"
                )
                sys.stdout.flush()
                proc.kill()
                sys.exit(1)

        watchdog_thread = Thread(target=watchdog, daemon=True)
        watchdog_thread.start()
        try:
            rtn = proc.wait()
            event.set()
            watchdog_thread.join()
        except subprocess.TimeoutExpired:
            print(f"Command {command} timed out after {timeout} seconds.")
        thread_stdout.join(timeout=10.0)
        if thread_stdout.is_alive():
            print("Thread is still alive, killing it.")
            stdout_stream.close()
            thread_stdout.join(timeout=10.0)
        thread_stderr.join(timeout=10.0)
        if thread_stderr.is_alive():
            print("Thread is still alive, killing it.")
            stderr_stream.close()
            thread_stderr.join(timeout=10.0)
        if rtn != 0 and not ignore_errors:
            print(f"Command {command} failed with return code {rtn}")
        return rtn
