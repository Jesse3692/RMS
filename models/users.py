from datetime import datetime, timezone
from . import db
from config.config import bcrypt
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # 关系
    password = db.relationship("UserPassword", backref="user", uselist=False)
    user_info = db.relationship("UserInfo", backref="user", lazy="dynamic")
    login_info = db.relationship("UserLoginInfo", backref="user", uselist=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        if not self.password:
            self.password = UserPassword(user_id=self.id)
        self.password.password_hash = bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

        # 更新密码修改时间
        if self.login_info:
            self.login_info.last_password_change_time = datetime.now(timezone.utc)
            if not self.login_info.has_changed_initial_password:
                self.login_info.has_changed_initial_password = True

    def check_password(self, password):
        if self.password:
            return bcrypt.check_password_hash(self.password.password_hash, password)
        return False

    def record_login(self):
        """记录用户登录信息"""
        if not self.login_info:
            self.login_info = UserLoginInfo(user_id=self.id)

        self.login_info.last_login_time = lambda: datetime.now(timezone.utc)()
        self.login_info.login_count = (self.login_info.login_count or 0) + 1
        self.login_info.is_new_user = False


class UserLoginInfo(db.Model):
    __tablename__ = "user_login_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    register_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    login_count = db.Column(db.Integer, default=0)
    last_login_time = db.Column(db.DateTime)
    is_new_user = db.Column(db.Boolean, default=True)
    has_changed_initial_password = db.Column(db.Boolean, default=False)
    last_password_change_time = db.Column(db.DateTime)

    def __repr__(self):
        return f"<UserLoginInfo {self.user_id}>"


class UserField(db.Model):
    __tablename__ = "user_fields"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_required = db.Column(db.Boolean, default=False)

    # 关系
    user_info = db.relationship("UserInfo", backref="field", lazy="dynamic")

    def __repr__(self):
        return f"<UserField {self.name}>"


class UserInfo(db.Model):
    __tablename__ = "user_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey("user_fields.id"), nullable=False)
    value = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<UserInfo {self.user_id}:{self.field_id}>"


class UserPassword(db.Model):
    __tablename__ = "user_passwords"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<UserPassword {self.user_id}>"


def init_user_fields():
    attributes = [
        {"name": "first_name", "description": "名", "is_required": True},
        {"name": "last_name", "description": "姓", "is_required": True},
        {"name": "gender", "description": "性别", "is_required": True},
        {"name": "phone_number", "description": "电话号码", "is_required": True},
        {"name": "id_number", "description": "身份证号码", "is_required": True},
        {"name": "photo", "description": "照片", "is_required": False},
    ]

    for attr in attributes:
        if not UserField.query.filter_by(name=attr["name"]).first():
            new_attr = UserField(
                name=attr["name"],
                description=attr["description"],
                is_required=attr["is_required"],
            )
            db.session.add(new_attr)

    db.session.commit()


def init_user_tables():
    # """初始化用户相关的所有表"""
    db.create_all()
    init_user_fields()
