class Node:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.posts = []

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def _insert_recursive(self, data, node):
        # Get the ID to compare (use "user_id" if it exists, else use "id")
        data_id = data.get("user_id", data.get("id"))
        node_id = node.data.get("user_id", node.data.get("id"))

        if data_id < node_id:
            if node.left is None:
                node.left = Node(data)
                node.left.posts.append(data)
            else:
                self._insert_recursive(data, node.left)
        elif data_id > node_id:
            if node.right is None:
                node.right = Node(data)
                node.right.posts.append(data)
            else:
                self._insert_recursive(data, node.right)
        else:
            node.posts.append(data)
            return

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            self.root.posts.append(value)
        else:
            self._insert_recursive(value, self.root)

    def _search_recursive(self, user_id, node):
        if node is None:
            return []

        node_id = node.data.get("user_id", node.data.get("id"))

        if user_id == node_id:
            return node.posts

        if user_id < node_id and node.left is not None:
            return self._search_recursive(user_id, node.left)
        elif user_id > node_id and node.right is not None:
            return self._search_recursive(user_id, node.right)
        else:
            return []

    def search(self, user_id):
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            # Handle case where user_id can't be converted to int
            pass
            
        if self.root is None:
            return []

        return self._search_recursive(user_id, self.root)