# This Python file uses the following encoding: utf-8

"""
Base Model class for other models
"""

from typing import List, Optional

from dictalchemy import DictableModel
from sqlalchemy.exc import DatabaseError

from core.decorators import restartable
from core.registry import db
from models.common.mixins import ReprMixin


__all__ = ("BaseModel",)


class BaseModel(db.Model, DictableModel, ReprMixin):
    """Base model for all other models"""
    __abstract__ = True
    __repr__ = ReprMixin.__repr__

    @restartable(exceptions=(DatabaseError,), callback=db.session.rollback)
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    @restartable(exceptions=(DatabaseError,), callback=db.session.rollback)
    def save_all(cls, model_objects: List['BaseModel']):
        db.session.add_all(model_objects)
        db.session.commit()

    @classmethod
    @restartable(exceptions=(DatabaseError,), callback=db.session.rollback)
    def get_or_create(cls, **kwargs) -> 'BaseModel':
        instance = db.session.query(cls).filter_by(**kwargs).first()
        if instance is None:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()

        return instance

    @classmethod
    @restartable(exceptions=(DatabaseError,), callback=db.session.rollback)
    def get_or_none(cls, **kwargs) -> Optional['BaseModel']:
        return db.session.query(cls).filter_by(**kwargs).first()

    @classmethod
    @restartable(exceptions=(DatabaseError,), callback=db.session.rollback)
    def create(cls, **kwargs) -> 'BaseModel':
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()

        return instance

    @classmethod
    @restartable(exceptions=(DatabaseError,), callback=db.session.rollback)
    def select_by(cls, **kwargs) -> List['BaseModel']:
        return db.session.query(cls).filter_by(**kwargs).all()

    @classmethod
    @restartable(exceptions=(DatabaseError,), callback=db.session.rollback)
    def get_by(cls, **kwargs) -> 'BaseModel':
        return db.session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def get_by_id(cls, row_id: int, check_active: bool = True) -> "BaseModel":
        stmt = db.session.query(cls).filter(cls.id == row_id)
        if check_active and hasattr(cls, 'active'):
            stmt = stmt.filter(cls.active.is_(True))
        return stmt.first()

    @classmethod
    def get_by_ids(cls, row_ids: List[int], check_active: bool = True) -> List["BaseModel"]:
        stmt = db.session.query(cls).filter(cls.id.in_(row_ids))
        if check_active and hasattr(cls, 'active'):
            stmt = stmt.filter(cls.active.is_(True))
        return stmt.all()

