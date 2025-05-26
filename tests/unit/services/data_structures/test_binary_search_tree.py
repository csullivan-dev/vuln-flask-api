import pytest
from app.services.data_structures.binary_search_tree import BinarySearchTree

class TestBinarySearchTree:
    def test_initialization(self):
        """Test that a new BST is initialized properly."""
        bst = BinarySearchTree()
        assert bst.root is None

    def test_insert(self):
        """Test inserting elements into the BST."""
        bst = BinarySearchTree()
        
        # Insert first element (becomes root)
        bst.insert({"id": 5, "value": "root"})
        assert bst.root.data["id"] == 5
        assert bst.root.data["value"] == "root"
        
        # Insert smaller element (should go left)
        bst.insert({"id": 3, "value": "left"})
        assert bst.root.left.data["id"] == 3
        
        # Insert larger element (should go right)
        bst.insert({"id": 7, "value": "right"})
        assert bst.root.right.data["id"] == 7

    def test_search(self):
        """Test searching for elements by user_id."""
        bst = BinarySearchTree()
        
        # Add test data
        test_data = [
            {"id": 1, "user_id": 100, "value": "A"},
            {"id": 2, "user_id": 200, "value": "B"},
            {"id": 3, "user_id": 100, "value": "C"},
            {"id": 4, "user_id": 300, "value": "D"},
        ]
        
        for item in test_data:
            bst.insert(item)
        
        # Search for existing user_id
        result = bst.search(100)
        assert isinstance(result, list)
        assert len(result) == 2
        assert {"id": 1, "user_id": 100, "value": "A"} in result
        assert {"id": 3, "user_id": 100, "value": "C"} in result
        
        # Search for another user_id
        result = bst.search(200)
        assert len(result) == 1
        assert result[0]["value"] == "B"
        
        # Search for non-existent user_id
        result = bst.search(999)
        assert result == []

    def test_search_empty_tree(self):
        """Test searching an empty tree."""
        bst = BinarySearchTree()
        result = bst.search(100)
        assert result == []

    def test_complex_tree(self):
        """Test a more complex tree structure."""
        bst = BinarySearchTree()
        
        # Insert in non-sorted order to test balancing
        elements = [
            {"id": 5, "user_id": 1},
            {"id": 3, "user_id": 1},
            {"id": 7, "user_id": 2},
            {"id": 2, "user_id": 1},
            {"id": 4, "user_id": 2},
            {"id": 6, "user_id": 1},
            {"id": 8, "user_id": 1},
        ]
        
        for elem in elements:
            bst.insert(elem)
        
        # Test searching different user_ids
        assert len(bst.search(1)) == 5
        assert len(bst.search(2)) == 2
        assert len(bst.search(3)) == 0