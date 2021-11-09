import inspect
from functools import lru_cache

from app.db.utils import UtcNow
from sqlalchemy import Column, DateTime, Table
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import InstrumentedAttribute


@as_declarative()
class Base:
    __table__: Table

    created: str = Column(
        "Created", DateTime(), nullable=False, server_default=UtcNow()
    )
    updated: str = Column(
        "Updated",
        DateTime(),
        nullable=False,
        server_default=UtcNow(),
        onupdate=UtcNow(),
    )

    @classmethod
    @lru_cache(maxsize=None)
    def primary_key_name(cls) -> str:
        """Gets the name of the column with the primary key.

        Source: https://stackoverflow.com/a/44960684
        """
        primary_key_name = cls.__table__.primary_key.columns.values()[0].name
        for key, value in cls.__dict__.items():
            if (
                isinstance(value, InstrumentedAttribute)
                and value.name == primary_key_name
            ):
                return key
        raise RuntimeError("No primary key found!")
