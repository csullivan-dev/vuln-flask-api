import json

def test_user_lifecycle(client, session):
    """
    Test the complete lifecycle of a user:
    - Create a user
    - Retrieve the user
    - Delete the user
    - Verify user no longer exists
    """
    # Create a user with all required fields
    response = client.post(
        '/user',
        json={
            'name': 'testuser',
            'email': 'test@example.com',
            'address': '123 Test St',
            'phone': '555-1234'
        }
    )
    assert response.status_code == 201
    user_data = json.loads(response.data)
    user_id = user_data['user_id']  # Note: Changed from 'id' to 'user_id' to match the API response

    # Retrieve user by ID
    response = client.get(f'/user/{user_id}')
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == user_id

    # Delete user
    response = client.delete(f'/user/{user_id}')
    assert response.status_code == 200

    # Verify user no longer exists
    response = client.get(f'/user/{user_id}')
    assert response.status_code == 404


def test_user_listing_orders(client, session):
    """
    Test the user listing functionality with different ordering:
    - Create multiple users
    - Verify ascending order endpoint
    - Verify descending order endpoint
    """
    # Create multiple users
    users = []
    for i in range(3):
        response = client.post(
            '/user',
            json={
                'name': f'user{i}',
                'email': f'user{i}@example.com',
                'address': f'Address {i}',
                'phone': f'Phone {i}'
            }
        )
        user_data = json.loads(response.data)
        users.append({'id': user_data['user_id']})

    # Test ascending order
    response = client.get('/user/ascending_id')
    data = json.loads(response.data)
    user_ids = [user['id'] for user in data]
    assert sorted(user_ids) == user_ids

    # Test descending order
    response = client.get('/user/descending_id')
    data = json.loads(response.data)
    user_ids = [user['id'] for user in data]
    assert sorted(user_ids, reverse=True) == user_ids