from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import db
from models.position import Position
from models.role import Role
from models.users import User

# 初始化蓝图
users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/create", methods=["POST"])
# @jwt_required()
def create_user():
    # 获取当前用户身份，用于权限控制（例如创建用户需要管理员权限）
    # current_user = get_jwt_identity()
    # http://localhost:5000/api/v1/users/create /api/v1/users/create
    print(request.url, request.path)
    # 获取请求参数
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    role_ids = request.json.get("roles", [])  # 角色ID列表
    position_ids = request.json.get("positions", [])

    # 检查是否存在此用户名
    existing_user = User.query.filter_by(username=username, email=email).first()
    if existing_user:
        return jsonify(message="Username already exists"), 400

    # 密码加密
    password_hash = Bcrypt().generate_password_hash(password).decode("utf-8")

    # 创建用户对象
    new_user = User(username=username, email=email)

    # 设置密码
    new_user.set_password(password_hash)

    # 分配职位
    if position_ids:
        for position_id in position_ids:
            position = Position.query.get(position_id)
            if position:
                new_user.positions.users_blueprintend(position)

    # 分配角色
    for role_id in role_ids:
        role = Role.query.get(role_id)
        if role:
            new_user.roles.users_blueprintend(role)
    # 保存用户数据到数据库
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User created successfully", user_id=new_user.id), 201


@users_blueprint.route("", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_info = {
            "id": user.id,
            "username": user.username,
            "department": user.department.name if user.department else "N/A",
            "roles": [role.name for role in user.roles],
        }
        user_list.users_blueprintend(user_info)

    return jsonify(users=user_list), 200


@users_blueprint.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    username = request.json.get("username", user.username)
    password = request.json.get("password")
    department_id = request.json.get("department_id", user.department_id)
    roles = request.json.get("roles", [])

    # 更新用户名
    user.username = username

    # 更新密码（如果提供了）
    if password:
        user.password_hash = Bcrypt().generate_password_hash(password).decode("utf-8")

    # 更新部门
    user.department_id = department_id

    # 更新角色
    user.roles.clear()  # 清除当前角色
    for role_id in roles:
        role = Role.query.get(role_id)
        if role:
            user.roles.users_blueprintend(role)

    db.session.commit()

    return jsonify(message="User updated successfully"), 200


@users_blueprint.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="User deleted successfully"), 200


@users_blueprint.route("/<int:user_id>/toggle", methods=["PATCH"])
@jwt_required()
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active  # 切换用户的状态
    db.session.commit()
    return jsonify(message="User status updated"), 200
