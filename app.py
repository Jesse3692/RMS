from flask import Flask

from api.v1.auth.auth import auth_blueprint
from api.v1.departments import departments_blueprint
from api.v1.roles import roles_blueprint
from api.v1.users import users_blueprint
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

    # 注册蓝图
    register_blueprint(app)

    # 初始化扩展
    init_extensions(app)

    with app.app_context():
        db.create_all()
        # init_positions_table()
        # init_user_roles()
        # init_customer_table()
        init_user_tables()
        init_log_tables()  # 添加这行

    return app


def register_blueprint(app):
    """
    Register blueprints to the Flask app.

    :param app: The Flask app
    """
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(departments_blueprint)
    app.register_blueprint(roles_blueprint)


def init_extensions(app):
    """
    Initializes all extensions used by the app.

    :param app: The Flask app
    """
    # 初始化扩展
    jsonrpc.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    redis_client.init_app(app)

    # 注册扩展为全局对象
    app.jsonrpc = jsonrpc
    app.jwt = jwt
    app.login_manager = login_manager
    app.bcrypt = bcrypt
    app.redis_client = redis_client


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
