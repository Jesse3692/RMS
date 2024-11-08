from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from models import db


class Position(db.Model):
    __tablename__ = "positions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    department_id = db.Column(
        db.Integer, db.ForeignKey("departments.id"), nullable=False
    )  # noqa:E501
    departments = relationship("Department", back_populates="positions")
    users = relationship("User", back_populates="positions", secondary="user_positions")  # noqa:E501
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # noqa:E501
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Position(name='{self.name}', department_id='{self.department_id}')>"  # noqa:E501
