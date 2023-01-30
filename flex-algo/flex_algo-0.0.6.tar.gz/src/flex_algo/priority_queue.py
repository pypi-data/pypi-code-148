class PriorityQueue:
    def __init__(self, comparator):
        self.queue = []
        self.comparator = comparator

    def push(self, val):
        self.queue.append(val)
        self.__sift_up()

    def size(self):
        return len(self.queue)

    def __compare(self, idx, parent):
        res = self.comparator(self.queue[idx], self.queue[parent])
        return res

    def __parent(self, idx):
        return int((idx - 1) / 2)

    def __swap(self, i, j):
        temp = self.queue[i]
        self.queue[i] = self.queue[j]
        self.queue[j] = temp

    def __sift_up(self):
        idx = self.size() - 1

        while idx > 0 and self.__compare(idx, self.__parent(idx)):
            parent = self.__parent(idx)
            self.__swap(idx, parent)
            idx = parent

    def __left_child(self, idx):
        return 2 * idx + 1

    def __right_child(self, idx):
        return 2 * idx + 2

    def __sift_down(self):
        size = self.size()
        idx = 0
        while (self.__left_child(idx) < size and self.__compare(self.__left_child(idx), idx)) or (self.__right_child(idx) < size and self.__compare(self.__right_child(idx), idx)):
            current = self.__left_child(idx)
            if self.__right_child(idx) and self.__compare(self.__right_child(idx), self.__left_child(idx)):
                current = self.__right_child(idx)

            self.__swap(idx, current)
            idx = current

    def is_empty(self):
        return self.size() == 0

    def pop(self):
        idx = self.size() - 1
        self.__swap(0, idx)
        val = self.queue.pop()

        self.__sift_down()

        return val

    def __repr__(self):
        return "->".join(str(x) for x in self.queue)


if __name__ == '__main__':
    cmp = lambda a, b: a < b

    def compare(a, b) -> bool:
        return a < b

    queue = PriorityQueue(compare)
    queue.push(4)
    queue.push(3)
    queue.push(1)
    queue.push(2)

    print(queue)

    val = queue.pop()
    print(val)
    val2 = queue.pop()
    print(val2)
    val3 = queue.pop()
    print(val3)
    val4 = queue.pop()
    print(val4)

    print(queue)
    print(queue.is_empty())
