class SetCompare:
    def __init__(self, idx_a: dict[str, set], idx_b: dict[str:set]):
        self.idx_a = idx_a
        self.idx_b = idx_b

    @staticmethod
    def overlaps_helper(idx_a, idx_b):
        overlaps = {}
        for id_a, fp_a in idx_a.items():
            overlaps[id_a] = set()
            for id_b, fp_b in idx_b.items():
                if fp_a.intersection(fp_b):
                    overlaps[id_a].add(id_b)
        return overlaps

    @property
    def overlaps(self):
        return SetCompare.overlaps_helper(
            self.idx_a, self.idx_b
        ) | SetCompare.overlaps_helper(self.idx_b, self.idx_a)

    def is_proper_superset(self, id_a):
        overlaps = self.overlaps
        return all([overlaps[id_b] == {id_a} for id_b in overlaps[id_a]])

    @property
    def equal_11_and_1n(self):
        overlaps = self.overlaps
        equal = []
        for id_a in self.idx_a:
            if self.is_proper_superset(id_a):
                equal.append(({id_a}, overlaps[id_a]))
        return equal

    @property
    def equal_n1(self):
        overlaps = self.overlaps
        equal = []
        for id_b in self.idx_b:
            if len(overlaps[id_b]) != 1:
                if self.is_proper_superset(id_b):
                    equal.append((overlaps[id_b], {id_b}))
        return equal

    @property
    def equal(self):
        return self.equal_11_and_1n + self.equal_n1

    @property
    def equal_ids(self):
        equal_ids = set()
        for ids1, ids2 in self.equal:
            equal_ids.update(ids1)
            equal_ids.update(ids2)
        return equal_ids

    @property
    def other(self):
        overlaps = self.overlaps
        equal_ids = self.equal_ids
        other = []
        for id_a in sorted(set(self.idx_a.keys()).difference(equal_ids)):
            for id_b in sorted(set(self.idx_b.keys()).difference(equal_ids)):
                if id_a in overlaps[id_b]:
                    other.append((id_a, id_b))
        return other

    def do(self):
        return dict(equal=self.equal, other=self.other)
