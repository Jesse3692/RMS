from sqlalchemy.orm import relationship

from models import db


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = relationship("Permission", secondary="role_permissions")

    # 定义反向关系
    users = db.relationship("User", secondary="user_roles", back_populates="roles")  # noqa:E501


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)  # noqa:E501
