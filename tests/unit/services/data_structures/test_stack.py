import pytest
from app.services.data_structures.stack import Stack, Node

class TestStack:
    def test_initialization(self):
        """Test that a new stack is initialized properly."""
        stack = Stack()
        assert stack.top is None

    def test_push(self):
        """Test that we can push items onto the stack."""
        stack = Stack()
        stack.push("first")
        assert stack.top.data == "first"
        assert stack.top.next_node is None
        
        # Push another item
        stack.push("second")
        assert stack.top.data == "second"
        assert stack.top.next_node.data == "first"

    def test_peek(self):
        """Test that peek returns the top node without removing it."""
        stack = Stack()
        assert stack.peek() is None
        
        stack.push("item")
        assert stack.peek().data == "item"
        
        # Verify peek didn't remove the item
        assert stack.top.data == "item"

    def test_pop(self):
        """Test that pop removes and returns the top item."""
        stack = Stack()
        
        # Test popping from empty stack
        assert stack.pop() is None
        
        # Add items and test popping
        stack.push("first")
        stack.push("second")
        
        popped = stack.pop()
        assert popped.data == "second"
        assert stack.top.data == "first"
        
        popped = stack.pop()
        assert popped.data == "first"
        assert stack.top is None
        
        # Pop from empty stack again
        assert stack.pop() is None

    def test_complex_operations(self):
        """Test sequence of stack operations."""
        stack = Stack()
        
        # Push multiple items
        for i in range(5):
            stack.push(i)
        
        # Pop and verify order (LIFO)
        for i in range(4, -1, -1):
            assert stack.pop().data == i