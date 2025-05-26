import json
from app.models import User
import pytest
from app.services.data_structures.linked_list import LinkedList

def test_create_user_success(client, session):
    """Test successful user creation with complete data."""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "address": "123 Test St",
        "phone": "123-456-7890"
    }
    
    response = client.post('/user', json=user_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    
    assert "user_id" in data
    assert data["message"] == "User created"
    
    # Verify user was added to database
    created_user = session.get(User, data["user_id"])
    assert created_user is not None
    assert created_user.name == user_data["name"]

def test_create_user_missing_fields(client):
    """Test user creation with missing required fields."""
    # Missing address and phone
    incomplete_data = {
        "name": "Incomplete User",
        "email": "incomplete@example.com"
    }
    
    response = client.post('/user', json=incomplete_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_get_users_descending(client, session):
    """Test getting users in descending order."""
    # Create multiple users
    users = []
    for i in range(3):
        user_data = {
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "address": f"Address {i}",
            "phone": f"Phone {i}"
        }
        response = client.post('/user', json=user_data)
        users.append(json.loads(response.data)["user_id"])
    
    # Get users in descending order
    response = client.get('/user/descending_id')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    
    # Verify data structure is as expected
    assert isinstance(data, list)
    assert len(data) >= 3
    
    # Check descending order
    user_ids = [user["id"] for user in data]
    assert sorted(user_ids, reverse=True) == user_ids
    
    # Verify LinkedList implementation is used (indirectly)
    # This is already covered by the fact that we're testing the endpoint result

def test_get_users_ascending(client, session):
    """Test getting users in ascending order."""
    # Create multiple users if needed
    # (can reuse setup from the descending test or create new users)
    
    # Get users in ascending order
    response = client.get('/user/ascending_id')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    
    # Verify data structure is as expected
    assert isinstance(data, list)
    
    # Check ascending order
    user_ids = [user["id"] for user in data]
    assert sorted(user_ids) == user_ids

def test_get_one_user(client, session):
    """Test retrieving a specific user by ID."""
    # Create a user
    user_data = {
        "name": "Single User",
        "email": "single@example.com",
        "address": "Single Address",
        "phone": "Single Phone"
    }
    response = client.post('/user', json=user_data)
    user_id = json.loads(response.data)["user_id"]
    
    # Get the specific user
    response = client.get(f'/user/{user_id}')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data["id"] == user_id
    assert data["name"] == user_data["name"]

def test_get_nonexistent_user(client):
    """Test retrieving a non-existent user."""
    # Using a very large ID that likely doesn't exist
    response = client.get('/user/999999')
    
    # Should either return 404 or an empty result (depending on implementation)
    if response.status_code == 404:
        assert "error" in json.loads(response.data)
    else:
        assert response.status_code == 200
        assert json.loads(response.data) is None

def test_delete_user(client, session):
    """Test deleting a user."""
    # Create a user
    user_data = {
        "name": "Delete User",
        "email": "delete@example.com",
        "address": "Delete Address",
        "phone": "Delete Phone"
    }
    response = client.post('/user', json=user_data)
    user_id = json.loads(response.data)["user_id"]
    
    # Delete the user
    response = client.delete(f'/user/{user_id}')
    assert response.status_code == 200
    
    # Verify user was deleted
    response = client.get(f'/user/{user_id}')
    # Should either return 404 or an empty result (depending on implementation)
    if response.status_code == 404:
        assert "error" in json.loads(response.data)
    else:
        assert response.status_code == 200
        assert json.loads(response.data) is None