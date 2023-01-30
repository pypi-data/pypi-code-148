
class QueryGroup:
    def __init__(self, queries):
        self._queries = queries

        # Next all queries first
        for i in range(len(queries)):
            queries[i].next()
            queries[i]._id = i

        self._err = None     # query error
        self._tick = 0       # current tick
        self._group_id = 0   # current object's groupID
        self._objects = {}   # dictionary objectID : object
        self._tags = {}      # dictionary objectID : tags
        self._curr = None

    # Prepare the next result row for reading with Scan
    def next(self):
        if self._err is not None:
            return False

        if self._curr is not None:
            q = self._queries[self._curr]
            if not q.next():
                self._queries = self._queries[:self._curr] + self._queries[self._curr+1:]
            self._curr = None

        if len(self._queries) == 0:
            return False

        min_q = 0
        min_tick = self._queries[0]._tick

        for i in range(1, len(self._queries)):
            if self._queries[i]._tick < min_tick:
                min_tick = self._queries[i]._tick
                min_q = i

        self._tick = min_tick
        self._group_id = self._queries[min_q]._id
        self._curr = min_q

        if self._group_id not in self._objects:
            _, obj, oid = self._queries[min_q].read()
            self._objects[self._group_id] = obj
            self._tags[self._group_id] = self._queries[min_q].get_tags(oid)

        return True

    # TODO tags
    def read(self):
        return self._tick, self._objects[self._group_id], self._group_id

    def get_tags(self, group_id):
        return self._tags[group_id]

    def close(self):
        for q in self._queries:
            q.close()
        return self._err

    def err(self):
        return self._err
