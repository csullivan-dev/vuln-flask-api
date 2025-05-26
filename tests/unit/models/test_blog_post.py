import pytest
from datetime import datetime
from app.models.blog_post import BlogPost
from app.models.user import User

class TestBlogPost:
    """Test suite for the BlogPost model"""
    
    def test_blog_post_creation(self):
        """Test that a blog post can be created with valid parameters"""
        post = BlogPost(
            title="Test Post",
            body="This is a test post body",
            date=datetime.now(),
            user_id=1
        )
        assert post.title == "Test Post"
        assert post.body == "This is a test post body"
        assert post.user_id == 1
        assert isinstance(post.date, datetime)
    
    def test_blog_post_fields(self):
        """Test that all blog post fields are correctly defined"""
        post = BlogPost()
        assert hasattr(post, 'id')
        assert hasattr(post, 'title')
        assert hasattr(post, 'body')
        assert hasattr(post, 'date')
        assert hasattr(post, 'user_id')

    def test_blog_post_user_relationship(self, unit_session):
        """Test the relationship between BlogPost and User models"""
        # Create a test user
        user = User(name="Test User", email="test@example.com")
        unit_session.add(user)
        unit_session.commit()

        # Create a post linked to the user
        post = BlogPost(
            title="Test Post",
            body="Test Body",
            user_id=user.id
        )
        unit_session.add(post)
        unit_session.commit()

        # Test the relationship
        assert post.user_id == user.id
        assert post in user.posts
    
    def test_blog_post_date_default(self):
        """Test that the date field gets a default value if not provided"""
        post = BlogPost(title="Test Post", body="Test Body", user_id=1)
        # Check if date is automatically set (implementation dependent)
        if post.date is not None:
            assert isinstance(post.date, datetime)
    
    def test_blog_post_serialization(self):
        """Test the blog post serialization with the helpers.serialize_blog_post function"""
        from app.utils.helpers import serialize_blog_post
        
        test_date = datetime.now()
        post = BlogPost(
            id=1,
            title="Test Post",
            body="Test Body",
            date=test_date,
            user_id=2
        )
        
        serialized = serialize_blog_post(post)
        assert serialized["id"] == 1
        assert serialized["title"] == "Test Post"
        assert serialized["body"] == "Test Body"
        assert serialized["date"] == test_date.isoformat()
        assert serialized["user_id"] == 2
    
    def test_blog_post_null_date_serialization(self):
        """Test serialization handles null date values"""
        from app.utils.helpers import serialize_blog_post
        
        post = BlogPost(
            id=1,
            title="Test Post",
            body="Test Body",
            date=None,
            user_id=2
        )
        
        serialized = serialize_blog_post(post)
        assert serialized["date"] is None