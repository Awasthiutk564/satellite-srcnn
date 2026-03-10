from __future__ import annotations

import torch
import torch.nn as nn
from pathlib import Path

# Fix BASE_DIR to point to satellite_srcnn/
BASE_DIR = Path(__file__).resolve().parents[3]

class SRCNN(nn.Module):
    def __init__(self, num_channels=1):
        super(SRCNN, self).__init__()
        self.conv1 = nn.Conv2d(num_channels, 64, kernel_size=9, padding=9 // 2)
        self.conv2 = nn.Conv2d(64, 32, kernel_size=5, padding=5 // 2)
        self.conv3 = nn.Conv2d(32, num_channels, kernel_size=5, padding=5 // 2)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.conv3(x)
        return x

def load_pretrained_model(device: torch.device, checkpoint_path: str | Path | None = None) -> SRCNN:
    model = SRCNN().to(device)
    
    if checkpoint_path is None:
        checkpoint_path = BASE_DIR / "checkpoints" / "srcnn_best.pth"
    
    if not Path(checkpoint_path).exists():
        raise FileNotFoundError(f"Model checkpoint not found at {checkpoint_path}")
    
    state_dict = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(state_dict)
    model.eval()
    return model
