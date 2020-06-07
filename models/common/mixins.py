# This Python file uses the following encoding: utf-8

"""
Mixin classes for models
"""

import logging
from datetime import datetime
from typing import Dict, List, Any

from sqlalchemy import func, inspect
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DatabaseError

from config import Config
from core.decorators import restartable
from core.registry import db


__all__ = ("TimestampMixin", "BulkMixin", "ReprMixin")


class TimestampMixin:
    """
    SQLAlchemy mixin, that adds "created" and "updated"
    datetime columns to models
    """
    created = db.Column(
        db.DateTime, default=datetime.now, server_default=func.now()
    )
    updated = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now,
        server_default=func.now(), server_onupdate=func.now()
    )


class BulkMixin:
    __table__: Any
    __tablename__: str

    @classmethod
    @restartable(exceptions=(DatabaseError,), callback=db.session.rollback)
    def get_last_modified(cls, since: datetime) -> Dict[str, int]:
        """
        Get rows, updated after "since" datetime
        Return Dict where key - unique field, value - id

        """
        if not (hasattr(cls, "conflict_index") and
                hasattr(cls, "id") and
                hasattr(cls, "updated")):
            return {}

        conflict_index = getattr(cls, "conflict_index")
        unique_field = getattr(cls, conflict_index[0])

        result = db.session.query(unique_field, cls.id).filter(
            cls.updated >= since
        ).all()
        db.session.commit()

        result = {row[0]: row[1] for row in result}
        return result

    @classmethod
    def save_bulk(cls, values: List[Dict], return_columns: list = None) -> List[dict]:
        """
        Bulk insert rows to DB by chunks.
        For each new and existed row set 'updated' column - update_time.

        Return 'updated' datetime

        """
        insert_stmt = cls._get_insert_stmt(update_time=func.now())
        if return_columns:
            insert_stmt = insert_stmt.returning(*return_columns)

        result = []
        step = Config.DB_CHUNK_SIZE
        for start in range(0, len(values), step):
            end = start + step
            rows = cls._insert_chunk(values[start:end], insert_stmt, return_values=bool(return_columns))
            if rows:
                result.extend(rows)
            logging.info("save_bulk inserted {} values to {}".format(
                end, cls.__tablename__
            ))

        return result

    @classmethod
    def _get_insert_stmt(cls, update_time: datetime):
        insert_stmt = insert(cls.__table__)
        unique_constraints = inspect(db.engine).get_unique_constraints(
            cls.__tablename__
        )
        if not hasattr(cls, "updated"):
            insert_stmt = insert_stmt.on_conflict_do_nothing()
        elif unique_constraints:
            insert_stmt = insert_stmt.on_conflict_do_update(
                constraint=unique_constraints[0]["name"],
                set_=dict(updated=update_time)
            )
        elif hasattr(cls, "conflict_index"):
            insert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=cls.conflict_index,
                set_=dict(updated=update_time)
            )

        return insert_stmt

    @classmethod
    @restartable(exceptions=(DatabaseError,), callback=db.session.rollback)
    def _insert_chunk(cls, chunk: List[Dict], insert_stmt, return_values: bool = False) -> List[dict]:
        result = []

        response = db.session.execute(insert_stmt.values(chunk))
        if return_values:
            result = response.fetchall()
            result = [dict(row) for row in result]

        db.session.commit()
        return result


class ReprMixin:
    """Beauty repr for SQLAlchemy objects"""
    __abstract__ = True

    __repr_attrs__ = []
    __repr_max_length__ = 25

    @property
    def _id_str(self):
        ids = inspect(self).identity
        if ids:
            return '-'.join([str(x) for x in ids]) if len(ids) > 1 \
                   else str(ids[0])
        else:
            return 'None'

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_length__

        values = []
        single = len(self.__repr_attrs__) == 1
        for key in self.__repr_attrs__:
            if not hasattr(self, key):
                raise KeyError("{} has incorrect attribute '{}' in "
                               "__repr__attrs__".format(self.__class__, key))
            value = getattr(self, key)
            wrap_in_quote = isinstance(value, str)

            value = str(value)
            if len(value) > max_length:
                value = value[:max_length] + '...'

            if wrap_in_quote:
                value = "'{}'".format(value)
            values.append(value if single else "{}:{}".format(key, value))

        return ' '.join(values)

    def __repr__(self):
        # get id like '#123'
        id_str = ('#' + self._id_str) if self._id_str else ''
        # join class name, id and repr_attrs
        return "<{} {}{}>".format(self.__class__.__name__, id_str,
                                  ' '+self._repr_attrs_str
                                  if self._repr_attrs_str else '')
