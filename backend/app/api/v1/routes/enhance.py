from __future__ import annotations

from typing import Literal

import cv2
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.models.image import Image
from app.db.models.result import Result
from app.db.models.user import User
from app.db.session import get_db
from app.ml.inference import run_super_resolution
from app.schemas.result import ResultRead
from app.utils.file_storage import (
    build_enhanced_output_path,
    get_absolute_path,
)


router = APIRouter()


class EnhanceRequest(BaseModel):
    image_id: str
    model_type: Literal["bicubic", "srcnn"] = Field(
        description="Super-resolution model to use."
    )
    scale_factor: int = Field(2, ge=2, le=4)


class EnhanceResponse(BaseModel):
    result: ResultRead
    original_image_url: str
    enhanced_image_url: str


@router.post("/", response_model=EnhanceResponse)
def enhance_image(
    payload: EnhanceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EnhanceResponse:
    image = (
        db.query(Image)
        .filter(Image.id == payload.image_id, Image.user_id == current_user.id)
        .first()
    )
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    hr_path = get_absolute_path(image.storage_path)
    if not hr_path.exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stored image file is missing on the server.",
        )

    try:
        output_img, metrics, elapsed_ms = run_super_resolution(
            hr_path=hr_path,
            model_type=payload.model_type,
            scale_factor=payload.scale_factor,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    rel_output_path, abs_output_path = build_enhanced_output_path(
        image_id=str(image.id),
        model_type=payload.model_type,
        scale_factor=payload.scale_factor,
    )

    # Save enhanced image
    success = cv2.imwrite(str(abs_output_path), output_img)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to write enhanced image to disk.",
        )

    # Persist result row
    result = Result(
        image_id=image.id,
        model_type=payload.model_type,
        scale_factor=payload.scale_factor,
        output_path=rel_output_path,
        psnr=metrics["psnr"],
        ssim=metrics["ssim"],
        mse=metrics["mse"],
        processing_time_ms=elapsed_ms,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    # Build URLs for frontend consumption; the frontend can prepend the API base URL.
    original_url = f"/files/{image.storage_path}"
    enhanced_url = f"/files/{rel_output_path}"

    return EnhanceResponse(
        result=ResultRead.model_validate(result),
        original_image_url=original_url,
        enhanced_image_url=enhanced_url,
    )

