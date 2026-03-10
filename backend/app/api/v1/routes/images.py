from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.models.image import Image
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.image import ImageDetail, ImageRead


router = APIRouter()


@router.get("/", response_model=List[ImageRead])
def read_images(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[ImageRead]:
    images = (
        db.query(Image)
        .filter(Image.user_id == current_user.id, Image.deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [ImageRead.model_validate(img) for img in images]


@router.get("/{image_id}", response_model=ImageDetail)
def read_image(
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
    return ImageDetail.model_validate(image)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(
    image_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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
    image.deleted = True
    db.commit()
    return None
