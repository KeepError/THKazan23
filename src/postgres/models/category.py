from datetime import datetime
import uuid

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from src.schemas.category import Category
from ..database import Base


class CategoryModel(Base):
    __tablename__ = "categories"
    category_uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )
    title: Mapped[str] = mapped_column(String(128), nullable=True)


def model_to_entity(model: CategoryModel) -> Category:
    return Category(
        category_uid=model.category_uid,
        title=model.title,
    )


def entity_to_model(entity: Category) -> CategoryModel:
    return CategoryModel(
        category_uid=entity.category_uid,
        title=entity.title,
    )
