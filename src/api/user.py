from flask import request, jsonify
from src.models.user import User  # Ensure correct import for the User model
from src.api.app import db  # Use the same db instance from app initialization
from src.schemas.user import UserCreateSchema, UserUpdateSchema  # Import the Pydantic schemas
from pydantic import ValidationError  # To handle validation errors

class CommonUser:
    def __init__(self, app):
        self.app = app
        return

    def create_user(self):
        """
        curl -X POST http://127.0.0.1:9020/user \
            -H "Content-Type: application/json" \
            -d '{
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "securepassword"
            }'
        :return:
        """
        data = request.get_json()

        try:
            # Validate incoming data with Pydantic
            user_data = UserCreateSchema(**data)
        except ValidationError as e:
            # If validation fails, return the error details
            return jsonify({"error": e.errors()}), 400

        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=user_data.email).first()
        if existing_user:
            return jsonify({"error": "Email already in use"}), 400

        # Create new user if the email is unique
        new_user = User(username=user_data.username, email=user_data.email, password=user_data.password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "user": {"id": new_user.id}}), 201

    def get_users(self):
        """
        get all users
        :return:
        """
        users = User.query.all()
        user_list = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
        return jsonify({"users": user_list}), 200

    def get_user(self, user_id):
        """
        get the user by user_id
        :param user_id:
        :return:
        """
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"id": user.id, "username": user.username, "email": user.email}), 200

    def update_user(self, user_id):
        """
        curl -X PUT http://127.0.0.1:9020/user/1 \
            -H "Content-Type: application/json" \
            -d '{
                "username": "updateduser",
                "email": "updateduser@example.com",
                "password": "newpassword"
            }'
        :param user_id:
        :return:
        """
        data = request.get_json()

        try:
            # Validate incoming data with Pydantic
            user_data = UserUpdateSchema(**data)
        except ValidationError as e:
            # If validation fails, return the error details
            return jsonify({"error": e.errors()}), 400

        # Retrieve the user from the database
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Check if the email is being updated and if it already exists
        if user_data.email and user_data.email != user.email:
            existing_user = User.query.filter_by(email=user_data.email).first()
            if existing_user:
                return jsonify({"error": "Email already in use"}), 400

        # Update user fields with validated data
        user.username = user_data.username or user.username
        user.email = user_data.email or user.email
        user.password = user_data.password or user.password
        db.session.commit()

        return jsonify({"message": "User updated successfully"}), 200

    def delete_user(self, user_id):
        """
        curl -X DELETE http://127.0.0.1:9020/user/1
        :param user_id:
        :return:
        """
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200

    def add_routes(self):
        self.app.add_url_rule('/user', 'get_users', self.get_users, methods=["GET"])
        self.app.add_url_rule('/user', 'create_user', self.create_user, methods=["POST"])
        self.app.add_url_rule('/user/<int:user_id>', 'get_user', self.get_user, methods=["GET"])
        self.app.add_url_rule('/user/<int:user_id>', 'update_user', self.update_user, methods=["PUT"])
        self.app.add_url_rule('/user/<int:user_id>', 'delete_user', self.delete_user, methods=["DELETE"])
