import numpy as np
from skimage.metrics import structural_similarity as ssim

def calculate_psnr(original: np.ndarray, compressed: np.ndarray) -> float:
    mse = np.mean((original.astype(np.float32) - compressed.astype(np.float32)) ** 2)
    if mse == 0:
        return 100.0
    return float(20 * np.log10(255.0 / np.sqrt(mse)))

def calculate_mse(original: np.ndarray, compressed: np.ndarray) -> float:
    return float(np.mean((original.astype(np.float32) - compressed.astype(np.float32)) ** 2))

def calculate_ssim(original: np.ndarray, compressed: np.ndarray) -> float:
    return float(ssim(original, compressed, data_range=255))
