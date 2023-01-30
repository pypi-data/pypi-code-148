class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        node = self.head
        nodes = []

        while node is not None:
            nodes.append(node.data)
            node = node.next

        return '->'.join(str(n) for n in nodes)

    def push_front(self, data):
        new_node = Node(data)
        new_node.next = self.head

        self.head = new_node

    def push_back(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        node = self.head
        while node.next is not None:
            node = node.next

        node.next = new_node

    def reverse(self):
        curr = self.head
        pre, nxt = None, None

        while curr is not None:
            nxt = curr.next
            curr.next = pre
            pre = curr
            curr = nxt

        self.head = pre

    def reverse_between(self, start, end):
        curr = self.head
        pre_start = curr
        idx = 0

        # find the start node
        while idx < start - 1:
            pre_start = curr
            curr = curr.next
            idx += 1

        start_node = curr

        pre, nxt = None, None
        while idx < end and curr is not None:
            idx += 1
            nxt = curr.next
            curr.next = pre
            pre = curr
            curr = nxt

        pre_start.next = pre
        start_node.next = curr

    def is_cyclic(self):
        tortoise = self.head
        hare = self.head

        while tortoise is not None and hare is not None:
            tortoise = tortoise.next
            hare = hare.next

            if hare is not None:
                hare = hare.next

            if tortoise == hare:
                break

        if tortoise is None or hare is None:
            return None

        p1 = self.head
        # meeting point
        p2 = tortoise

        while p1 != p2:
            p1 = p1.next
            p2 = p2.next

        return p1


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return str(self.data)


def is_cyclic(head):
    tortoise = head
    hare = head

    while tortoise is not None and hare is not None:
        tortoise = tortoise.next
        hare = hare.next

        if hare is not None:
            hare = hare.next

        if tortoise == hare:
            break

    if tortoise is None or hare is None:
        return None

    p1 = head
    # meeting point
    p2 = tortoise

    while p1 != p2:
        p1 = p1.next
        p2 = p2.next

    return p1


if __name__ == '__main__':
    print('=============testing Linked List==========')
    node_a = Node(1)
    print(node_a)
    node_b = Node(2)
    node_a.next = node_b
    node_c = Node(3)
    node_b.next = node_c
    node_d = Node(4)
    node_c.next = node_d
    node_d.next = node_b

    cyclic_node = is_cyclic(node_a)
    print(cyclic_node)

    llist = LinkedList()

    llist.push_back(1)
    llist.push_back(2)
    llist.push_back(3)
    llist.push_back(4)
    llist.push_back(5)
    print(llist)

    cyclic = llist.is_cyclic()
    print(cyclic)

    llist.reverse_between(2, 4)
    print(llist)

    llist2 = LinkedList()
    llist2.push_back(5)
    llist2.reverse_between(1, 1)
    print(llist2)

