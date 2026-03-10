from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[2]
STORAGE_ROOT = BASE_DIR / "storage"
ORIGINAL_DIR = STORAGE_ROOT / "original"
ENHANCED_DIR = STORAGE_ROOT / "enhanced"


def _ensure_directories():
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    ENHANCED_DIR.mkdir(parents=True, exist_ok=True)


def get_absolute_path(relative_path: str) -> Path:
    return STORAGE_ROOT / relative_path


def save_uploaded_image_bytes(
    user_id: str,
    original_filename: str,
    data: bytes,
) -> Tuple[str, int, int, str]:
    _ensure_directories()
    
    unique_id = uuid.uuid4().hex
    ext = os.path.splitext(original_filename)[1]
    if not ext:
        ext = ".png"
    
    filename = f"{user_id}_{unique_id}{ext}"
    relative_path = os.path.join("original", filename)
    absolute_path = ORIGINAL_DIR / filename
    
    with open(absolute_path, "wb") as f:
        f.write(data)
    
    img = cv2.imread(str(absolute_path))
    if img is None:
        os.remove(absolute_path)
        raise ValueError("Invalid image file uploaded.")
    
    height, width = img.shape[:2]
    # Normalize path for DB (use forward slashes)
    db_relative_path = relative_path.replace("\\", "/")
    
    return db_relative_path, width, height, original_filename


def build_enhanced_output_path(
    image_id: str,
    model_type: str,
    scale_factor: int,
) -> Tuple[str, Path]:
    _ensure_directories()
    
    filename = f"enhanced_{image_id}_{model_type}_x{scale_factor}.png"
    relative_path = os.path.join("enhanced", filename)
    absolute_path = ENHANCED_DIR / filename
    
    # Normalize path for DB
    db_relative_path = relative_path.replace("\\", "/")
    
    return db_relative_path, absolute_path
