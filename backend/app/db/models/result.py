import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    image_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    model_type = Column(String, nullable=False)  # e.g. "bicubic" or "srcnn"
    scale_factor = Column(Integer, nullable=False)

    output_path = Column(String, nullable=False)

    psnr = Column(Float, nullable=False)
    ssim = Column(Float, nullable=False)
    mse = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processing_time_ms = Column(Integer, nullable=True)

    # Relationships
    image = relationship("Image", back_populates="results")

