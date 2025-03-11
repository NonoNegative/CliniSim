class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last
        self.display()

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        self.head = new_node

    def delete(self, key):
        temp = self.head
        while temp and temp.data != key:
            temp = temp.next
        if not temp:
            return
        if temp.prev:
            temp.prev.next = temp.next
        if temp.next:
            temp.next.prev = temp.prev
        if temp == self.head:
            self.head = temp.next
        temp = None

    def display(self):
        temp = self.head
        elements = []
        while temp:
            elements.append(str(temp.data))
            temp = temp.next

    def search(self, key):
        temp = self.head
        while temp:
            if temp.data == key:
                return True
            temp = temp.next
        return False

    def reverse(self):
        temp = None
        current = self.head
        while current:
            temp = current.prev
            current.prev = current.next
            current.next = temp
            current = current.prev
        if temp:
            self.head = temp.prev

    def to_list(self):
        result = []
        temp = self.head
        while temp:
            result.append(temp.data)
            temp = temp.next
        return result