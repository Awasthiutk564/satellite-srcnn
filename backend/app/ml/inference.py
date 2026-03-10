import time
import torch
import cv2
import numpy as np
from pathlib import Path

from app.ml.srcnn_model import load_pretrained_model
from app.utils.bicubic import run_bicubic_interpolation
from app.utils.metrics import calculate_psnr, calculate_ssim, calculate_mse

def run_super_resolution(hr_path: Path, model_type: str, scale_factor: int):
    hr_img = cv2.imread(str(hr_path))
    if hr_img is None:
        raise ValueError(f"Image not found at {hr_path}")

    start_time = time.time()
    
    if model_type == "bicubic":
        output_img = run_bicubic_interpolation(hr_path, scale_factor)
    else:
        # SRCNN inference
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = load_pretrained_model(device)
        
        # Prepare image (Y channel only or RGB? SRCNN usually Y)
        img_ycc = cv2.cvtColor(hr_img, cv2.COLOR_BGR2YCrCb)
        y, cb, cr = cv2.split(img_ycc)
        
        # Create LR
        h, w = y.shape
        lr_y = cv2.resize(y, (w // scale_factor, h // scale_factor), interpolation=cv2.INTER_CUBIC)
        # Bicubic upsample as input to SRCNN
        input_y = cv2.resize(lr_y, (w, h), interpolation=cv2.INTER_CUBIC)
        
        input_tensor = torch.from_numpy(input_y).view(1, 1, h, w).to(device).float() / 255.0
        
        with torch.no_grad():
            output_tensor = model(input_tensor).clamp(0.0, 1.0)
            
        output_y = (output_tensor.cpu().numpy()[0, 0] * 255.0).astype(np.uint8)
        
        # Merge back
        output_img = cv2.merge([output_y, cb, cr])
        output_img = cv2.cvtColor(output_img, cv2.COLOR_YCrCb2BGR)

    elapsed_ms = int((time.time() - start_time) * 1000)
    
    metrics = {
        "psnr": calculate_psnr(hr_img, output_img),
        "ssim": calculate_ssim(hr_img, output_img),
        "mse": calculate_mse(hr_img, output_img),
    }
    
    return output_img, metrics, elapsed_ms
