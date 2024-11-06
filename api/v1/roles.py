from flask import jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import Department, Role, User, db


@app.route("/roles", methods=["POST"])
@jwt_required()
def create_role():
    role_name = request.json.get("name")

    # 检查是否已经存在角色
    existing_role = Role.query.filter_by(name=role_name).first()
    if existing_role:
        return jsonify(message="Role already exists"), 400

    # 创建角色
    new_role = Role(name=role_name)
    db.session.add(new_role)
    db.session.commit()

    return jsonify(message="Role created successfully", role_id=new_role.id), 201


@app.route("/roles/<int:role_id>", methods=["PUT"])
@jwt_required()
def edit_role(role_id):
    role = Role.query.get_or_404(role_id)
    role_name = request.json.get("name", role.name)
    role.name = role_name
    db.session.commit()
    return jsonify(message="Role updated successfully"), 200


@app.route("/roles/<int:role_id>", methods=["DELETE"])
@jwt_required()
def delete_role(role_id):
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return jsonify(message="Role deleted successfully"), 200


@app.route("/roles/<int:role_id>/assign", methods=["POST"])
@jwt_required()
def assign_role_to_user(role_id):
    user_id = request.json.get("user_id")
    user = User.query.get_or_404(user_id)
    role = Role.query.get_or_404(role_id)

    # 将角色分配给用户
    user.roles.append(role)
    db.session.commit()

    return jsonify(message="Role assigned to user successfully"), 200


@app.route("/roles/<int:role_id>/permissions", methods=["POST"])
@jwt_required()
def assign_permissions_to_role(role_id):
    permission_ids = request.json.get("permission_ids", [])
    role = Role.query.get_or_404(role_id)

    for perm_id in permission_ids:
        permission = Permission.query.get(perm_id)
        if permission:
            role.permissions.append(permission)

    db.session.commit()
    return jsonify(message="Permissions assigned to role successfully"), 200
