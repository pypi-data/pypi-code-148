class StacksQueue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x):
        self.in_stack.append(x)

    def pop(self):
        if len(self.out_stack) == 0:
            while len(self.in_stack) > 0:
                val = self.in_stack.pop()
                self.out_stack.append(val)

        v = self.out_stack.pop()
        return v

    def peek(self):
        if len(self.out_stack) == 0:
            while len(self.in_stack) > 0:
                val = self.in_stack.pop()
                self.out_stack.append(val)

        return self.out_stack[len(self.out_stack)-1]

    def empty(self):
        return len(self.out_stack) == 0 and len(self.in_stack) == 0


if __name__ == '__main__':
    queue = StacksQueue()
    queue.push(1)
    queue.push(2)
    queue.push(3)

    first = queue.peek()
    print(first)

    val = queue.pop()
    print(val)

    empty = queue.empty()
    print(empty)
