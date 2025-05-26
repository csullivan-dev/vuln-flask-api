import os
import pytest
import json
from datetime import datetime, date
from unittest.mock import MagicMock
from app import create_app
from app.extensions import db as _db
from app.models.user import User
from app.models.blog_post import BlogPost
from app.services.data_structures.linked_list import LinkedList
from app.services.data_structures.binary_search_tree import BinarySearchTree
from app.services.data_structures.hash_table import HashTable
from app.services.data_structures.custom_queue import Queue
from app.services.data_structures.stack import Stack

# ------------------------------------------------------
# Application & Database Fixtures - Session Level
# ------------------------------------------------------

@pytest.fixture(scope='session')
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')

    # Explicitly set the test database to use an in-memory SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Create a test context and push it
    with app.app_context():
        yield app
    # Context automatically popped after yield


@pytest.fixture(scope='session')
def db(app):
    """Setup and teardown a database for testing."""
    # Create the database and tables within the app context
    _db.create_all()

    yield _db

    # Teardown - drop all tables
    _db.session.remove()
    _db.drop_all()

# ------------------------------------------------------
# Database Fixtures - Function Level
# ------------------------------------------------------

@pytest.fixture(scope='function')
def function_scoped_app():
    """Create a fresh app for each test function that needs it."""
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def function_scoped_db(function_scoped_app):
    """Create a fresh database for each test function that needs it."""
    _db.create_all()
    
    yield _db
    
    _db.session.remove()
    _db.drop_all()

