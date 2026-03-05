from __future__ import annotations

import numpy as np
from skimage.metrics import structural_similarity as ssim


def calculate_mse(original: np.ndarray, predicted: np.ndarray) -> float:
    original_f = original.astype(np.float32)
    predicted_f = predicted.astype(np.float32)
    return float(np.mean((original_f - predicted_f) ** 2))


def calculate_psnr(original: np.ndarray, predicted: np.ndarray) -> float:
    mse = calculate_mse(original, predicted)
    if mse == 0:
        return 100.0
    max_pixel = 255.0
    return float(20 * np.log10(max_pixel / np.sqrt(mse)))


def calculate_ssim(original: np.ndarray, predicted: np.ndarray) -> float:
    return float(ssim(original, predicted, data_range=255))

