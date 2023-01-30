class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def push_back(self, data):
        node = Node(data)
        self.head = node

    def insert(self, values):
        head = None
        curr = None
        for value in values:
            if isinstance(value, list):
                child = self.insert(value)
                curr.child = child
            else:
                node = Node(value)
                if head is None:
                    head = node
                    curr = node
                else:
                    node.prev = curr
                    curr.next = node
                    curr = node

        return head

    def push_array(self, values):
        head = self.insert(values)
        self.head = head

    def __flatten(self, head):
        curr = head
        prev = curr
        while curr is not None:
            if curr.child is not None:
                first, last = self.__flatten(curr.child)
                first.prev = curr
                nxt = curr.next
                curr.child = None
                curr.next = first
                last.next = nxt
            else:
                prev = curr
                curr = curr.next

        return head, prev

    def flatten(self):
        self.__flatten(self.head)

    def __repr__(self):
        curr = self.head
        nodes = []
        while curr is not None:
            nodes.append(curr.data)
            curr = curr.next

        return "->".join(str(x) for x in nodes)


class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
        self.child = None


if __name__ == '__main__':
    arr = [1, 2, 3, [7, 8, [11, 12], 9, 10], 4, 5, 6]
    llist = DoublyLinkedList()
    llist.push_array(arr)
    llist.flatten()
    print(llist)
