import os
from datetime import timedelta


class JWTConfig:
    # JWT 密钥，用于签名令牌
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "your-jwt-secret-key-here"

    # 令牌过期时间，设置为 1 小时
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # 刷新令牌过期时间，设置为 30 天
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # 令牌位置，可以是 'headers', 'cookies', 'json', 'query_string'
    JWT_TOKEN_LOCATION = ["headers"]

    # 在 headers 中的令牌前缀
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    # 是否允许刷新令牌
    JWT_REFRESH_TOKEN_ENABLED = True

    # 是否在响应中包含 JWT 声明
    JWT_CLAIMS_IN_REFRESH_TOKEN = True

    # 黑名单启用
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
