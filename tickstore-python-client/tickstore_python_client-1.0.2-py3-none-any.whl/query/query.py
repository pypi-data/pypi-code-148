from tickstore.db import DeltaBuffer


class QueryFunctor:
    def __init__(self, apply, args):
        self.apply = apply
        self.args = args


class Query:
    def __init__(self, generator, object_constructor, delta_constructor):
        self._generator = generator
        self._object_constructor = object_constructor
        self._delta_constructor = delta_constructor

        self._err = None     # query error
        self._batch = None   # current batch
        self._batch_idx = 0  # current batch's idx
        self._tick = 0       # current tick
        self._group_id = 0   # current object's groupID
        self._objects = {}   # dictionary objectID : object
        self._tags = {}      # dictionary objectID : tags

    # Prepare the next result row for reading with Scan
    def next(self):
        if self._err is not None:
            return False
        # If we have already read all the events, fetch a new batch
        if self._batch is None:
            try:
                msg = self._generator.next()
                self._batch = msg
                self._batch_idx = 0
            except Exception as e:
                self._err = e
                return False

        event = self._batch.ticks[self._batch_idx]

        self._tick = event.tick
        self._group_id = event.group_id

        if self._group_id in self._objects:
            obj = self._objects[self._group_id]
        else:
            obj = self._object_constructor()
            self._objects[self._group_id] = obj

        if event.HasField("deltas"):
            buffer = DeltaBuffer(self._delta_constructor, event.deltas)
            try:
                obj.process_deltas(buffer)
            except Exception as e:
                self._err = e
                return False
        elif event.HasField("snapshot"):
            try:
                obj.from_snapshot(event.snapshot.snapshot)
            except Exception as e:
                self._err = e
                return False
            self._tags[self._group_id] = event.snapshot.tags

        self._batch_idx += 1

        if self._batch_idx == len(self._batch.ticks):
            self._batch = None
            self._batch_idx = -1

        return True

# TODO tags
    def read(self):
        return self._tick, self._objects[self._group_id], self._group_id

    def get_tags(self, group_id):
        return self._tags[group_id]

    def close(self):
        self._generator.cancel()
        return self._err

    def err(self):
        return self._err
