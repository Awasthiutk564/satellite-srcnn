import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
from app.ml.metrics import calculate_mse, calculate_psnr, calculate_ssim

def run_bicubic_super_resolution(hr_path: Path, scale_factor: int) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Run bicubic interpolation super-resolution.
    1. Load HR image
    2. Downsample to LR
    3. Upsample back to HR size using bicubic interpolation
    4. Calculate metrics
    """
    hr_img = cv2.imread(str(hr_path), cv2.IMREAD_GRAYSCALE)
    if hr_img is None:
        raise ValueError(f"Could not read image from {hr_path}")
    
    h, w = hr_img.shape[:2]
    
    # Simulate LR by downsampling
    lr_small = cv2.resize(
        hr_img,
        (w // scale_factor, h // scale_factor),
        interpolation=cv2.INTER_CUBIC,
    )
    
    # Upscale back to HR size
    bicubic_up = cv2.resize(
        lr_small,
        (w, h),
        interpolation=cv2.INTER_CUBIC,
    )
    
    metrics = {
        "psnr": calculate_psnr(hr_img, bicubic_up),
        "mse": calculate_mse(hr_img, bicubic_up),
        "ssim": calculate_ssim(hr_img, bicubic_up),
    }
    
    return bicubic_up, metrics
