import protos_pb2
from tickstore import db
import queue


class NoTickObjectError(Exception):
    pass


class TickWriter:
    def __init__(self, measurement, tags, ack):
        self.measurement = measurement
        self.tags = tags

        self._ack = ack
        self._tick_object = None
        self._batch = protos_pb2.TickEventBatch()
        _, self._delta_type = db.get_object(measurement)
        self._last_tick = 0
        self._q = queue.Queue(1)
        self._err = None
        #TODO mutex ?

    def __iter__(self):
        return

    def __next__(self):
        obj = self._q.get()
        if obj is None:
            raise StopIteration

        return obj

    # Write a tick object in the database
    def write_object(self, tick, tick_object):
        if self._err is not None:
            raise self._err

        if self._tick_object is None:
            self._tick_object = tick_object
            snapshot = tick_object.to_snapshot()
            event = protos_pb2.TickEvent(
                tick=tick,
                snapshot=protos_pb2.TickSnapshot(
                    measurement=self.measurement,
                    tags=self.tags,
                    snapshot=snapshot
                )
            )

            self._batch.events.append(event)

        else:
            deltas = self._tick_object.deltas_to(tick_object)
            if deltas is None:
                return

            buffer = db.DeltaBuffer(self._delta_type, None)
            try:
                for delta in deltas:
                    buffer.append(delta)
            except Exception as e:
                self._err = e
                raise e

            event = protos_pb2.TickEvent(
                tick=tick,
                deltas=buffer.bytes())

            try:
                self._tick_object.process_deltas(deltas)
            except Exception as e:
                self._err = e
                raise e

            self._batch.events.append(event)

    # write a tick delta in the database
    def write_deltas(self, tick, deltas):
        if self._err is not None:
            raise self._err

        if self._tick_object is None:
            raise NoTickObjectError

        buffer = db.DeltaBuffer(self._delta_type, None)
        for delta in deltas:
            buffer.append(delta)

        event = protos_pb2.TickEvent(
                tick=tick,
                event=protos_pb2.TickEvent_Deltas(deltas=buffer.bytes()))

        self._batch.events.append(event)
        self._tick_object.process_deltas(deltas)

    # flush the current batch
    def flush(self):
        if self._err is not None:
            raise self._err

        self._flush()

    def _flush(self):
        if len(self._batch.events) == 0:
            return
        self._q.put(self._batch)
        ack = self._ack._next()
        self._batch = protos_pb2.TickEventBatch()
        self._last_tick = ack.tick

    def close(self):
        self._flush()
        # put None to the queue to signal end of iteration
        self._q.put(None)
        self._ack.cancel()
