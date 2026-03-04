# =============================================================
# PHASE 5 — Custom Dataset Class
# Kya karta hai:
# PyTorch ko batata hai ki images kahan se load karni hain
# aur kaise prepare karni hain training ke liye
# =============================================================

import os
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset

class SatelliteDataset(Dataset):
    def __init__(self, hr_dir, lr_dir):
        # HR aur LR folders ke paths store karo
        self.hr_dir   = hr_dir
        self.lr_dir   = lr_dir

        # Saari files ki list banao
        self.files    = sorted(os.listdir(hr_dir))

        print(f"Dataset loaded! Total patches: {len(self.files)}")

    def __len__(self):
        # Kitni images hain total
        return len(self.files)

    def __getitem__(self, index):
        # Ek image pair load karo (HR + LR)
        filename = self.files[index]

        hr_path  = os.path.join(self.hr_dir, filename)
        lr_path  = os.path.join(self.lr_dir, filename)

        # Images load karo grayscale mein
        hr_img   = cv2.imread(hr_path, cv2.IMREAD_GRAYSCALE)
        lr_img   = cv2.imread(lr_path, cv2.IMREAD_GRAYSCALE)

        # 0-255 se 0-1 range mein convert karo
        hr_img   = hr_img.astype(np.float32) / 255.0
        lr_img   = lr_img.astype(np.float32) / 255.0

        # PyTorch tensor mein convert karo
        # (H, W) → (1, H, W) — channel dimension add karo
        hr_tensor = torch.from_numpy(hr_img).unsqueeze(0)
        lr_tensor = torch.from_numpy(lr_img).unsqueeze(0)

        return lr_tensor, hr_tensor