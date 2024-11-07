from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Position(db.Model):
    __tablename__ = "positions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)  # noqa:E501
    department = relationship("Department", back_populates="positions")
    users = relationship("User", back_populates="positions", secondary="user_positions")  # noqa:E501

    def __repr__(self):
        return f"<Position(name='{self.name}', department_id='{self.department_id}')>"  # noqa:E501
