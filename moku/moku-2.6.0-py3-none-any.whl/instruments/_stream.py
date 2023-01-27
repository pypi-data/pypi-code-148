import threading
from moku.helpers.converter import StreamConverter


class StreamInstrument(object):
    def __init__(self):
        self._thread = None
        self._converter = None
        self.stream_id = None
        self._stream_error = None

    def get_chunk(self):
        raise NotImplementedError()

    def _write_data(self):
        while True:
            try:
                data = self.get_chunk()
                if data:
                    self._converter.put_data(data)
            except:
                self._stream_error = "Unknown error occurred."
                # closes the stdin of the subprocess,
                # ... indicating end of stream
                self._converter.put_data(b'')
                break

    def process_streaming_interface(self):
        if self._stream_error:
            raise Exception(self._stream_error)
        if self._thread is None:
            if self._converter:
                self._converter.close()
            self._converter = StreamConverter()
            self._thread = threading.Thread(
                target=self._write_data, daemon=True)
            self._thread.start()
        return self._converter
