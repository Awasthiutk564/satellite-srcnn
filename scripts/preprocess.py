# =============================================================
# PHASE 2 — Image Preprocessing Script
# Kya karta hai yeh script:
# 1. Raw satellite images load karta hai
# 2. High Resolution (HR) patches banata hai
# 3. Low Resolution (LR) patches banata hai (3x downscale)
# 4. Dono ko save karta hai processed folder mein
# =============================================================

import os
import cv2
import numpy as np

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw", "archive", "UCMerced_LandUse", "Images")
HIGH_RES_DIR = os.path.join(BASE_DIR, "data", "processed", "high_res")
LOW_RES_DIR  = os.path.join(BASE_DIR, "data", "processed", "low_res")

# ── Settings ──────────────────────────────────────────────────
PATCH_SIZE   = 99   # HR patch ka size (99x99 pixels)
SCALE_FACTOR = 3    # Kitna downscale karna hai (3x)
STRIDE       = 33   # Kitne pixels skip karke next patch lena hai
MAX_IMAGES   = 100  # Kitni images process karni hain (100 kaafi hai)

# ── Main Function ─────────────────────────────────────────────
def preprocess():
    # Counters
    patch_count = 0
    image_count = 0

    print("Preprocessing shuru ho raha hai...")
    print(f"HR Patch Size : {PATCH_SIZE}x{PATCH_SIZE}")
    print(f"LR Patch Size : {PATCH_SIZE//SCALE_FACTOR}x{PATCH_SIZE//SCALE_FACTOR}")
    print(f"Scale Factor  : {SCALE_FACTOR}x\n")

    # Har class folder mein jao (agricultural, airplane, etc.)
    for class_name in sorted(os.listdir(RAW_DIR)):
        class_path = os.path.join(RAW_DIR, class_name)

        if not os.path.isdir(class_path):
            continue

        # Har image file ko process karo
        for img_file in sorted(os.listdir(class_path)):

            # Agar enough images ho gayi toh stop karo
            if image_count >= MAX_IMAGES:
                break

            # Sirf .tif ya .png files lo
            if not (img_file.endswith('.tif') or img_file.endswith('.png')):
                continue

            img_path = os.path.join(class_path, img_file)

            # Image load karo aur grayscale banao
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            # Image ko float mein convert karo (0-1 range)
            img = img.astype(np.float32) / 255.0

            # Image se patches nikalo
            h, w = img.shape
            for y in range(0, h - PATCH_SIZE + 1, STRIDE):
                for x in range(0, w - PATCH_SIZE + 1, STRIDE):

                    # HR patch nikalo
                    hr_patch = img[y:y+PATCH_SIZE, x:x+PATCH_SIZE]

                    # LR patch banao — pehle chhota karo phir wapas bado
                    lr_small = cv2.resize(
                        hr_patch,
                        (PATCH_SIZE // SCALE_FACTOR, PATCH_SIZE // SCALE_FACTOR),
                        interpolation=cv2.INTER_CUBIC
                    )
                    lr_patch = cv2.resize(
                        lr_small,
                        (PATCH_SIZE, PATCH_SIZE),
                        interpolation=cv2.INTER_CUBIC
                    )

                    # Save karo (0-255 range mein wapas convert karke)
                    hr_save = (hr_patch * 255.0).astype(np.uint8)
                    lr_save = (lr_patch * 255.0).astype(np.uint8)

                    patch_name = f"{class_name}_{image_count:04d}_patch{patch_count:05d}.png"
                    cv2.imwrite(os.path.join(HIGH_RES_DIR, patch_name), hr_save)
                    cv2.imwrite(os.path.join(LOW_RES_DIR,  patch_name), lr_save)

                    patch_count += 1

            image_count += 1
            print(f"  ✅ Processed: {class_name}/{img_file} | Total patches: {patch_count}")

        if image_count >= MAX_IMAGES:
            break

    print(f"\n🎉 Preprocessing complete!")
    print(f"   Total images processed : {image_count}")
    print(f"   Total patches created  : {patch_count}")
    print(f"   HR patches saved in    : {HIGH_RES_DIR}")
    print(f"   LR patches saved in    : {LOW_RES_DIR}")

# ── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    preprocess()