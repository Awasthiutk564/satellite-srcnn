# =============================================================
# PHASE 2 — Dataset Download karne ka script
# UC Merced Land Use Dataset download hoga
# =============================================================

import urllib.request
import os
import zipfile

# ── Folder paths ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR  = os.path.join(BASE_DIR, "data", "raw")

# ── Dataset ka URL ────────────────────────────────────────────
URL      = "http://weegee.vision.ucmerced.edu/datasets/UCMerced_LandUse.zip"
ZIP_PATH = os.path.join(RAW_DIR, "UCMerced_LandUse.zip")

# ── Step 1: Download karo ─────────────────────────────────────
def download_dataset():
    print("Dataset download ho raha hai... thoda wait karo!")
    print("Size lagbhag 318 MB hai.\n")

    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent    = min(int(downloaded * 100 / total_size), 100)
        print(f"\rProgress: {percent}% ", end="")

    urllib.request.urlretrieve(URL, ZIP_PATH, show_progress)
    print("\n\nDownload complete! ✅")

# ── Step 2: Extract karo ──────────────────────────────────────
def extract_dataset():
    print("Files extract ho rahi hain...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(RAW_DIR)
    print("Extract complete! ✅")

# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    download_dataset()
    extract_dataset()
    print("\nDataset ready hai data/raw folder mein! 🎉")