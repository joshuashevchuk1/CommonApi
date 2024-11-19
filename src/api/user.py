from flask import request, jsonify
import src.models.user as user_model
from src.api.app import db


class CommonUser:
    def __init__(self, app):
        self.app = app
        return

    def create_user(self):
        """
        curl -X POST http://127.0.0.1:5000/user \
            -H "Content-Type: application/json" \
            -d '{
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "securepassword"
            }'
        :return:
        """
        data = request.get_json()
        if not data or not all(k in data for k in ("username", "email", "password")):
            return jsonify({"error": "Invalid data"}), 400

        new_user = user_model.User(username=data["username"], email=data["email"], password=data["password"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully", "user": {"id": new_user.id}}), 201

    def get_users(self):
        """
        get all users
        :return:
        """
        users = user_model.User.query.all()
        user_list = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
        return jsonify({"users": user_list}), 200

    def get_user(self, user_id):
        """
        get the user by user_id
        :param user_id:
        :return:
        """
        user = user_model.User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"id": user.id, "username": user.username, "email": user.email}), 200

    def update_user(self, user_id):
        """
        curl -X PUT http://127.0.0.1:5000/user/1 \
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
        user = user_model.User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.password = data.get("password", user.password)
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200

    def delete_user(self, user_id):
        """
        curl -X DELETE http://127.0.0.1:5000/user/1
        :param user_id:
        :return:
        """
        user = user_model.User.query.get(user_id)
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
