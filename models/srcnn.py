import torch
import torch.nn as nn

class SRCNN(nn.Module):
    """
    Super-Resolution Convolutional Neural Network (SRCNN)
    Architecture:
    - Layer 1: Feature extraction (9x9 kernel, 64 filters)
    - Layer 2: Non-linear mapping (1x1 kernel, 32 filters)
    - Layer 3: Reconstruction (5x5 kernel, 1 filter)
    """
    def __init__(self, num_channels=1):
        super(SRCNN, self).__init__()
        # Layer 1: Feature Extraction
        self.conv1 = nn.Conv2d(num_channels, 64, kernel_size=9, padding=4)
        # Layer 2: Non-linear Mapping
        self.conv2 = nn.Conv2d(64, 32, kernel_size=1, padding=0)
        # Layer 3: Reconstruction
        self.conv3 = nn.Conv2d(32, num_channels, kernel_size=5, padding=2)
        
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.conv3(x)
        return x
