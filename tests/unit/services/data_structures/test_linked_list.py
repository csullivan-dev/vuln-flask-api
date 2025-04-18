import pytest
from app.services.data_structures.linked_list import LinkedList, Node

class TestLinkedList:
    def test_initialization(self):
        """Test that a new linked list is initialized properly."""
        ll = LinkedList()
        assert ll.head is None
        assert ll.last_node is None
        assert ll.to_list() == []

    def test_insert_beginning_empty_list(self):
        """Test inserting at the beginning of an empty list."""
        ll = LinkedList()
        ll.insert_beginning({'id': 1})
        
        assert ll.head is not None
        assert ll.head.data == {'id': 1}
        assert ll.last_node == ll.head
        assert ll.get_length() == 1
        assert ll.to_list() == [{'id': 1}]

    def test_insert_beginning_non_empty_list(self):
        """Test inserting at the beginning of a non-empty list."""
        ll = LinkedList()
        ll.insert_beginning({'id': 1})
        ll.insert_beginning({'id': 2})
        
        assert ll.head.data == {'id': 2}
        assert ll.head.next_node.data == {'id': 1}
        assert ll.get_length() == 2
        assert ll.to_list() == [{'id': 2}, {'id': 1}]

    def test_insert_at_end_empty_list(self):
        """Test inserting at the end of an empty list."""
        ll = LinkedList()
        ll.insert_at_end({'id': 1})
        
        assert ll.head is not None
        assert ll.head.data == {'id': 1}
        assert ll.last_node == ll.head
        assert ll.get_length() == 1
        assert ll.to_list() == [{'id': 1}]

    def test_insert_at_end_non_empty_list(self):
        """Test inserting at the end of a non-empty list."""
        ll = LinkedList()
        ll.insert_at_end({'id': 1})
        ll.insert_at_end({'id': 2})
        
        assert ll.head.data == {'id': 1}
        assert ll.last_node.data == {'id': 2}
        assert ll.get_length() == 2
        assert ll.to_list() == [{'id': 1}, {'id': 2}]

    def test_mixed_insertions(self):
        """Test mixed insertions (beginning and end)."""
        ll = LinkedList()
        ll.insert_beginning({'id': 2})
        ll.insert_at_end({'id': 3})
        ll.insert_beginning({'id': 1})
        ll.insert_at_end({'id': 4})
        
        assert ll.get_length() == 4
        assert ll.to_list() == [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}]

    def test_remove_beginning_empty_list(self):
        """Test removing from the beginning of an empty list."""
        ll = LinkedList()
        removed = ll.remove_beginning()
        
        assert removed is None
        assert ll.head is None
        assert ll.last_node is None
        assert ll.get_length() == 0

    def test_remove_beginning_single_item(self):
        """Test removing from the beginning of a list with a single item."""
        ll = LinkedList()
        ll.insert_beginning({'id': 1})
        
        removed = ll.remove_beginning()
        
        assert removed == {'id': 1}
        assert ll.head is None
        assert ll.last_node is None
        assert ll.get_length() == 0

    def test_remove_beginning_multiple_items(self):
        """Test removing from the beginning of a list with multiple items."""
        ll = LinkedList()
        ll.insert_beginning({'id': 1})
        ll.insert_beginning({'id': 2})
        ll.insert_beginning({'id': 3})
        
        removed = ll.remove_beginning()
        
        assert removed == {'id': 3}
        assert ll.head.data == {'id': 2}
        assert ll.get_length() == 2
        
        removed = ll.remove_beginning()
        
        assert removed == {'id': 2}
        assert ll.head.data == {'id': 1}
        assert ll.head == ll.last_node
        assert ll.get_length() == 1

    def test_get_user_by_id_found(self):
        """Test getting a user by ID when the user exists."""
        ll = LinkedList()
        ll.insert_beginning({'id': 1, 'name': 'Alice'})
        ll.insert_beginning({'id': 2, 'name': 'Bob'})
        ll.insert_beginning({'id': 3, 'name': 'Charlie'})
        
        user = ll.get_user_by_id(2)
        
        assert user == {'id': 2, 'name': 'Bob'}

    def test_get_user_by_id_not_found(self):
        """Test getting a user by ID when the user doesn't exist."""
        ll = LinkedList()
        ll.insert_beginning({'id': 1, 'name': 'Alice'})
        ll.insert_beginning({'id': 2, 'name': 'Bob'})
        
        user = ll.get_user_by_id(3)
        
        assert user is None

    def test_get_user_by_id_empty_list(self):
        """Test getting a user by ID from an empty list."""
        ll = LinkedList()
        user = ll.get_user_by_id(1)
        
        assert user is None

    def test_get_user_by_id_with_string_id(self):
        """Test getting a user by ID with a string ID parameter."""
        ll = LinkedList()
        ll.insert_beginning({'id': 1, 'name': 'Alice'})
        ll.insert_beginning({'id': 2, 'name': 'Bob'})
        
        user = ll.get_user_by_id("2")  # Note the string ID
        
        assert user == {'id': 2, 'name': 'Bob'}

    def test_to_list_empty(self):
        """Test to_list method on an empty list."""
        ll = LinkedList()
        assert ll.to_list() == []

    def test_to_list_with_items(self):
        """Test to_list method on a list with items."""
        ll = LinkedList()
        ll.insert_beginning({'id': 3})
        ll.insert_beginning({'id': 2})
        ll.insert_beginning({'id': 1})
        
        assert ll.to_list() == [{'id': 1}, {'id': 2}, {'id': 3}]

    def test_get_length(self):
        """Test get_length method."""
        ll = LinkedList()
        assert ll.get_length() == 0
        
        ll.insert_beginning({'id': 1})
        assert ll.get_length() == 1
        
        ll.insert_beginning({'id': 2})
        ll.insert_at_end({'id': 3})
        assert ll.get_length() == 3
        
        ll.remove_beginning()
        assert ll.get_length() == 2

    def test_print_ll(self, capsys):
        """Test print_ll method."""
        ll = LinkedList()
        ll.print_ll()
        captured = capsys.readouterr()
        assert captured.out.strip() == "None"
        
        ll.insert_beginning({'id': 2})
        ll.insert_beginning({'id': 1})
        ll.print_ll()
        captured = capsys.readouterr()
        assert "{'id': 1}" in captured.out
        assert "{'id': 2}" in captured.out
        assert "->" in captured.out
        assert "None" in captured.out