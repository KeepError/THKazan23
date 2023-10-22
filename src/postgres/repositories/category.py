import uuid

from sqlalchemy.orm.session import Session

from src.schemas.category import Category
from ..models.category import CategoryModel, model_to_entity, entity_to_model


class CategoryRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session
    
    def get_by_uid(self, category_uid: uuid.UUID) -> Category | None:
        category_model = self.session.query(CategoryModel).filter(CategoryModel.category_uid == category_uid).first()
        if not category_model:
            return None
        return model_to_entity(category_model)

    def get_by_title(self, title: str) -> Category | None:
        category_model = self.session.query(CategoryModel).filter(CategoryModel.title == title).first()
        if not category_model:
            return None
        return model_to_entity(category_model)

    def get_list(self, offset: int, limit: int) -> list[Category]:
        category_models = (
            self.session.query(CategoryModel).offset(offset).limit(limit).all()
        )
        return list(map(model_to_entity, category_models))

    def add(self, category: Category) -> Category:
        category_model = entity_to_model(category)
        self.session.add(category_model)
        self.session.commit()
        return model_to_entity(category_model)

    def next_uid(self) -> uuid.UUID:
        return Category.next_id()
