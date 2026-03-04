# =============================================================
# PHASE 4 — SRCNN Model Definition
# Original Paper: Dong et al. (2014)
# "Learning a Deep Convolutional Network for Image Super-Resolution"
#
# Architecture:
# Layer 1 — Feature Extraction    (9x9 kernel, 64 filters)
# Layer 2 — Non-linear Mapping    (1x1 kernel, 32 filters)
# Layer 3 — Reconstruction        (5x5 kernel,  1 filter)
# =============================================================

import torch
import torch.nn as nn

class SRCNN(nn.Module):
    def __init__(self):
        super(SRCNN, self).__init__()

        # ── Layer 1: Feature Extraction ───────────────────────
        # Blurry image se important features/patterns nikalta hai
        # 9x9 bada kernel isliye ki zyada area dekh sake
        self.layer1 = nn.Sequential(
            nn.Conv2d(
                in_channels  = 1,   # Grayscale image = 1 channel
                out_channels = 64,  # 64 alag alag features dhundega
                kernel_size  = 9,   # 9x9 pixels ka area dekh ke
                padding      = 4    # Image size same rakhne ke liye
            ),
            nn.ReLU(inplace=True)   # Negative values zero kar do
        )

        # ── Layer 2: Non-linear Mapping ───────────────────────
        # Features ko better representation mein convert karta hai
        # 1x1 kernel isliye ki pixel-wise mapping kare
        self.layer2 = nn.Sequential(
            nn.Conv2d(
                in_channels  = 64,  # Layer 1 ke 64 features aate hain
                out_channels = 32,  # 32 refined features nikalega
                kernel_size  = 1,   # 1x1 pixel dekh ke
                padding      = 0
            ),
            nn.ReLU(inplace=True)
        )

        # ── Layer 3: Reconstruction ───────────────────────────
        # Final sharp image banata hai
        # 5x5 kernel isliye ki smooth reconstruction ho
        self.layer3 = nn.Conv2d(
            in_channels  = 32,  # Layer 2 ke 32 features aate hain
            out_channels = 1,   # Final output = 1 channel grayscale
            kernel_size  = 5,   # 5x5 pixels ka area dekh ke
            padding      = 2    # Image size same rakhne ke liye
        )

        # ── Weights Initialize karo ───────────────────────────
        self._initialize_weights()

    def forward(self, x):
        # Yeh function batata hai ki data kaise flow karega
        # Input blurry image → Layer1 → Layer2 → Layer3 → Sharp image
        x = self.layer1(x)  # Feature extraction
        x = self.layer2(x)  # Non-linear mapping
        x = self.layer3(x)  # Reconstruction
        return x

    def _initialize_weights(self):
        # Weights sahi se initialize karo training ke liye
        for layer in [self.layer1, self.layer2, self.layer3]:
            if isinstance(layer, nn.Sequential):
                for module in layer:
                    if isinstance(module, nn.Conv2d):
                        nn.init.normal_(module.weight, mean=0, std=0.001)
                        nn.init.zeros_(module.bias)
            elif isinstance(layer, nn.Conv2d):
                nn.init.normal_(layer.weight, mean=0, std=0.001)
                nn.init.zeros_(layer.bias)


# ── Quick Test ────────────────────────────────────────────────
if __name__ == "__main__":
    import torch

    # Fake input banao — 1 image, 1 channel, 99x99 pixels
    dummy_input = torch.randn(1, 1, 99, 99)

    # Model banao
    model       = SRCNN()

    # Forward pass karo
    output      = model(dummy_input)

    print("SRCNN Model Ready! ✅")
    print(f"Input  shape : {dummy_input.shape}")
    print(f"Output shape : {output.shape}")
    print(f"\nModel Architecture:")
    print(model)