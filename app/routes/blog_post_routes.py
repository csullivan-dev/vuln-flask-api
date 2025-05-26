from flask import Blueprint, request, jsonify
from app import db
from app.models.blog_post import BlogPost
from app.models.user import User
from app.services.data_structures.hash_table import HashTable
from app.services.data_structures.binary_search_tree import BinarySearchTree
from app.services.data_structures.custom_queue import Queue
from app.services.data_structures.stack import Stack
from datetime import datetime

blog_post_bp = Blueprint('blog_post', __name__, url_prefix='/blog_post')

@blog_post_bp.route("/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    if "title" not in data or "body" not in data:
        return jsonify({"error": "Missing required fields (title, body)"}), 400

    ht = HashTable(10)
    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", datetime.now().date())
    ht.add_key_value("user_id", user_id)

    new_blog_post = BlogPost(
        title=ht.get_value("title"),
        body=ht.get_value("body"),
        date=ht.get_value("date"),
        user_id=ht.get_value("user_id")
    )
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message": "Blog post created", "blog_post_id": new_blog_post.id}), 201

@blog_post_bp.route("/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    blog_posts = BlogPost.query.all()
    queue = Queue()

    for post in blog_posts:
        queue.enqueue(post)

    return_list = []

    for _ in range(len(blog_posts)):
        post = queue.dequeue()
        numeric_body = 0
        for char in post.body:
            numeric_body += ord(char)

        post.body = numeric_body

        return_list.append({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id
        })

    return jsonify(return_list), 200

# Route for user's blog posts (moved from user routes for better organization)
@blog_post_bp.route("/user/<user_id>", methods=["GET"])
def get_all_blog_posts(user_id):
    blog_posts = BlogPost.query.all()
    
    bst = BinarySearchTree()
    for post in blog_posts:
        bst.insert({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id
        })
    
    user_posts = bst.search(user_id)
    
    if not user_posts:
        return jsonify({"error": "Posts not found for user"}), 404
    
    return jsonify(user_posts), 200


@blog_post_bp.route("/user/<user_id>", methods=["DELETE"])
def delete_all_blog_posts(user_id):
    blog_posts = BlogPost.query.filter_by(user_id=user_id).all()

    if not blog_posts:
        return jsonify({"error": "No blog posts found for this user"}), 404

    stack_instance = Stack()

    # Store the actual BlogPost objects in the stack
    for post in blog_posts:
        stack_instance.push(post)

    # When popping from the stack, we need to retrieve the actual BlogPost object
    for _ in range(len(blog_posts)):
        node = stack_instance.pop()
        if node:
            # The node is an instance of Node, but we need to access the data attribute
            post_to_delete = node.data
            db.session.delete(post_to_delete)
            db.session.commit()

    return jsonify({"message": "Blog posts successfully deleted"}), 200