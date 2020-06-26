from abc import ABC, abstractmethod

class BaseQueue(ABC):
    ''' Abstract base class for queue implementations. '''
    def __init__(self, max_in_memory: int):
        self._max_in_memory = max_in_memory

    @property
    def max_in_memory(self) -> int:
        '''
            The maximum number of items that can be held in memory at any given time.
            All other items in the queue must be written to disk.
        '''
        return self._max_in_memory

    @property
    @abstractmethod
    def count(self) -> int:
        '''
            The total number of items in the queue.
        '''

    @property
    @abstractmethod
    def in_memory_count(self) -> int:
        '''
            The number of items currently in memory.
        '''

    @property
    @abstractmethod
    def on_disk_count(self) -> int:
        '''
            The number of items currently on disk.
        '''

    @abstractmethod
    def enqueue(self, value):
        '''
            Adds an item to the queue.
        '''

    @abstractmethod
    def dequeue(self) -> object:
        '''
            Removes an item from the queue and returns it.
        '''

    @abstractmethod
    def peek(self) -> object:
        '''
            Returns the first item in the queue.
        '''
