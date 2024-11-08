from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models import db


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = relationship("Permission", secondary="role_permissions")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # noqa:E501
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # 定义反向关系
    users = db.relationship("User", secondary="user_roles", back_populates="roles")  # noqa:E501
