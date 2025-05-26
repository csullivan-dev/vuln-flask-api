import pytest
from app.services.data_structures.hash_table import HashTable

class TestHashTable:
    def test_initialization(self):
        """Test that hash table is initialized with correct size."""
        ht = HashTable(10)
        assert ht.size == 10
        assert len(ht.buckets) == 10
        for bucket in ht.buckets:
            assert bucket is None

    def test_hash(self):
        """Test the hash function produces expected values."""
        ht = HashTable(10)
        # Hash should be consistent for the same key
        key = "test_key"
        hash1 = ht.custom_hash(key)
        hash2 = ht.custom_hash(key)
        assert hash1 == hash2
        
        # Hash should be within bounds of table size
        assert 0 <= hash1 < ht.size

    def test_add_key_value(self):
        """Test adding key-value pairs to the hash table."""
        ht = HashTable(5)
        ht.add_key_value("name", "Alice")
        ht.add_key_value("age", 30)
        
        # Check if keys are stored correctly
        assert ht.get_value("name") == "Alice"
        assert ht.get_value("age") == 30
        
        # Test overwriting existing key
        ht.add_key_value("name", "Bob")
        assert ht.get_value("name") == "Bob"

    def test_get_value(self):
        """Test retrieving values from the hash table."""
        ht = HashTable(5)
        
        # Test getting non-existent key
        assert ht.get_value("nonexistent") is None
        
        # Add and retrieve values
        ht.add_key_value("key1", "value1")
        ht.add_key_value("key2", 42)
        
        assert ht.get_value("key1") == "value1"
        assert ht.get_value("key2") == 42
        
        # Test case-sensitivity
        ht.add_key_value("Key", "CaseSensitive")
        assert ht.get_value("Key") == "CaseSensitive"
        assert ht.get_value("key") is None

    def test_collision_handling(self):
        """Test that hash table handles collisions correctly."""
        # Create tiny hash table to force collisions
        ht = HashTable(2)
        
        # Add multiple items (will definitely cause collisions)
        test_data = {
            "a": 1, "b": 2, "c": 3, "d": 4, "e": 5
        }
        
        for key, value in test_data.items():
            ht.add_key_value(key, value)
        
        # Check all values can be retrieved correctly
        for key, value in test_data.items():
            assert ht.get_value(key) == value