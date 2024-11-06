from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Permission(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class RolePermissions(db.Model):
    __tablename__ = "role_permissions"
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    )
