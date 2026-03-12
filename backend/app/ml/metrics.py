import numpy as np
from skimage.metrics import structural_similarity as ssim

def calculate_psnr(original, compressed):
    """Calculate Peak Signal to Noise Ratio."""
    mse = np.mean((original.astype(np.float32) - compressed.astype(np.float32)) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

def calculate_mse(original, compressed):
    """Calculate Mean Squared Error."""
    return np.mean((original.astype(np.float32) - compressed.astype(np.float32)) ** 2)

def calculate_ssim(original, compressed):
    """Calculate Structural Similarity Index."""
    return ssim(original, compressed, data_range=255)
