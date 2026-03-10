# =============================================================
# PHASE 5 — Training Script
# Kya karta hai:
# 1. Dataset load karta hai
# 2. SRCNN model banata hai
# 3. 50 epochs tak train karta hai
# 4. Har epoch ka loss save karta hai
# 5. Best model checkpoint save karta hai
# =============================================================

import os
import sys
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split

# Apne modules import karo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.srcnn       import SRCNN  # pyright: ignore[reportMissingImports]
from utils.dataset      import SatelliteDataset

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIGH_RES_DIR = os.path.join(BASE_DIR, "data", "processed", "high_res")
LOW_RES_DIR  = os.path.join(BASE_DIR, "data", "processed", "low_res")
CHECKPOINT   = os.path.join(BASE_DIR, "checkpoints")

# ── Settings ──────────────────────────────────────────────────
BATCH_SIZE   = 16
NUM_EPOCHS   = 200
LEARNING_RATE= 5e-5 
DEVICE       = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Main Training Function ────────────────────────────────────
def train():
    print(f"Training shuru ho raha hai!")
    print(f"Device : {DEVICE}")
    print(f"Epochs : {NUM_EPOCHS}")
    print(f"Batch  : {BATCH_SIZE}\n")

    # ── Dataset load karo ─────────────────────────────────────
    full_dataset = SatelliteDataset(HIGH_RES_DIR, LOW_RES_DIR)

    # Train aur Validation split karo (80% train, 20% val)
    train_size   = int(0.8 * len(full_dataset))
    val_size     = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader   = DataLoader(val_dataset,   batch_size=BATCH_SIZE, shuffle=False)

    print(f"Train patches : {train_size}")
    print(f"Val patches   : {val_size}\n")

    # ── Model, Loss, Optimizer ────────────────────────────────
    model        = SRCNN().to(DEVICE)
    criterion    = nn.MSELoss()        # Loss = predicted aur actual ka difference
    optimizer    = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_val_loss= float('inf')
    train_losses = []
    val_losses   = []

    # ── Training Loop ─────────────────────────────────────────
    for epoch in range(1, NUM_EPOCHS + 1):

        # ── Train ─────────────────────────────────────────────
        model.train()
        train_loss = 0.0

        for lr_imgs, hr_imgs in train_loader:
            lr_imgs  = lr_imgs.to(DEVICE)
            hr_imgs  = hr_imgs.to(DEVICE)

            # Forward pass — model se output lo
            outputs  = model(lr_imgs)

            # Loss calculate karo
            loss     = criterion(outputs, hr_imgs)

            # Backward pass — weights update karo
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        avg_train_loss = train_loss / len(train_loader)

        # ── Validation ────────────────────────────────────────
        model.eval()
        val_loss = 0.0

        with torch.no_grad():
            for lr_imgs, hr_imgs in val_loader:
                lr_imgs  = lr_imgs.to(DEVICE)
                hr_imgs  = hr_imgs.to(DEVICE)
                outputs  = model(lr_imgs)
                loss     = criterion(outputs, hr_imgs)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)

        train_losses.append(avg_train_loss)
        val_losses.append(avg_val_loss)

        # ── Progress Print karo ───────────────────────────────
        print(f"Epoch [{epoch:02d}/{NUM_EPOCHS}] "
              f"Train Loss: {avg_train_loss:.6f} | "
              f"Val Loss: {avg_val_loss:.6f}")

        # ── Best Model Save karo ──────────────────────────────
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(),
                       os.path.join(CHECKPOINT, "srcnn_best.pth"))
            print(f"  ✅ Best model saved! Val Loss: {best_val_loss:.6f}")

    # ── Final Model Save karo ─────────────────────────────────
    torch.save(model.state_dict(),
               os.path.join(CHECKPOINT, "srcnn_final.pth"))

    print(f"\n🎉 Training Complete!")
    print(f"   Best Val Loss : {best_val_loss:.6f}")
    print(f"   Model saved in: {CHECKPOINT}")

    # ── Loss history save karo ────────────────────────────────
    import pandas as pd
    loss_df = pd.DataFrame({
        "epoch"      : list(range(1, NUM_EPOCHS + 1)),
        "train_loss" : train_losses,
        "val_loss"   : val_losses
    })
    loss_path = os.path.join(BASE_DIR, "results", "metrics", "loss_history.csv")
    loss_df.to_csv(loss_path, index=False)
    print(f"   Loss history  : {loss_path}")

# ── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    train()