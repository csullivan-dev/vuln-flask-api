from flask import request, jsonify
from typing import Dict, List, Any, Optional, Union, Tuple
import json
from datetime import datetime

def serialize_user(user) -> Dict[str, Any]:
    """Convert a User model instance to a dictionary for JSON serialization"""
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "address": user.address,
        "phone": user.phone
    }

def serialize_blog_post(post) -> Dict[str, Any]:
    """Convert a BlogPost model instance to a dictionary for JSON serialization"""
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "date": post.date.isoformat() if post.date else None,
        "user_id": post.user_id
    }

# Request validation
def validate_request_data(required_fields: List[str]) -> Tuple[bool, Optional[Dict[str, str]]]:
    """
    Validate that a JSON request contains all required fields
    
    Args:
        required_fields: List of field names that must be present
        
    Returns:
        Tuple containing (is_valid, error_response)
        If valid, error_response will be None
        If invalid, error_response will be a dict that can be returned as JSON
    """
    try:
        data = request.get_json()
        if not data:
            return False, {"error": "No JSON data provided"}
            
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return False, {"error": f"Missing required fields: {', '.join(missing_fields)}"}
            
        return True, None
    except Exception as e:
        return False, {"error": f"Invalid request data: {str(e)}"}

# Error handling
def create_error_response(message: str, status_code: int = 400) -> Tuple[Dict[str, str], int]:
    """Create a standardized error response"""
    return {"error": message}, status_code

# Date/time utilities
def get_current_date():
    """Get current date for consistent date handling"""
    return datetime.now().date()

# Pagination helper
def paginate_results(items: List[Any], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """
    Create a paginated result from a list of items

    Args:
        items: List of items to paginate
        page: Page number (1-indexed)
        per_page: Number of items per page

    Returns:
        Dict with pagination info and page items
    """
    total_pages = (len(items) + per_page - 1) // per_page

    # Ensure page is within valid range
    start = (page - 1) * per_page
    end = start + per_page

    # Return empty list if page is out of bounds
    if page > total_pages:
        paginated_items = []
    else:
        paginated_items = items[start:end]

    return {
        "total": len(items),
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "items": paginated_items
    }

# Security helpers (if needed)
def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters from input"""
    # Simple example - in a real app you'd use a proper HTML sanitizer
    return text.replace("<", "&lt;").replace(">", "&gt;")