import json
import pytest
from datetime import datetime

@pytest.fixture
def test_user(client):
    """Create a test user for blog post tests."""
    user_data = {
        "name": "Blog User",
        "email": "blog@example.com",
        "address": "Blog Address",
        "phone": "Blog Phone"
    }
    response = client.post('/user', json=user_data)
    user_id = json.loads(response.data)["user_id"]
    return user_id

def test_create_blog_post_success(client, session, test_user):
    """Test successful blog post creation."""
    post_data = {
        "title": "Test Post",
        "body": "This is a test post body."
    }
    
    response = client.post(f'/blog_post/{test_user}', json=post_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    
    assert "blog_post_id" in data
    assert data["message"] == "Blog post created"

def test_create_blog_post_missing_fields(client, test_user):
    """Test blog post creation with missing required fields."""
    # Missing body
    incomplete_data = {
        "title": "Incomplete Post"
    }
    
    response = client.post(f'/blog_post/{test_user}', json=incomplete_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_create_blog_post_nonexistent_user(client):
    """Test creating a blog post for a non-existent user."""
    post_data = {
        "title": "Non-existent User Post",
        "body": "This post should not be created."
    }
    
    response = client.post('/blog_post/999999', json=post_data)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data

def test_get_numeric_post_bodies(client, test_user):
    """Test retrieving posts with numeric body transformation."""
    # Create some posts
    post_data1 = {"title": "Numeric Post 1", "body": "ABC"}
    post_data2 = {"title": "Numeric Post 2", "body": "XYZ"}
    
    client.post(f'/blog_post/{test_user}', json=post_data1)
    client.post(f'/blog_post/{test_user}', json=post_data2)
    
    # Get numeric bodies
    response = client.get('/blog_post/numeric_body')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    
    # Verify numeric transformation
    for post in data:
        assert isinstance(post["body"], int)
        # Check if ABC's sum equals the first post's body value (exact value depends on character encodings)
        if post["title"] == "Numeric Post 1":
            assert post["body"] == sum(ord(c) for c in "ABC")
        elif post["title"] == "Numeric Post 2":
            assert post["body"] == sum(ord(c) for c in "XYZ")

def test_get_all_blog_posts_for_user(client, test_user):
    """Test retrieving all blog posts for a specific user."""
    # Create multiple posts for the user
    post_titles = ["Post 1", "Post 2", "Post 3"]
    for title in post_titles:
        post_data = {
            "title": title,
            "body": f"Body for {title}"
        }
        client.post(f'/blog_post/{test_user}', json=post_data)
    
    # Get posts for the user
    response = client.get(f'/blog_post/user/{test_user}')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    
    # Verify all posts belong to the user
    assert len(data) >= len(post_titles)
    for post in data:
        assert post["user_id"] == int(test_user)
    
    # Verify all created posts are present
    returned_titles = [post["title"] for post in data]
    for title in post_titles:
        assert title in returned_titles

def test_get_blog_posts_for_nonexistent_user(client):
    """Test retrieving blog posts for a non-existent user."""
    response = client.get('/blog_post/user/999999')
    
    # The route should return 404 if user posts are not found
    if response.status_code == 404:
        data = json.loads(response.data)
        assert "error" in data
    else:
        # Or possibly an empty list if that's the behavior
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 0

def test_delete_all_blog_posts_for_user(client, test_user):
    """Test deleting all blog posts for a user."""
    # Create posts for user
    for i in range(3):
        post_data = {
            "title": f"Delete Post {i}",
            "body": f"Body for delete post {i}"
        }
        client.post(f'/blog_post/{test_user}', json=post_data)
    
    # Verify posts exist
    response = client.get(f'/blog_post/user/{test_user}')
    before_delete = json.loads(response.data)
    assert len(before_delete) >= 3
    
    # Delete all posts
    response = client.delete(f'/blog_post/user/{test_user}')
    assert response.status_code == 200
    
    # Verify posts were deleted
    response = client.get(f'/blog_post/user/{test_user}')
    after_delete = json.loads(response.data)
    
    # Should either return 404 or an empty list (depending on implementation)
    if response.status_code == 404:
        assert "error" in after_delete
    else:
        assert response.status_code == 200
        assert len(after_delete) == 0

def test_delete_posts_for_nonexistent_user(client):
    """Test deleting blog posts for a non-existent user."""
    response = client.delete('/blog_post/user/999999')
    
    # Should return 404 as there are no blog posts to delete
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data