from flask import Blueprint, current_app, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from .models import validate_user

# 初始化蓝图
auth_blueprint = Blueprint("auth", __name__)

bcrypt = Bcrypt()


@auth_blueprint.route("/login", methods=["POST"])
def login():
    """
    登录

    POST /login

    Parameters:
        username - String - 用户名
        password - String - 密码

    Returns:
        200 - {"message": "Login successful", "access_token": "jwt-token"}
        401 - {"message": "Invalid username or password"}
    """

    username = request.json.get("username")
    password = request.json.get("password")

    if user := validate_user(username, password):
        # TODO 添加session
        # 生成JWT token
        access_token = create_access_token(identity=user.id)
        # 保存到redis中
        # 从当前应用配置中获取 redis_client
        redis_client = current_app.config["redis_client"]
        redis_client.setex(f"access_token:{user.id}", 3600, access_token)
        return jsonify(message="Login successful", access_token=access_token), 200
    else:
        return jsonify(message="Invalid username or password"), 401


@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """
    刷新JWT访问令牌。

    POST /refresh

    此端点要求请求携带有效的刷新令牌，以便生成新的访问令牌。

    Returns:
        200 - {"access_token": "新的JWT访问令牌"}
    """
    current_user = get_jwt_identity()
    refresh_token = create_refresh_token(identity=current_user)
    # 保存到redis中
    redis_client = current_app.config["redis_client"]
    redis_client.setex(f"access_token:{current_user}", 3600, refresh_token)
    return jsonify(access_token=refresh_token), 200


@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    # TODO 删除 session
    response = jsonify(message="Logout successful")
    # TODO 清除JWT token
    # response.set_cookie("access_token", "", expires=0)

    return response
