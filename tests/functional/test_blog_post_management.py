import json

def test_blog_post_lifecycle(client, session, test_user):
    """
    Test the complete lifecycle of blog posts:
    - Create blog posts for a user
    - Retrieve all posts for that user
    - Delete all posts for that user
    - Verify posts no longer exist
    """
    user_id = test_user['id']

    # Create multiple blog posts
    post_ids = []
    for i in range(3):
        response = client.post(
            f'/blog_post/{user_id}',
            json={'title': f'Post {i}', 'body': f'Content {i}'}
        )
        assert response.status_code == 201
        post_data = json.loads(response.data)

        # Adjust to handle response formats that might use blog_post_id instead of id
        post_id = post_data.get('id') or post_data.get('blog_post_id')
        assert post_id is not None, "No post ID found in response"
        post_ids.append(post_id)

    # Retrieve all posts for the user
    response = client.get(f'/blog_post/user/{user_id}')
    assert response.status_code == 200
    posts = json.loads(response.data)
    assert len(posts) == 3

    # Delete all posts for the user
    response = client.delete(f'/blog_post/user/{user_id}')
    assert response.status_code == 200

    # Verify posts no longer exist
    response = client.get(f'/blog_post/user/{user_id}')
    # Handle either 200 with empty array or 404
    if response.status_code == 200:
        assert len(json.loads(response.data)) == 0
    else:
        assert response.status_code == 404


def test_numeric_body_transformation(client, session, test_user):
    """
    Test the numeric body transformation feature:
    - Create posts with numeric content
    - Call the numeric_body endpoint
    - Verify transformation
    """
    user_id = test_user['id']

    # Create posts with numeric content in body
    client.post(
        f'/blog_post/{user_id}',
        json={'title': 'Numeric Post', 'body': 'This post has number 42 in it'}
    )
    client.post(
        f'/blog_post/{user_id}',
        json={'title': 'Another Post', 'body': 'This one has 100 and 200'}
    )

    # Test numeric body transformation
    response = client.get('/blog_post/numeric_body')
    assert response.status_code == 200
    transformed_posts = json.loads(response.data)

    # Verify transformation logic (specific assertions would depend on implementation)
    assert len(transformed_posts) > 0
    # Verify that all post bodies are now integers
    for post in transformed_posts:
        assert isinstance(post["body"], int)