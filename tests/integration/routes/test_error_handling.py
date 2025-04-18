import json
import pytest

def test_malformed_json(client):
    """Test handling of malformed JSON inputs."""
    # Send a request with invalid JSON
    response = client.post(
        '/user',
        data="This is not JSON",
        content_type='application/json'
    )
    
    # Should return 400 Bad Request
    assert response.status_code == 400

def test_method_not_allowed(client):
    """Test handling of invalid HTTP methods."""
    # Try PUT on an endpoint that doesn't support it
    response = client.put('/user/1')
    
    # Should return 405 Method Not Allowed
    assert response.status_code == 405

def test_route_not_found(client):
    """Test handling of nonexistent routes."""
    response = client.get('/nonexistent_route')
    
    # Should return 404 Not Found
    assert response.status_code == 404

def test_invalid_content_type(client):
    """Test handling of requests with incorrect content type."""
    # Send a request with form data instead of JSON
    response = client.post(
        '/user',
        data={'name': 'Test', 'email': 'test@example.com'},
        content_type='application/x-www-form-urlencoded'
    )
    
    # This may return 400 Bad Request or other error code depending on implementation
    assert response.status_code in [400, 415, 422]