from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.services.data_structures.linked_list import LinkedList

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route("", methods=["POST"])
def create_user():
    try:
        # Check content type first
        if request.content_type != 'application/json':
            return jsonify({"error": "Content-Type must be application/json"}), 415

        # Try to parse JSON data
        data = request.get_json()

        # If data is None, it means the JSON was malformed
        if data is None:
            return jsonify({"error": "Invalid JSON format"}), 400

        if not all(key in data for key in ["name", "email", "address", "phone"]):
            return jsonify({"error": "Missing required fields"}), 400

        new_user = User(
            name=data["name"],
            email=data["email"],
            address=data["address"],
            phone=data["phone"]
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created", "user_id": new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_bp.route("/descending_id", methods=["GET"])
def get_all_users_descending():
    try:
        users = User.query.all()
        all_users_ll = LinkedList()
        for user in users:
            all_users_ll.insert_beginning(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "address": user.address,
                    "phone": user.phone
                }
            )
        return jsonify(all_users_ll.to_list()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/ascending_id", methods=["GET"])
def get_all_users_ascending():
    try:
        users = User.query.order_by(User.id).all()
        all_users_ll = LinkedList()
        for user in users:
            all_users_ll.insert_at_end(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "address": user.address,
                    "phone": user.phone
                }
            )
        return jsonify(all_users_ll.to_list()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()
    all_users_ll = LinkedList()
    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )

    user = all_users_ll.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500