import pytest
from app.services.data_structures.custom_queue import Queue

class TestQueue:
    def test_initialization(self):
        """Test that a new queue is initialized properly."""
        queue = Queue()
        assert queue.head is None
        assert queue.tail is None

    def test_enqueue_empty(self):
        """Test enqueueing to an empty queue."""
        queue = Queue()
        queue.enqueue("first")
        
        assert queue.head.data == "first"
        assert queue.tail.data == "first"
        assert queue.head is queue.tail

    def test_enqueue_multiple(self):
        """Test enqueueing multiple items."""
        queue = Queue()
        queue.enqueue("first")
        queue.enqueue("second")
        queue.enqueue("third")
        
        assert queue.head.data == "first"
        assert queue.tail.data == "third"
        assert queue.head.next_node.data == "second"

    def test_dequeue_empty(self):
        """Test dequeueing from an empty queue."""
        queue = Queue()
        result = queue.dequeue()
        assert result is None

    def test_dequeue(self):
        """Test dequeueing from a queue with items."""
        queue = Queue()
        queue.enqueue("first")
        queue.enqueue("second")
        
        # Dequeue first item
        result = queue.dequeue()
        assert result == "first"
        assert queue.head.data == "second"
        assert queue.tail.data == "second"
        
        # Dequeue second item
        result = queue.dequeue()
        assert result == "second"
        assert queue.head is None
        assert queue.tail is None
        
        # Queue is now empty
        result = queue.dequeue()
        assert result is None

    def test_fifo_behavior(self):
        """Test that the queue follows First-In-First-Out behavior."""
        queue = Queue()
        test_items = ["A", "B", "C", "D", "E"]
        
        # Enqueue all items
        for item in test_items:
            queue.enqueue(item)
        
        # Dequeue and verify order
        for expected_item in test_items:
            assert queue.dequeue() == expected_item