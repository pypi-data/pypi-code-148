import logging
import queue
import shutil
import time
from os import environ
from pathlib import Path
from subprocess import PIPE, Popen
from threading import Thread

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

MOKU_CLI_PATH = environ.get('MOKU_CLI_PATH', shutil.which("mokucli"))
if MOKU_CLI_PATH:
    MOKU_CLI_PATH = Path(MOKU_CLI_PATH).expanduser()


class StreamConverter:
    """
    Parses incoming .li stream to CSV
    """

    def __init__(self):
        logging.info("Creating parser...")
        if not MOKU_CLI_PATH:
            raise Exception(
                "Cannot find mokucli utility, try setting "
                "MOKU_CLI_PATH to the absolute path of mokucli or "
                "please download the latest version from here:"
                "https://www.liquidinstruments.com/resources/software")

        self.proc = Popen([MOKU_CLI_PATH, "convert", "-", "-"],
                          stdin=PIPE, stdout=PIPE, stderr=PIPE)

        self._in = self.proc.stdin

        self._in_running = True
        self._out_running = True
        self._record_size = None
        self.schema = None

        self.in_stream = queue.Queue()
        self.error = None

        self._write_stdin()
        self._wait_until_complete()

    def put_data(self, data):
        """
        Write stream bytes to convert
        """
        if self.error:
            raise Exception(self.error)

        if data:
            self.in_stream.put_nowait(data)
        else:
            logging.info("Closed proc.stdin")
            self._in_running = False

    def get_data(self, size=500):
        """
        Read the converted bytes
        """
        if self.error:
            raise Exception(self.error)

        if self._in_running or self._out_running:
            _parsed_data = []

            # First row is always a csv header
            if not self.schema:
                self.schema = self.proc.stdout.readline().decode(
                    "utf8").strip()
                logging.info(self.schema)

            _parsed_data.append(self.schema)

            # Knowing the row size will help us to
            # serve exact number of user requested rows
            if not self._record_size:
                entry_1 = self.proc.stdout.readline()
                self._record_size = len(entry_1)
                _parsed_data.append(entry_1.decode("utf8"))

            data = self.proc.stdout.readlines(
                size * self._record_size)
            _parsed_data.extend([d.decode("utf8") for d in data])
            return self.csv_to_object(_parsed_data)

        raise Exception("End of stream")

    def csv_to_object(self, csv_data):
        result = dict((x.strip(), []) for x in csv_data[0].split(','))
        _key_list = list(result.keys())
        for _e in csv_data[1:]:
            vals = list(map(float, _e.split(',')))
            for i, v in enumerate(vals):
                result[_key_list[i]].append(v)
        return result

    def close(self):
        """
        Cancels the conversion stream
        """
        if self.proc and self.proc.poll() is None:
            logging.info("Closing proc...")
            self.proc.kill()

    def _write_stdin(self):
        def _write():
            while True:
                if self.in_stream.qsize():
                    self._in.write(self.in_stream.get_nowait())
                    self._in.flush()
                elif not self._in_running:
                    break

        _thread = Thread(target=_write, daemon=True)
        _thread.start()

    def _wait_until_complete(self):
        def _wait():
            while self.proc.poll() is None:
                time.sleep(0.1)
                continue

            if self.proc.returncode:
                self.error = self.proc.stderr.read(1024).decode(
                    "utf8")

            self._out_running = False
            self._in_running = False

        _thread = Thread(target=_wait, daemon=True)
        _thread.start()
