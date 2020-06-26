from base.base_queue import BaseQueue
import pickle

class Node():
    def __init__(self, value):
        self.value = value
        self.next = None

class DiskQueue():
    def __init__(self):
        self.head = None
        self.tail = None

class Queue(BaseQueue):
    ''' Abstract base class for queue implementations. '''
    def __init__(self, max_in_memory: int):
        super().__init__(max_in_memory)
        if (type(self.max_in_memory) is not int) or (self.max_in_memory < 0):
            raise ValueError
        self.memory_count = 0
        self.disk_count = 0
        self.head = None
        self.tail = None

    @property
    def count(self) -> int:
        return self.memory_count + self.disk_count

    @property
    def in_memory_count(self) -> int:
        return self.memory_count

    @property
    def on_disk_count(self) -> int:
        return self.disk_count

    @property
    def is_full(self) -> bool:
        return self.memory_count == self.max_in_memory

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    def read_pickle(self) -> object:
        try:
            pickle_reader = open('disk_storage', 'rb')
        except EOFError and FileNotFoundError:
            return None
        disk_queue = pickle.load(pickle_reader)
        pickle_reader.close()
        return disk_queue

    def write_pickle(self, disk_queue):
        pickle_writer = open('disk_storage', 'wb')
        pickle.dump(disk_queue, pickle_writer)
        pickle_writer.close()

    def add_to_disk(self, node):
        disk_queue = self.read_pickle()
        if self.disk_count > 0:
            disk_queue.tail.next = node
        else:
            disk_queue = DiskQueue()
            disk_queue.head = node
        disk_queue.tail = node
        self.write_pickle(disk_queue)

    def remove_from_disk(self) -> object:
        disk_queue = self.read_pickle()
        if disk_queue is None:
            return None
        node = disk_queue.head
        if disk_queue.head is disk_queue.tail:
            disk_queue.tail = None
        disk_queue.head = disk_queue.head.next
        self.write_pickle(disk_queue)
        return node

    def enqueue(self, value):
        node = Node(value)
        if self.is_full:
            self.add_to_disk(node)
            self.disk_count += 1
        else:
            if self.is_empty:
                self.head = node
            else:
                self.tail.next = node
            self.tail = node
            self.memory_count += 1

    def dequeue(self) -> object:
        assert not self.is_empty, "The queue is empty."
        if self.max_in_memory == 0:
            disk_node = self.remove_from_disk()
            self.disk_count -= 1
            return disk_node.value
        node = self.head
        if self.head is self.tail:
            self.tail = None
        self.head = self.head.next
        self.memory_count -= 1
        if self.disk_count > 0:
            disk_node = self.remove_from_disk()
            self.disk_count -= 1
            self.enqueue(disk_node.value)
        return node.value

    def peek(self) -> object:
        assert not self.is_empty, "The queue is empty."
        if self.max_in_memory == 0:
            return self.read_pickle().head.value
        return self.head.value
