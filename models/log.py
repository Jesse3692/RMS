from models import db
from datetime import datetime, timezone


class LoginLog(db.Model):
    __tablename__ = "login_log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    login_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    ip_address = db.Column(db.String(45), nullable=True)
    computer_name = db.Column(db.String(255), nullable=True)

    user = db.relationship("User", backref=db.backref("login_logs", lazy="dynamic"))

    def __repr__(self):
        return f"<LoginLog {self.id} for user {self.user_id}>"


class OperationLog(db.Model):
    __tablename__ = "operation_logs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    operation = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<OperationLog {self.id} by {self.username}>"


def init_log_tables():
    db.create_all()
