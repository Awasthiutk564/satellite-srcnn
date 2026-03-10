from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.result import ResultRead


class ImageRead(BaseModel):
    id: UUID
    original_filename: str
    storage_path: str
    width: int
    height: int
    uploaded_at: datetime
    deleted: bool

    class Config:
        from_attributes = True


class ImageDetail(ImageRead):
    results: List[ResultRead] = []

