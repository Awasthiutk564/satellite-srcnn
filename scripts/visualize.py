# =============================================================
# PHASE 7 — Visualization Script
# Kya karta hai:
# 1. Loss curve graph banata hai
# 2. PSNR/SSIM/MSE bar charts banata hai
# 3. Before/After image comparison banata hai
# 4. Sab kuch results/images folder mein save karta hai
# =============================================================

import os
import sys
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.srcnn import SRCNN

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR  = os.path.join(BASE_DIR, "results", "images")
METRICS_DIR  = os.path.join(BASE_DIR, "results", "metrics")
HIGH_RES_DIR = os.path.join(BASE_DIR, "data", "processed", "high_res")
LOW_RES_DIR  = os.path.join(BASE_DIR, "data", "processed", "low_res")
CHECKPOINT   = os.path.join(BASE_DIR, "checkpoints", "srcnn_best.pth")
DEVICE       = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Graph 1: Loss Curve ───────────────────────────────────────
def plot_loss_curve():
    loss_path = os.path.join(METRICS_DIR, "loss_history.csv")
    df        = pd.read_csv(loss_path)

    plt.figure(figsize=(10, 5))
    plt.plot(df["epoch"], df["train_loss"], label="Train Loss", color="blue",   linewidth=2)
    plt.plot(df["epoch"], df["val_loss"],   label="Val Loss",   color="orange", linewidth=2)
    plt.xlabel("Epoch",     fontsize=13)
    plt.ylabel("Loss",      fontsize=13)
    plt.title("SRCNN Training Loss Curve", fontsize=15)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.tight_layout()

    save_path = os.path.join(RESULTS_DIR, "loss_curve.png")
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"✅ Loss curve saved: {save_path}")

# ── Graph 2: Metrics Comparison Bar Chart ────────────────────
def plot_metrics_comparison():
    eval_path  = os.path.join(METRICS_DIR, "evaluation_results.csv")
    df         = pd.read_csv(eval_path)

    metrics    = ["PSNR", "MSE", "SSIM"]
    bicubic    = [df["Bicubic_PSNR"].mean(), df["Bicubic_MSE"].mean(), df["Bicubic_SSIM"].mean()]
    srcnn      = [df["SRCNN_PSNR"].mean(),   df["SRCNN_MSE"].mean(),   df["SRCNN_SSIM"].mean()]

    x          = np.arange(len(metrics))
    width      = 0.35

    fig, axes  = plt.subplots(1, 3, figsize=(15, 5))

    colors_b   = ["#4C72B0", "#4C72B0", "#4C72B0"]
    colors_s   = ["#DD8452", "#DD8452", "#DD8452"]

    for i, (ax, metric, bval, sval) in enumerate(zip(axes, metrics, bicubic, srcnn)):
        bars = ax.bar(["Bicubic", "SRCNN"], [bval, sval],
                      color=[colors_b[i], colors_s[i]],
                      width=0.5, edgecolor="black")

        # Values dikhao bars ke upar
        for bar, val in zip(bars, [bval, sval]):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.01 * bar.get_height(),
                    f"{val:.4f}", ha="center", va="bottom", fontsize=11)

        ax.set_title(f"{metric} Comparison", fontsize=13)
        ax.set_ylabel(metric, fontsize=11)
        ax.grid(axis="y", alpha=0.5)

    plt.suptitle("Bicubic vs SRCNN — Performance Comparison", fontsize=15)
    plt.tight_layout()

    save_path = os.path.join(RESULTS_DIR, "metrics_comparison.png")
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"✅ Metrics comparison saved: {save_path}")

# ── Graph 3: Before/After Image Comparison ───────────────────
def plot_image_comparison():
    model = SRCNN().to(DEVICE)
    model.load_state_dict(torch.load(CHECKPOINT, map_location=DEVICE))
    model.eval()

    # Pehli 3 images lo comparison ke liye
    files = sorted(os.listdir(HIGH_RES_DIR))[:3]

    fig, axes = plt.subplots(3, 3, figsize=(12, 12))

    col_titles = ["Low Resolution\n(Input)", "Bicubic\n(Baseline)", "SRCNN\n(Ours)"]
    for ax, title in zip(axes[0], col_titles):
        ax.set_title(title, fontsize=13, fontweight="bold")

    for row, filename in enumerate(files):
        hr_path  = os.path.join(HIGH_RES_DIR, filename)
        lr_path  = os.path.join(LOW_RES_DIR,  filename)

        hr_img   = cv2.imread(hr_path, cv2.IMREAD_GRAYSCALE)
        lr_img   = cv2.imread(lr_path, cv2.IMREAD_GRAYSCALE)

        # Bicubic
        h, w        = hr_img.shape
        bicubic_img = cv2.resize(lr_img, (w, h), interpolation=cv2.INTER_CUBIC)

        # SRCNN
        lr_tensor   = torch.from_numpy(
                          lr_img.astype(np.float32) / 255.0
                      ).unsqueeze(0).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            sr_tensor = model(lr_tensor)

        sr_img      = sr_tensor.squeeze().cpu().numpy()
        sr_img      = np.clip(sr_img * 255.0, 0, 255).astype(np.uint8)

        # Plot karo
        axes[row][0].imshow(lr_img,      cmap="gray")
        axes[row][1].imshow(bicubic_img, cmap="gray")
        axes[row][2].imshow(sr_img,      cmap="gray")

        for ax in axes[row]:
            ax.axis("off")

    plt.suptitle("Visual Comparison: LR vs Bicubic vs SRCNN",
                 fontsize=15, fontweight="bold")
    plt.tight_layout()

    save_path = os.path.join(RESULTS_DIR, "image_comparison.png")
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"✅ Image comparison saved: {save_path}")

# ── Run All ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("Visualizations ban rahi hain...\n")
    plot_loss_curve()
    plot_metrics_comparison()
    plot_image_comparison()
    print(f"\n🎉 Sab graphs ban gaye! Check karo: results/images/")