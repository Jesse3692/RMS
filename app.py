from flask import Flask

from config.config import bcrypt, jsonrpc, jwt, login_manager, redis_client
from config.database_config import DatabaseConfig
from config.jwt_config import JWTConfig

# from config.session_config import SessionConfig
from models import db, init_db
from models.log import init_log_tables
from models.users import init_user_tables


def create_app():
    app = Flask(__name__)
    app.config.from_object(DatabaseConfig)
    app.config.from_object(JWTConfig)
    # app.config.from_object(SessionConfig)

    # 初始化数据库
    init_db(app)

    # 初始化其他扩展
    jsonrpc.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    redis_client.init_app(app)

    with app.app_context():
        db.create_all()
        # init_positions_table()
        # init_user_roles()
        # init_customer_table()
        init_user_tables()
        init_log_tables()  # 添加这行

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
