import cv2
import numpy as np

def run_bicubic_interpolation(img_path: str, scale_factor: int) -> np.ndarray:
    img = cv2.imread(str(img_path))
    if img is None:
        raise ValueError(f"Could not read image at {img_path}")
    
    h, w = img.shape[:2]
    # Downsample to create LR
    lr_size = (w // scale_factor, h // scale_factor)
    if lr_size[0] < 1 or lr_size[1] < 1:
        raise ValueError("Image too small for this scale factor.")
        
    lr = cv2.resize(img, lr_size, interpolation=cv2.INTER_CUBIC)
    # Upsample back
    hr_bicubic = cv2.resize(lr, (w, h), interpolation=cv2.INTER_CUBIC)
    return hr_bicubic
