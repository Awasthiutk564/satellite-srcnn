import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    original_filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)

    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)

    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User", back_populates="images")
    results = relationship(
        "Result",
        back_populates="image",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

