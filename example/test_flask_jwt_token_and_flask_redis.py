from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask_redis import FlaskRedis

app = Flask(__name__)

# 配置 Redis
app.config["REDIS_URL"] = "redis://:qweasd123@localhost:63799/0"
redis_client = FlaskRedis(app)

# 配置 JWT
app.config["JWT_SECRET_KEY"] = "your-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    hours=2
)  # 设置 token 过期时间为两小时

jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    # 这里应该包含验证用户凭证的逻辑
    username = request.json.get("username")
    password = request.json.get("password")
    # 假设用户验证成功
    access_token = create_access_token(identity=username)
    # 将 token 存储到 Redis 中，并设置过期时间
    redis_client.setex(username, 7200, access_token)
    return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    # 从 Redis 中获取 token
    token = redis_client.get(current_user)
    if token:
        # 刷新令牌
        access_token = create_access_token(identity=current_user)
        # 将 token 存储到 Redis 中，并设置过期时间
        redis_client.setex(current_user, 7200, access_token)
        return jsonify(logged_in_as=current_user)
    else:
        return jsonify(error="Token has been revoked or expired"), 401


if __name__ == "__main__":
    app.run(debug=True)
