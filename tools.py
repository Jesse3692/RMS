from functools import wraps

from flask import g, jsonify
from flask_jwt_extended import get_jwt_identity

from models.users import User


def role_required(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.get(current_user)
            roles = [role.name for role in user.roles]
            if role_name not in roles:
                return jsonify(message="Insufficient permissions"), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def check_permission(permission_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查用户是否有权限
            user_permissions = [p.name for p in g.current_user.permissions]
            if permission_name not in user_permissions:
                return jsonify({"error": "Permission denied"}), 403
            return func(*args, **kwargs)

        return wrapper

    return decorator


# @app.route("/admin", methods=["GET"])
# @jwt_required()
# @role_required("admin")
# def admin_area():
#     return jsonify(message="Welcome Admin!"), 200
