# =============================================================
# PHASE 6 — Evaluation Script
# Kya karta hai:
# 1. Trained SRCNN model load karta hai
# 2. Test images pe run karta hai
# 3. PSNR, SSIM, MSE calculate karta hai
# 4. Bicubic se compare karta hai
# 5. Result table save karta hai
# =============================================================

import os
import sys
import cv2
import numpy as np
import pandas as pd
import torch
from skimage.metrics import structural_similarity as ssim

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.srcnn  import SRCNN

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIGH_RES_DIR = os.path.join(BASE_DIR, "data", "processed", "high_res")
LOW_RES_DIR  = os.path.join(BASE_DIR, "data", "processed", "low_res")
CHECKPOINT   = os.path.join(BASE_DIR, "checkpoints", "srcnn_best.pth")
RESULTS_DIR  = os.path.join(BASE_DIR, "results", "metrics")

# ── Device ────────────────────────────────────────────────────
DEVICE       = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Metrics Functions ─────────────────────────────────────────
def calculate_psnr(original, compressed):
    mse = np.mean((original.astype(np.float32) - compressed.astype(np.float32)) ** 2)
    if mse == 0:
        return 100
    return 20 * np.log10(255.0 / np.sqrt(mse))

def calculate_mse(original, compressed):
    return np.mean((original.astype(np.float32) - compressed.astype(np.float32)) ** 2)

def calculate_ssim(original, compressed):
    return ssim(original, compressed, data_range=255)

# ── Main Evaluation Function ──────────────────────────────────
def evaluate():
    print("Evaluation shuru ho raha hai...\n")

    # ── Model load karo ───────────────────────────────────────
    model = SRCNN().to(DEVICE)
    model.load_state_dict(torch.load(CHECKPOINT, map_location=DEVICE))
    model.eval()
    print(f"✅ Model loaded from: {CHECKPOINT}\n")

    results  = []
    files    = sorted(os.listdir(HIGH_RES_DIR))

    for i, filename in enumerate(files):
        hr_path  = os.path.join(HIGH_RES_DIR, filename)
        lr_path  = os.path.join(LOW_RES_DIR,  filename)

        hr_img   = cv2.imread(hr_path, cv2.IMREAD_GRAYSCALE)
        lr_img   = cv2.imread(lr_path, cv2.IMREAD_GRAYSCALE)

        if hr_img is None or lr_img is None:
            continue

        # ── Bicubic ───────────────────────────────────────────
        h, w         = hr_img.shape
        bicubic_img  = cv2.resize(lr_img, (w, h), interpolation=cv2.INTER_CUBIC)

        # ── SRCNN ─────────────────────────────────────────────
        lr_tensor    = torch.from_numpy(
                           lr_img.astype(np.float32) / 255.0
                       ).unsqueeze(0).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            sr_tensor = model(lr_tensor)

        sr_img       = sr_tensor.squeeze().cpu().numpy()
        sr_img       = np.clip(sr_img * 255.0, 0, 255).astype(np.uint8)

        # ── Metrics calculate karo ────────────────────────────
        results.append({
            "filename"      : filename,
            "Bicubic_PSNR"  : round(calculate_psnr(hr_img, bicubic_img), 4),
            "Bicubic_MSE"   : round(calculate_mse(hr_img,  bicubic_img), 4),
            "Bicubic_SSIM"  : round(calculate_ssim(hr_img, bicubic_img), 4),
            "SRCNN_PSNR"    : round(calculate_psnr(hr_img, sr_img),      4),
            "SRCNN_MSE"     : round(calculate_mse(hr_img,  sr_img),      4),
            "SRCNN_SSIM"    : round(calculate_ssim(hr_img, sr_img),      4),
        })

        if (i + 1) % 500 == 0:
            print(f"  Progress: {i+1}/{len(files)} done...")

    # ── Results save karo ─────────────────────────────────────
    df           = pd.DataFrame(results)
    output_path  = os.path.join(RESULTS_DIR, "evaluation_results.csv")
    df.to_csv(output_path, index=False)

    # ── Final Comparison Table print karo ─────────────────────
    print(f"\n{'='*50}")
    print(f"  FINAL RESULTS COMPARISON")
    print(f"{'='*50}")
    print(f"  Metric  |  Bicubic   |  SRCNN")
    print(f"{'─'*50}")
    print(f"  PSNR    |  {df['Bicubic_PSNR'].mean():.4f}  |  {df['SRCNN_PSNR'].mean():.4f} dB")
    print(f"  MSE     |  {df['Bicubic_MSE'].mean():.4f} |  {df['SRCNN_MSE'].mean():.4f}")
    print(f"  SSIM    |  {df['Bicubic_SSIM'].mean():.4f}  |  {df['SRCNN_SSIM'].mean():.4f}")
    print(f"{'='*50}")
    print(f"\n🎉 Evaluation Complete!")
    print(f"   Results saved in: {output_path}")

# ── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    evaluate()