from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.db.base_class import Base
from app.schemas.resource_created import ResourceCreated
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ResourceCreated:
        resource_created = ResourceCreated()
        obj_in_data = obj_in.dict()
        obj_in_data[self.model.primary_key_name()] = resource_created.identifier

        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        return resource_created
