from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

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


@app.route("/admin", methods=["GET"])
@jwt_required()
@role_required("admin")
def admin_area():
    return jsonify(message="Welcome Admin!"), 200
