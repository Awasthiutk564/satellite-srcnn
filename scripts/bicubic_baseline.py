# =============================================================
# PHASE 3 — Bicubic Interpolation Baseline
# Kya karta hai yeh script:
# 1. LR patches load karta hai
# 2. Bicubic interpolation se upscale karta hai
# 3. HR patches se compare karta hai
# 4. PSNR, SSIM, MSE calculate karta hai
# 5. Results save karta hai
# =============================================================

import os
import cv2
import numpy as np
import pandas as pd
from skimage.metrics import structural_similarity as ssim

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIGH_RES_DIR = os.path.join(BASE_DIR, "data", "processed", "high_res")
LOW_RES_DIR  = os.path.join(BASE_DIR, "data", "processed", "low_res")
RESULTS_DIR  = os.path.join(BASE_DIR, "results", "metrics")

# ── Metrics Functions ─────────────────────────────────────────

def calculate_psnr(original, compressed):
    # PSNR = Peak Signal to Noise Ratio
    # Jitna zyada PSNR, utni achhi quality
    mse = np.mean((original.astype(np.float32) - compressed.astype(np.float32)) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

def calculate_mse(original, compressed):
    # MSE = Mean Squared Error
    # Jitna kam MSE, utni achhi quality
    return np.mean((original.astype(np.float32) - compressed.astype(np.float32)) ** 2)

def calculate_ssim(original, compressed):
    # SSIM = Structural Similarity Index
    # 1 ke kareeb = perfect similarity
    return ssim(original, compressed, data_range=255)

# ── Main Function ─────────────────────────────────────────────

def run_bicubic_baseline():
    print("Bicubic Baseline shuru ho raha hai...\n")

    results = []
    files   = sorted(os.listdir(HIGH_RES_DIR))
    total   = len(files)

    for i, filename in enumerate(files):
        # HR aur LR images load karo
        hr_path = os.path.join(HIGH_RES_DIR, filename)
        lr_path = os.path.join(LOW_RES_DIR,  filename)

        hr_img  = cv2.imread(hr_path, cv2.IMREAD_GRAYSCALE)
        lr_img  = cv2.imread(lr_path, cv2.IMREAD_GRAYSCALE)

        if hr_img is None or lr_img is None:
            continue

        # Bicubic upscale karo — LR ko HR size tak bado
        h, w        = hr_img.shape
        bicubic_img = cv2.resize(lr_img, (w, h), interpolation=cv2.INTER_CUBIC)

        # Metrics calculate karo
        psnr_val = calculate_psnr(hr_img, bicubic_img)
        mse_val  = calculate_mse(hr_img,  bicubic_img)
        ssim_val = calculate_ssim(hr_img, bicubic_img)

        results.append({
            "filename" : filename,
            "PSNR"     : round(psnr_val, 4),
            "MSE"      : round(mse_val,  4),
            "SSIM"     : round(ssim_val, 4)
        })

        # Har 500 images pe progress dikhao
        if (i + 1) % 500 == 0:
            print(f"  Progress: {i+1}/{total} images done...")

    # Results ko CSV mein save karo
    df          = pd.DataFrame(results)
    output_path = os.path.join(RESULTS_DIR, "bicubic_results.csv")
    df.to_csv(output_path, index=False)

    # Average metrics print karo
    print(f"\n🎉 Bicubic Baseline Complete!")
    print(f"   Total images evaluated : {len(results)}")
    print(f"   Average PSNR           : {df['PSNR'].mean():.4f} dB")
    print(f"   Average MSE            : {df['MSE'].mean():.4f}")
    print(f"   Average SSIM           : {df['SSIM'].mean():.4f}")
    print(f"\n   Results saved in       : {output_path}")

# ── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    run_bicubic_baseline()