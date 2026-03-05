from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ResultRead(BaseModel):
    id: str
    image_id: str
    model_type: str
    scale_factor: int
    output_path: str
    psnr: float
    ssim: float
    mse: float
    created_at: datetime
    processing_time_ms: Optional[int] = None

    class Config:
        from_attributes = True

