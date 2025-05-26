import pytest
from app.models.user import User
from app.models.blog_post import BlogPost

def test_new_user(unit_session):
    """Test creating a new user."""
    user = User(name="test_user", email="test@example.com")
    unit_session.add(user)
    unit_session.commit()
    
    assert user.id is not None
    assert user.name == "test_user"
    assert user.email == "test@example.com"

def test_user_model_initialization(unit_session):
    """Test User model initialization with all valid parameters."""
    user = User(
        name="John Doe",
        email="john@example.com",
        address="123 Main St",
        phone="555-1234"
    )
    unit_session.add(user)
    unit_session.commit()
    
    assert user.id is not None
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.address == "123 Main St"
    assert user.phone == "555-1234"
    assert isinstance(user.posts, list)
    assert len(user.posts) == 0

def test_user_model_defaults(unit_session):
    """Test User model with minimal required fields."""
    # Based on the model, only id is automatically assigned
    user = User()
    unit_session.add(user)
    unit_session.commit()
    
    assert user.id is not None
    assert user.name is None
    assert user.email is None
    assert user.address is None
    assert user.phone is None
    assert isinstance(user.posts, list)
    assert len(user.posts) == 0

def test_user_model_update(unit_session):
    """Test updating User model attributes."""
    user = User(name="Original Name", email="original@example.com")
    unit_session.add(user)
    unit_session.commit()
    
    # Update user attributes
    user.name = "Updated Name"
    user.email = "updated@example.com"
    user.address = "456 New Address"
    user.phone = "555-5678"
    unit_session.commit()
    
    # Fetch fresh from DB to verify persistence
    updated_user = unit_session.query(User).filter_by(id=user.id).first()
    assert updated_user.name == "Updated Name"
    assert updated_user.email == "updated@example.com"
    assert updated_user.address == "456 New Address" 
    assert updated_user.phone == "555-5678"

def test_user_posts_relationship(unit_session):
    """Test the relationship between User and BlogPost models."""
    # Create a test user
    user = User(name="Blog Author", email="author@example.com")
    unit_session.add(user)
    unit_session.commit()
    
    # Create multiple posts linked to the user
    post1 = BlogPost(
        title="First Post",
        body="First post content",
        user_id=user.id
    )
    post2 = BlogPost(
        title="Second Post",
        body="Second post content",
        user_id=user.id
    )
    unit_session.add_all([post1, post2])
    unit_session.commit()
    
    # Test the relationship
    assert len(user.posts) == 2
    assert post1 in user.posts
    assert post2 in user.posts
    assert user.posts[0].title in ["First Post", "Second Post"]
    assert user.posts[1].title in ["First Post", "Second Post"]

def test_cascade_delete(unit_session):
    """Test that deleting a user cascades to delete their posts."""
    # Create a test user
    user = User(name="Delete Test", email="delete@example.com")
    unit_session.add(user)
    unit_session.commit()
    
    # Create posts for this user
    post1 = BlogPost(title="Delete Post 1", body="Content 1", user_id=user.id)
    post2 = BlogPost(title="Delete Post 2", body="Content 2", user_id=user.id)
    unit_session.add_all([post1, post2])
    unit_session.commit()
    
    # Store post IDs
    post1_id = post1.id
    post2_id = post2.id
    
    # Delete the user
    unit_session.delete(user)
    unit_session.commit()
    
    # Check that posts were also deleted
    assert unit_session.query(BlogPost).filter_by(id=post1_id).first() is None
    assert unit_session.query(BlogPost).filter_by(id=post2_id).first() is None

def test_user_representation(unit_session):
    """Test string representation of User model if implemented."""
    user = User(name="Test User", email="test@example.com")
    unit_session.add(user)
    unit_session.commit()
    
    # If __repr__ is implemented, test it
    # Note: This test will pass regardless, but should be updated if 
    # a __repr__ or __str__ method is added to the User model
    str(user)  # This should not raise an exception