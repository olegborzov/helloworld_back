# This Python file uses the following encoding: utf-8

"""
User models
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from models.common import TimestampMixin, BulkMixin, BaseModel
from core.registry import db

__all__ = ["User"]


class User(BaseModel, TimestampMixin, UserMixin, BulkMixin):
    __tablename__ = "user"
    __repr_attrs__ = ["email", "is_admin", "active"]
    conflict_index = ["email"]

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, nullable=False, default=False, server_default="f")
    active = db.Column(db.Boolean, nullable=False, default=True, server_default="t")

    @classmethod
    def get_by_email(cls, email: str) -> "User":
        return db.session.query(cls).filter_by(email=email).first()

    @classmethod
    def create(cls, email: str, password: str) -> "User":
        new_user = cls(email=email)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @property
    def password(self):
        raise AttributeError("Can't read")

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
