from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    users = relationship("User", back_populates="department")
    positions = relationship("Position", back_populates="department")

    def __repr__(self) -> str:
        return f"<Department(name='{self.name}')>"
