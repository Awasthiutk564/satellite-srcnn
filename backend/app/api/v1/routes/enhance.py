from __future__ import annotations

from typing import Literal, Optional

import cv2
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
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
    save_uploaded_image_bytes,
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

    # Build URLs for frontend consumption
    original_url = f"/files/{image.storage_path}"
    enhanced_url = f"/files/{rel_output_path}"

    return EnhanceResponse(
        result=ResultRead.model_validate(result),
        original_image_url=original_url,
        enhanced_image_url=enhanced_url,
    )


@router.post("/upload", response_model=EnhanceResponse)
async def enhance_uploaded_image(
    file: UploadFile = File(...),
    model_type: str = Form("srcnn"),
    scale_factor: int = Form(2),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EnhanceResponse:
    """Upload an image and enhance it in one step."""
    if scale_factor < 2 or scale_factor > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scale factor must be between 2 and 4.",
        )
    if model_type not in ("bicubic", "srcnn"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="model_type must be 'bicubic' or 'srcnn'.",
        )

    data = await file.read()

    # Save the uploaded image
    try:
        rel_path, width, height, original_name = save_uploaded_image_bytes(
            user_id=str(current_user.id),
            original_filename=file.filename,
            data=data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Create image record
    image = Image(
        user_id=current_user.id,
        original_filename=original_name,
        storage_path=rel_path,
        width=width,
        height=height,
    )
    db.add(image)
    db.commit()
    db.refresh(image)

    # Run super-resolution
    hr_path = get_absolute_path(image.storage_path)
    try:
        output_img, metrics, elapsed_ms = run_super_resolution(
            hr_path=hr_path,
            model_type=model_type,
            scale_factor=scale_factor,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    rel_output_path, abs_output_path = build_enhanced_output_path(
        image_id=str(image.id),
        model_type=model_type,
        scale_factor=scale_factor,
    )

    success = cv2.imwrite(str(abs_output_path), output_img)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to write enhanced image to disk.",
        )

    result = Result(
        image_id=image.id,
        model_type=model_type,
        scale_factor=scale_factor,
        output_path=rel_output_path,
        psnr=metrics["psnr"],
        ssim=metrics["ssim"],
        mse=metrics["mse"],
        processing_time_ms=elapsed_ms,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    original_url = f"/files/{image.storage_path}"
    enhanced_url = f"/files/{rel_output_path}"

    return EnhanceResponse(
        result=ResultRead.model_validate(result),
        original_image_url=original_url,
        enhanced_image_url=enhanced_url,
    )
