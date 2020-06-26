import os
import tempfile
import pytest
from implementation.queue import Queue

class HelperClass:
    def __init__(self, value: str):
        self._value = value

    @property
    def value(self):
        return self._value

def none_test_helper(max: int):
    queue = Queue(max)

    with pytest.raises(Exception):
        queue.dequeue()

    queue.enqueue(1)
    queue.enqueue(None)

    assert queue.count == 2
    assert queue.dequeue() == 1
    assert queue.dequeue() is None
    assert queue.count == 0

def test_negative_max():
    with pytest.raises(Exception) as e:
        Queue(-1)

def test_enqueue_object():
    queue = Queue(0)
    queue.enqueue(HelperClass("abc"))
    queue.enqueue(HelperClass("def"))
    assert queue.dequeue().value == "abc"
    assert queue.dequeue().value == "def"

    queue.enqueue(HelperClass("ghi"))
    assert queue.dequeue().value == "ghi"

def test_none_enqueue():
    none_test_helper(10)
    none_test_helper(0)

def test_peek():
    ''' Simple test of the peek method. '''
    queue = Queue(10)
    queue.enqueue(1)
    assert queue.peek() == 1

    queue.dequeue()
    queue.enqueue(4)
    assert queue.peek() == 4

def test_disk_only():
    queue = Queue(0)
    total_count = 100
    halfway = 100 // 2

    queue.enqueue(0)
    assert queue.on_disk_count == 1
    assert queue.on_disk_count == queue.count
    assert queue.in_memory_count == 0

    for i in range(1, total_count):
        queue.enqueue(i)
        assert queue.on_disk_count == i + 1
        assert queue.on_disk_count == queue.count
        assert queue.in_memory_count == 0

    for i in range(0, halfway):
        peek = queue.peek()
        assert i == peek
        assert i == queue.dequeue()
        assert queue.on_disk_count == total_count - (i + 1)
        assert queue.on_disk_count == queue.count
        assert queue.in_memory_count == 0

    queue.enqueue(total_count)
    assert queue.on_disk_count == halfway + 1
    assert queue.on_disk_count == queue.count
    assert queue.in_memory_count == 0

    for i in range(halfway, total_count + 1):
        peek = queue.peek()
        assert i == peek
        assert i == queue.dequeue()
        assert queue.on_disk_count == total_count - i
        assert queue.on_disk_count == queue.count
        assert queue.in_memory_count == 0

    assert queue.count == 0
    assert queue.on_disk_count == 0
    assert queue.in_memory_count == 0

    with pytest.raises(Exception):
        queue.dequeue()

def test_mixed():
    total_count = 100
    halfway = 100 // 2
    queue = Queue(halfway)

    queue.enqueue(0)
    assert queue.in_memory_count == 1
    assert queue.in_memory_count == queue.count
    assert queue.on_disk_count == 0

    for i in range(1, total_count):
        queue.enqueue(i)

        if i < halfway:
            assert queue.in_memory_count == i + 1
            assert queue.in_memory_count == queue.count
            assert queue.on_disk_count == 0
        else:
            assert queue.in_memory_count == halfway
            assert queue.on_disk_count == i - halfway + 1
            assert queue.count == queue.in_memory_count + queue.on_disk_count

    for i in range(0, halfway):
        peek = queue.peek()
        assert i == peek
        assert i == queue.dequeue()
        assert queue.in_memory_count == halfway
        assert queue.on_disk_count == halfway - (i + 1)
        assert queue.count == queue.in_memory_count + queue.on_disk_count

    queue.enqueue(total_count)
    assert queue.in_memory_count == halfway
    assert queue.on_disk_count == 1
    assert queue.count == queue.in_memory_count + queue.on_disk_count

    for i in range(halfway, total_count + 1):
        peek = queue.peek()
        assert i == peek
        assert i == queue.dequeue()
        assert queue.count == queue.in_memory_count
        assert queue.on_disk_count == 0
        assert queue.in_memory_count == total_count - i

    assert queue.count == 0
    assert queue.on_disk_count == 0
    assert queue.in_memory_count == 0

    with pytest.raises(Exception):
        queue.dequeue()
