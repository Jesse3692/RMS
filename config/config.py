from flask_jsonrpc import JSONRPC
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# JSON-RPC
jsonrpc = JSONRPC(service_url="/", enable_web_browsable_api=False)

# JWT
jwt = JWTManager()

# Login Manager
login_manager = LoginManager()

# Bcrypt
bcrypt = Bcrypt()

# @login_manager.user_loader
# def load_user(user_id):
#     from models.user import User
#     return User.query.get(int(user_id))
