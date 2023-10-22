from datetime import datetime
import uuid

from pydantic import BaseModel


class Category(BaseModel):
    category_uid: uuid.UUID
    title: str
    

    @staticmethod
    def next_id():
        return uuid.uuid4()
