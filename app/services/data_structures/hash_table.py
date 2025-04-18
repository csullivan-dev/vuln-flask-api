class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

class Data:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

class HashTable:
    def __init__(self, table_size):
        self.size = table_size  # Renamed from table_size to size
        self.buckets = [None] * table_size  # Renamed from hash_table to buckets

    def custom_hash(self, key):
        hash_value = 0
        for char in key:
            hash_value += ord(char)
            hash_value = (hash_value * ord(char)) % self.size  # Use self.size instead of self.table_size
        return hash_value

    def add_key_value(self, key, value):
        hashed_key = self.custom_hash(key)
        if self.buckets[hashed_key] is None:
            self.buckets[hashed_key] = Node(Data(key, value), None)
        else:
            # Check if key already exists and update if it does
            node = self.buckets[hashed_key]
            # Check first node
            if node.data.key == key:
                node.data.value = value
                return
                
            # Check subsequent nodes
            prev = node
            while node.next_node:
                node = node.next_node
                if node.data.key == key:
                    node.data.value = value
                    return
                prev = node
            
            # If we get here, key doesn't exist, so add a new node
            node.next_node = Node(Data(key, value), None)

    def get_value(self, key):
        hashed_key = self.custom_hash(key)
        if self.buckets[hashed_key] is not None:
            node = self.buckets[hashed_key]
            if node.next_node is None:
                if key == node.data.key:
                    return node.data.value
                return None
            
            while node:
                if key == node.data.key:
                    return node.data.value
                node = node.next_node
        return None

    def print_table(self):
        print("{")
        for i, val in enumerate(self.buckets):  # Use self.buckets instead of self.hash_table
            if val is not None:
                llist_string = ""
                node = val
                if node.next_node:
                    while node.next_node:
                        llist_string += (
                            str(node.data.key) + " : " + str(node.data.value) + " --> "
                        )
                        node = node.next_node
                    llist_string += (str(node.data.key) + " : " + str(node.data.value) + " --> None")
                    print(f"    [{i}] {llist_string}")
                else:
                    print(f"    [{i}] {val.data.key} : {val.data.value}")
            else:
                print(f"    [{i}] {val}")
        print("}")