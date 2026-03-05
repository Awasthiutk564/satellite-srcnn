from __future__ import annotations

from pathlib import Path
from typing import Tuple

import torch

from models.srcnn import SRCNN


BASE_DIR = Path(__file__).resolve().parents[2]
CHECKPOINTS_DIR = BASE_DIR / "checkpoints"
DEFAULT_WEIGHTS_PATH = CHECKPOINTS_DIR / "srcnn_best.pth"

_model: SRCNN | None = None
_device: torch.device | None = None


def _load_model() -> Tuple[SRCNN, torch.device]:
    global _model, _device

    if _model is not None and _device is not None:
        return _model, _device

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SRCNN().to(device)

    if DEFAULT_WEIGHTS_PATH.exists():
        state = torch.load(DEFAULT_WEIGHTS_PATH, map_location=device)
        model.load_state_dict(state)

    model.eval()
    _model, _device = model, device
    return model, device


def get_srcnn_model() -> Tuple[SRCNN, torch.device]:
    \"\"\"Return a lazily-loaded SRCNN model and device.

    If the checkpoint is missing, the model will run with randomly
    initialized weights so that the API still functions for demos.
    \"\"\""
    return _load_model()

