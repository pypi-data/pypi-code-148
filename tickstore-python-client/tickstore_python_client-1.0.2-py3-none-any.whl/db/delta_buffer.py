from ctypes import Structure, sizeof, memmove


class DeltaBuffer:
    def __init__(self, data_type, buffer):
        self._data_type = data_type
        if buffer is None:
            self._buf = bytearray()
        else:
            self._buf = buffer
        self._buf_idx = 0

    def __len__(self):
        return int(len(self._buf) / sizeof(self._data_type))

    def __iter__(self):
        self._buf_idx = 0
        return self

    def __next__(self):
        offset = self._buf_idx * sizeof(self._data_type)
        if offset < len(self._buf):
            delta = self._data_type.from_buffer_copy(self._buf, offset)
            self._buf_idx += 1
            return delta
        else:
            raise StopIteration

    def __getitem__(self, item):
        offset = item * sizeof(self._data_type)
        # TODO we want from_buffer not from_buffer_copy, why make a copy ?? but API doesn't allow us to use bytes
        delta = self._data_type.from_buffer_copy(self._buf, offset)
        return delta

    def __setitem__(self, key, value):
        # TODO assert type
        start_offset = key * sizeof(self._data_type)
        end_offset = start_offset + sizeof(self._data_type)
        self._buf[start_offset:end_offset] = bytes(value)

    def append(self, value):
        self._buf.extend(bytes(value))
        self._buf_idx = len(self._buf)

    def bytes(self):
        return bytes(self._buf)