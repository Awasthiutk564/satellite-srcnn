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


def _ensure_directories() -> None:
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    ENHANCED_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_image_bytes(
    user_id: str,
    original_filename: str | None,
    data: bytes,
) -> Tuple[str, int, int, str]:
    \"\"\"Save an uploaded image to disk and return metadata.

    Returns a tuple of:
    (relative_storage_path, width, height, original_filename)
    \"\"\"

    _ensure_directories()

    safe_name = original_filename or \"upload.png\"
    suffix = Path(safe_name).suffix or \".png\"
    filename = f\"{user_id}_{uuid.uuid4().hex}{suffix}\"

    rel_path = Path(\"original\") / filename
    abs_path = ORIGINAL_DIR / filename

    # Write raw bytes to disk
    with abs_path.open(\"wb\") as f:
        f.write(data)

    # Decode image to get dimensions (grayscale is fine for SRCNN)
    np_data = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_GRAYSCALE)
    if img is None:
        # Fallback: try reading back from disk
        img = cv2.imread(str(abs_path), cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError(\"Uploaded file is not a valid image.\")

    height, width = img.shape[:2]

    return str(rel_path).replace(\"\\\\\", \"/\"), width, height, safe_name


def get_absolute_path(relative_path: str) -> Path:
    \"\"\"Resolve a stored relative path to an absolute file system path.\"\"\"
    return STORAGE_ROOT / Path(relative_path)


def build_enhanced_output_path(image_id: str, model_type: str, scale_factor: int) -> tuple[str, Path]:
    \"\"\"Generate a relative and absolute path for an enhanced image output.\"\"\"
    _ensure_directories()
    filename = f\"{image_id}_{model_type}_x{scale_factor}.png\"
    rel_path = Path(\"enhanced\") / filename
    abs_path = ENHANCED_DIR / filename
    return str(rel_path).replace(\"\\\\\", \"/\"), abs_path