@pytest.fixture(scope='function')
def unit_session(function_scoped_db):
    """Session for unit tests that ensures tables are created for each test."""
    connection = function_scoped_db.engine.connect()
    transaction = connection.begin()
    
    session = function_scoped_db.session
    session.bind = connection
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for each test."""
    # Use the session directly
    session = db.session

    # Set up the session for testing
    connection = db.engine.connect()
    transaction = connection.begin()

    # Bind the session to the connection for the test
    session.bind = connection

    yield session

    # Clean up
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def setup_database(app, db):
    """Create all database tables for testing"""
    with app.app_context():
        # Explicitly create all tables
        db.create_all()
        yield
        # Clean up
        db.drop_all()

# Update the client fixture to depend on setup_database
@pytest.fixture(scope='function')
def client(app, setup_database):
    """A test client for the app."""
    return app.test_client()

# ------------------------------------------------------
# Model Fixtures for Unit Tests
# ------------------------------------------------------

@pytest.fixture
def unit_sample_user(unit_session):
    """Create a sample user for unit testing."""
    user = User(
        name="Test User",
        email="test@example.com",
        address="123 Test St",
        phone="555-1234"
    )
    unit_session.add(user)
    unit_session.commit()
    return user

@pytest.fixture
def unit_sample_blog_post(unit_session, unit_sample_user):
    """Create a sample blog post for unit testing."""
    post = BlogPost(
        title="Test Post",
        body="This is a test post content.",
        date=date.today(),
        user_id=unit_sample_user.id
    )
    unit_session.add(post)
    unit_session.commit()
    return post

# ------------------------------------------------------
# API Test Fixtures
# ------------------------------------------------------

@pytest.fixture
def setup_data(client):
    """Set up users and posts for data structure tests."""
    # Create users
    users = []
    for i in range(5):
        response = client.post(
            '/user',
            json={
                'name': f'dsuser{i}',
                'email': f'ds{i}@example.com',
                'address': f'Address {i}',
                'phone': f'555-{i}{i}{i}{i}'
            }
        )
        print(f"User creation response: {response.data}")
        user_data = json.loads(response.data)

        # Map user_id to id for compatibility with tests
        if 'user_id' in user_data and 'id' not in user_data:
            user_data['id'] = user_data['user_id']

        users.append(user_data)

    # Ensure we have at least one user created
    assert len(users) > 0, "No users were created"

    # Ensure the first user has an ID field
    assert 'id' in users[0], f"First user has no id field. Available fields: {list(users[0].keys())}"

    # Create posts for first user
    user_id = users[0]['id']
    for i in range(5):
        client.post(
            f'/blog_post/{user_id}',
            json={'title': f'DS Post {i}', 'body': f'Test content {i * 10}'}
        )

    return {'users': users}

@pytest.fixture
def test_user(client):
    """Create a test user for blog post tests."""
    response = client.post(
        '/user',
        json={
            'name': 'bloguser',
            'email': 'blog@example.com',
            'address': 'Test Address',
            'phone': '555-1234'
        }
    )
    print(f"Test user creation response: {response.data}")  # Debug print
    user_data = json.loads(response.data)

    # Handle error response
    if 'error' in user_data:
        pytest.fail(f"Failed to create test user: {user_data['error']}")

    # Map user_id to id for compatibility with tests
    if 'user_id' in user_data and 'id' not in user_data:
        user_data['id'] = user_data['user_id']

    # Ensure user has an ID (either original or mapped)
    assert 'id' in user_data, f"User response missing both 'id' and 'user_id' fields. Available fields: {list(user_data.keys())}"

    return user_data

# ------------------------------------------------------
# Original Model Fixtures (keep these for backward compatibility)
# ------------------------------------------------------

@pytest.fixture
def sample_user(session):
    """Create a sample user for testing."""
    user = User(
        name="Test User",
        email="test@example.com",
        address="123 Test St",
        phone="555-1234"
    )
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def sample_users(session):
    """Create multiple sample users for testing."""
    users = []
    for i in range(1, 6):
        user = User(
            name=f"User {i}",
            email=f"user{i}@example.com",
            address=f"Address {i}",
            phone=f"555-{i}{i}{i}{i}"
        )
        session.add(user)
        users.append(user)
    
    session.commit()
    return users

@pytest.fixture
def sample_blog_post(session, sample_user):
    """Create a sample blog post for testing."""
    post = BlogPost(
        title="Test Post",
        body="This is a test post content.",
        date=date.today(),
        user_id=sample_user.id
    )
    session.add(post)
    session.commit()
    return post

@pytest.fixture
def sample_blog_posts(session, sample_user):
    """Create multiple sample blog posts for testing."""
    posts = []
    for i in range(1, 6):
        post = BlogPost(
            title=f"Post {i}",
            body=f"Content for post {i}",
            date=date.today(),
            user_id=sample_user.id
        )
        session.add(post)
        posts.append(post)
    
    session.commit()
    return posts

@pytest.fixture
def multiple_users_with_posts(session):
    """Create multiple users each with multiple blog posts."""
    users = []
    posts = []
    
    # Create users
    for i in range(1, 4):
        user = User(
            name=f"User {i}",
            email=f"user{i}@example.com",
            address=f"Address {i}",
            phone=f"555-{i}{i}{i}{i}"
        )
        session.add(user)
        users.append(user)
    
    session.commit()
    
    # Create posts for each user
    for user in users:
        for j in range(1, 4):
            post = BlogPost(
                title=f"Post {j} by User {user.id}",
                body=f"Content for post {j} by user {user.id}",
                date=date.today(),
                user_id=user.id
            )
            session.add(post)
            posts.append(post)
    
    session.commit()
    return {'users': users, 'posts': posts}

# ------------------------------------------------------
# Data Structure Fixtures
# ------------------------------------------------------

@pytest.fixture
def empty_linked_list():
    """Create an empty linked list for testing."""
    return LinkedList()

@pytest.fixture
def populated_linked_list():
    """Create a linked list with sample data for testing."""
    ll = LinkedList()
    for i in range(5, 0, -1):  # Add 5,4,3,2,1 in reverse order
        ll.insert_beginning({'id': i, 'value': f'Item {i}'})
    return ll

@pytest.fixture
def empty_bst():
    """Create an empty binary search tree for testing."""
    return BinarySearchTree()

@pytest.fixture
def populated_bst():
    """Create a binary search tree with sample data for testing."""
    bst = BinarySearchTree()
    items = [
        {'id': 5, 'user_id': 1, 'value': 'Item 5'},
        {'id': 3, 'user_id': 1, 'value': 'Item 3'},
        {'id': 7, 'user_id': 2, 'value': 'Item 7'},
        {'id': 2, 'user_id': 1, 'value': 'Item 2'},
        {'id': 4, 'user_id': 2, 'value': 'Item 4'},
        {'id': 6, 'user_id': 1, 'value': 'Item 6'},
        {'id': 8, 'user_id': 1, 'value': 'Item 8'},
    ]
    for item in items:
        bst.insert(item)
    return bst

@pytest.fixture
def empty_hash_table():
    """Create an empty hash table for testing."""
    return HashTable(10)

@pytest.fixture
def populated_hash_table():
    """Create a hash table with sample data for testing."""
    ht = HashTable(10)
    ht.add_key_value("name", "Test User")
    ht.add_key_value("email", "test@example.com")
    ht.add_key_value("id", 1)
    return ht

@pytest.fixture
def empty_queue():
    """Create an empty queue for testing."""
    return Queue()

@pytest.fixture
def populated_queue():
    """Create a queue with sample data for testing."""
    queue = Queue()
    for i in range(1, 6):  # Add 1,2,3,4,5
        queue.enqueue(f"Item {i}")
    return queue

@pytest.fixture
def empty_stack():
    """Create an empty stack for testing."""
    return Stack()

@pytest.fixture
def populated_stack():
    """Create a stack with sample data for testing."""
    stack = Stack()
    for i in range(1, 6):  # Add 1,2,3,4,5
        stack.push(f"Item {i}")
    return stack

# ------------------------------------------------------
# Utility Fixtures
# ------------------------------------------------------

@pytest.fixture
def mock_flask_request():
    """Create a mock Flask request for testing utility functions."""
    mock_request = MagicMock()
    mock_request.get_json.return_value = {"name": "Test", "email": "test@example.com"}
    return mock_request

@pytest.fixture
def json_response_validator():
    """Helper function to validate JSON response from API."""
    def _validate(response, expected_status_code=200):
        assert response.status_code == expected_status_code
        assert response.content_type == 'application/json'
        return json.loads(response.data)
    
    return _validate

@pytest.fixture
def api_headers():
    """Common headers for API requests."""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

# ------------------------------------------------------
# Path and Files Fixtures
# ------------------------------------------------------

@pytest.fixture
def test_data_dir():
    """Get the path to the test data directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'tests', 'data')

