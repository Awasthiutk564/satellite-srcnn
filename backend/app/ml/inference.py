from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, Literal, Tuple

import cv2
import numpy as np
import torch

from app.ml.bicubic import run_bicubic_super_resolution
from app.ml.metrics import calculate_mse, calculate_psnr, calculate_ssim
from app.ml.srcnn_model import get_srcnn_model


ModelType = Literal["bicubic", "srcnn"]


def _load_hr_image(path: Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not read image from {path}")
    return img


def run_super_resolution(
    hr_path: Path,
    model_type: ModelType,
    scale_factor: int,
) -> Tuple[np.ndarray, Dict[str, float], int]:
    """Run bicubic or SRCNN super-resolution and return the output + metrics.

    Returns:
        (output_image_uint8, metrics_dict, processing_time_ms)
    """

    start = time.perf_counter()

    if model_type == "bicubic":
        output_img, metrics = run_bicubic_super_resolution(hr_path, scale_factor)
    else:
        # For SRCNN, first create a bicubic-upsampled image that matches HR size,
        # then feed it through the CNN and compute metrics against the original HR.
        hr_img = _load_hr_image(hr_path)
        h, w = hr_img.shape[:2]
        if h < scale_factor or w < scale_factor:
            raise ValueError("Image is too small for the requested scale factor.")

        lr_small = cv2.resize(
            hr_img,
            (w // scale_factor, h // scale_factor),
            interpolation=cv2.INTER_CUBIC,
        )
        bicubic_up = cv2.resize(
            lr_small,
            (w, h),
            interpolation=cv2.INTER_CUBIC,
        )

        model, device = get_srcnn_model()

        # Prepare tensor
        inp = bicubic_up.astype(np.float32) / 255.0
        inp_tensor = torch.from_numpy(inp).unsqueeze(0).unsqueeze(0).to(device)

        with torch.no_grad():
            sr_tensor = model(inp_tensor)

        sr_img = sr_tensor.squeeze().cpu().numpy()
        sr_img = np.clip(sr_img * 255.0, 0, 255).astype(np.uint8)

        metrics = {
            "psnr": calculate_psnr(hr_img, sr_img),
            "mse": calculate_mse(hr_img, sr_img),
            "ssim": calculate_ssim(hr_img, sr_img),
        }

        output_img = sr_img

    elapsed_ms = int((time.perf_counter() - start) * 1000)
    return output_img, metrics, elapsed_ms

