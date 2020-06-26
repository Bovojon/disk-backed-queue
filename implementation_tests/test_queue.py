from implementation.queue import Queue
import unittest

class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue(5)

    def test_peek_empty_queue(self):
        self.assertRaises(AssertionError, self.queue.peek)

    def test_peek_non_empty_queue(self):
        for i in [1, 43, 7]:
            self.queue.enqueue(i)
        self.assertEqual(self.queue.peek(), 1)

    def test_enqueue_one_element(self):
        self.queue.enqueue(4)
        self.assertEqual(self.queue.peek(), 4)
        self.assertEqual(self.queue.in_memory_count, 1)

    def test_enqueue_string(self):
        self.queue.enqueue("Hello")
        self.assertEqual(self.queue.peek(), "Hello")

    def test_enqueue_when_full(self):
        for i in [4, 98, 51, 5, 8, 90, 43, 89]:
            self.queue.enqueue(i)
        self.assertEqual(self.queue.on_disk_count, 3)

    def test_full_queue(self):
        for i in [7, 2, 4, 12, 3, 9]:
            self.queue.enqueue(i)
        self.assertTrue(self.queue.is_full)
        self.assertEqual(self.queue.in_memory_count, 5)
        self.assertEqual(self.queue.on_disk_count, 1)
        self.assertEqual(self.queue.count, 6)

    def test_empty_queue_true(self):
        self.assertTrue(self.queue.is_empty)

    def test_empty_queue_false(self):
        self.queue.enqueue(9)
        self.assertFalse(self.queue.is_empty)

    def test_dequeue_empty_queue(self):
        self.assertRaises(AssertionError, self.queue.dequeue)

    def test_dequeue_unfull_queue(self):
        for i in [4, 98, 51]:
            self.queue.enqueue(i)
        self.assertEqual(self.queue.dequeue(), 4)
        self.assertEqual(self.queue.peek(), 98)
        self.assertEqual(self.queue.in_memory_count, 2)
        self.assertEqual(self.queue.on_disk_count, 0)

    def test_dequeue_full_queue(self):
        for i in [12, 83, 51, 100, 8, 90, 43, 89]:
            self.queue.enqueue(i)
        self.assertEqual(self.queue.dequeue(), 12)
        self.assertEqual(self.queue.peek(), 83)
        self.assertEqual(self.queue.in_memory_count, 5)
        self.assertEqual(self.queue.on_disk_count, 2)

    def test_dequeue_one_element(self):
        self.queue.enqueue(4)
        self.assertEqual(self.queue.dequeue(), 4)
        self.assertRaises(AssertionError, self.queue.peek)

    def test_non_int_max_memory(self):
        self.assertRaises(ValueError, Queue, "6")

if __name__ == '__main__':
    unittest.main()