@pytest.fixture
def load_test_data():
    """Load test data from JSON files."""
    def _load(filename):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'tests', 'data', filename)
        with open(file_path, 'r') as f:
            return json.load(f)
    
    return _load

# ------------------------------------------------------
# Serialization Helpers
# ------------------------------------------------------

class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime objects."""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

@pytest.fixture
def json_serializer():
    """Create a JSON serializer that can handle dates and complex objects."""
    return lambda obj: json.dumps(obj, cls=DateTimeEncoder)

# ------------------------------------------------------
# Integration Test Helpers
# ------------------------------------------------------

@pytest.fixture
def authenticated_client(client, sample_user):
    """A test client with authentication headers set."""
    # This is a simplified example - in a real app, you'd implement proper auth
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Test-User-ID': str(sample_user.id)
    }
    
    class AuthenticatedClient:
        def __init__(self, client, headers):
            self.client = client
            self.headers = headers
        
        def get(self, url, **kwargs):
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers'].update(self.headers)
            return self.client.get(url, **kwargs)
        
        def post(self, url, **kwargs):
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers'].update(self.headers)
            return self.client.post(url, **kwargs)
        
        def put(self, url, **kwargs):
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers'].update(self.headers)
            return self.client.put(url, **kwargs)
        
        def delete(self, url, **kwargs):
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers'].update(self.headers)
            return self.client.delete(url, **kwargs)
    
    return AuthenticatedClient(client, headers)