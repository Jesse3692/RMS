from sqlalchemy.orm import relationship

from models import db
from datetime import datetime, timezone


class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    users = relationship(
        "User", back_populates="departments", secondary="user_departments"
    )
    positions = relationship("Position", back_populates="departments")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # noqa:E501
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Department(name='{self.name}')>"
