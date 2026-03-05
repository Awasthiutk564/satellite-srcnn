from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]

from app.core.dependencies import get_current_user
from app.db.models.image import Image
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.image import ImageDetail, ImageRead
from app.utils.file_storage import save_uploaded_image_bytes


router = APIRouter()


@router.post("/upload", response_model=ImageRead, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ImageRead:
    data = await file.read()
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
    return ImageRead.model_validate(image)


@router.get("/", response_model=List[ImageRead])
def list_images(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[ImageRead]:
    query = (
        db.query(Image)
        .filter(Image.user_id == current_user.id, Image.deleted.is_(False))
        .order_by(Image.uploaded_at.desc())
        .offset(skip)
        .limit(limit)
    )
    images = query.all()
    return [ImageRead.model_validate(img) for img in images]


@router.get("/{image_id}", response_model=ImageDetail)
def get_image_detail(
    image_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ImageDetail:
    image = (
        db.query(Image)
        .filter(Image.id == image_id, Image.user_id == current_user.id)
        .first()
    )
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    # Eager load results for this image
    _ = image.results  # access to ensure relationship is populated
    return ImageDetail.model_validate(image)

