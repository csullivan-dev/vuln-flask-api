import pytest
from datetime import date, datetime, timedelta
from unittest.mock import patch, MagicMock
from flask import Flask, Response, json

from app.utils.helpers import (
    serialize_user,
    serialize_blog_post,
    validate_request_data,
    create_error_response,
    get_current_date,
    paginate_results,
    sanitize_input
)

class TestSerializers:
    def test_serialize_user_complete(self):
        """Test serializing a user with all fields."""
        # Create a mock user object
        user = MagicMock()
        user.id = 1
        user.name = "Test User"
        user.email = "test@example.com"
        user.address = "123 Test St"
        user.phone = "555-1234"
        
        result = serialize_user(user)
        
        assert result == {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "address": "123 Test St",
            "phone": "555-1234"
        }
    
    def test_serialize_user_null_fields(self):
        """Test serializing a user with null fields."""
        user = MagicMock()
        user.id = 1
        user.name = None
        user.email = "test@example.com"
        user.address = None
        user.phone = None
        
        result = serialize_user(user)
        
        assert result == {
            "id": 1,
            "name": None,
            "email": "test@example.com",
            "address": None,
            "phone": None
        }
    
    def test_serialize_blog_post_complete(self):
        """Test serializing a blog post with all fields."""
        post = MagicMock()
        post.id = 1
        post.title = "Test Post"
        post.body = "Test Content"
        post.date = date(2023, 1, 1)
        post.user_id = 5
        
        result = serialize_blog_post(post)
        
        assert result == {
            "id": 1,
            "title": "Test Post",
            "body": "Test Content",
            "date": "2023-01-01",
            "user_id": 5
        }
    
    def test_serialize_blog_post_null_date(self):
        """Test serializing a blog post with null date."""
        post = MagicMock()
        post.id = 1
        post.title = "Test Post"
        post.body = "Test Content"
        post.date = None
        post.user_id = 5
        
        result = serialize_blog_post(post)
        
        assert result == {
            "id": 1,
            "title": "Test Post",
            "body": "Test Content",
            "date": None,
            "user_id": 5
        }

class TestRequestValidation:
    @pytest.fixture
    def app(self):
        """Create a Flask app for testing."""
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
    
    def test_validate_request_data_valid(self, app):
        """Test validating a request with all required fields."""
        with app.test_request_context(
            json={"name": "Test", "email": "test@example.com"}
        ):
            is_valid, error = validate_request_data(["name", "email"])
            assert is_valid is True
            assert error is None
    
    def test_validate_request_data_missing_fields(self, app):
        """Test validating a request with missing fields."""
        with app.test_request_context(
            json={"name": "Test"}
        ):
            is_valid, error = validate_request_data(["name", "email"])
            assert is_valid is False
            assert "Missing required fields" in error["error"]
            assert "email" in error["error"]
    
    def test_validate_request_data_no_json(self, app):
        """Test validating a request with no JSON data."""
        with app.test_request_context():
            is_valid, error = validate_request_data(["name"])
            assert is_valid is False
            assert "Invalid request data" in error["error"]


    def test_validate_request_data_invalid_json(self, app):
        """Test validating a request with invalid JSON."""
        with app.test_request_context():
            # Use Flask's request object directly with patching
            with patch('flask.request.get_json', side_effect=Exception("Invalid JSON")):
                is_valid, error = validate_request_data(["name"])
                assert is_valid is False
                assert "Invalid request data" in error["error"]

class TestErrorHandling:
    def test_create_error_response_default_status(self):
        """Test creating an error response with default status code."""
        response, status_code = create_error_response("Test error")
        assert response == {"error": "Test error"}
        assert status_code == 400
    
    def test_create_error_response_custom_status(self):
        """Test creating an error response with custom status code."""
        response, status_code = create_error_response("Not found", 404)
        assert response == {"error": "Not found"}
        assert status_code == 404

class TestDateTimeUtils:
    def test_get_current_date(self):
        """Test getting the current date."""
        with patch('app.utils.helpers.datetime') as mock_datetime:
            # Set a fixed date for testing
            fixed_date = datetime(2023, 1, 15)
            mock_datetime.now.return_value = fixed_date
            
            result = get_current_date()
            
            assert result == date(2023, 1, 15)
            mock_datetime.now.assert_called_once()

class TestPagination:
    def test_paginate_results_first_page(self):
        """Test paginating results - first page."""
        items = list(range(25))  # 25 items
        result = paginate_results(items, page=1, per_page=10)
        
        assert result["total"] == 25
        assert result["page"] == 1
        assert result["per_page"] == 10
        assert result["total_pages"] == 3
        assert result["items"] == list(range(10))  # First 10 items
    
    def test_paginate_results_middle_page(self):
        """Test paginating results - middle page."""
        items = list(range(25))
        result = paginate_results(items, page=2, per_page=10)
        
        assert result["total"] == 25
        assert result["page"] == 2
        assert result["per_page"] == 10
        assert result["total_pages"] == 3
        assert result["items"] == list(range(10, 20))  # Items 10-19
    
    def test_paginate_results_last_page(self):
        """Test paginating results - last page."""
        items = list(range(25))
        result = paginate_results(items, page=3, per_page=10)
        
        assert result["total"] == 25
        assert result["page"] == 3
        assert result["per_page"] == 10
        assert result["total_pages"] == 3
        assert result["items"] == list(range(20, 25))  # Last 5 items
    
    def test_paginate_results_empty_list(self):
        """Test paginating an empty list."""
        result = paginate_results([], page=1, per_page=10)
        
        assert result["total"] == 0
        assert result["page"] == 1
        assert result["per_page"] == 10
        assert result["total_pages"] == 0
        assert result["items"] == []
    
    def test_paginate_results_page_out_of_bounds(self):
        """Test paginating with a page number that's out of bounds."""
        items = list(range(5))
        result = paginate_results(items, page=4, per_page=2)
        
        assert result["total"] == 5
        assert result["page"] == 4
        assert result["per_page"] == 2
        assert result["total_pages"] == 3
        assert result["items"] == []  # No items on this page
    
    def test_paginate_results_default_values(self):
        """Test paginating with default values."""
        items = list(range(25))
        result = paginate_results(items)
        
        assert result["page"] == 1
        assert result["per_page"] == 10
        assert result["items"] == list(range(10))

class TestSecurity:
    def test_sanitize_input_no_html(self):
        """Test sanitizing input with no HTML tags."""
        input_text = "Normal text without HTML"
        result = sanitize_input(input_text)
        assert result == input_text
    
    def test_sanitize_input_with_html(self):
        """Test sanitizing input containing HTML tags."""
        input_text = "<script>alert('XSS')</script>Normal text<b>bold</b>"
        expected = "&lt;script&gt;alert('XSS')&lt;/script&gt;Normal text&lt;b&gt;bold&lt;/b&gt;"
        result = sanitize_input(input_text)
        assert result == expected
    
    def test_sanitize_input_empty_string(self):
        """Test sanitizing an empty string."""
        result = sanitize_input("")
        assert result == ""