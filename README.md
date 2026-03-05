## Satellite SRCNN

Deep Learning-Based Super-Resolution for Satellite Imaging Systems

This repository contains an implementation of a Super-Resolution Convolutional Neural Network (SRCNN) for enhancing the spatial resolution of satellite imagery. The project also includes a FastAPI-based backend for serving the model as a web service.

### Project Structure

```
satellite_srcnn/
├── backend/                    # FastAPI backend for model serving
│   ├── app/
│   │   ├── api/v1/routes/     # API endpoints (auth, images, enhance)
│   │   ├── core/              # Configuration, security, dependencies
│   │   ├── db/                # Database models and session management
│   │   ├── ml/                # ML utilities (inference, metrics)
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # Business logic services
│   └── alembic/               # Database migrations
├── checkpoints/               # Saved model checkpoints
├── data/                      # Training and evaluation datasets
│   ├── processed/             # Processed HR/LR patches
│   ├── raw/                   # Raw downloaded data
│   └── split/                 # Train/val/test splits
├── models/                    # Model architectures (SRCNN)
├── results/                   # Generated outputs
│   ├── images/                # Comparison images
│   └── metrics/               # CSV metrics (loss, PSNR, SSIM, MSE)
├── scripts/                    # Training, evaluation, and data scripts
│   ├── train.py              # SRCNN training script
│   ├── evaluate.py           # Model evaluation script
│   ├── bicubic_baseline.py   # Bicubic interpolation baseline
│   ├── prepare_data.py       # Dataset download script
│   └── preprocess.py          # Image preprocessing script
└── utils/                     # Utility functions
    └── dataset.py            # PyTorch dataset class
```

### Key Features

- **SRCNN Architecture**: Super-Resolution Convolutional Neural Network based on Dong et al. (2014)
  - Layer 1: Feature Extraction (9x9 kernel, 64 filters)
  - Layer 2: Non-linear Mapping (1x1 kernel, 32 filters)
  - Layer 3: Reconstruction (5x5 kernel, 1 filter)
- **Bicubic Interpolation Baseline**: Traditional upscaling method for comparison
- **Training Pipeline**: 200 epochs with Adam optimizer, MSE loss, best model checkpointing
- **Evaluation Metrics**: PSNR, MSE, SSIM for quantitative comparison
- **FastAPI Backend**: RESTful API for image enhancement
- **UC Merced Land Use Dataset**: Standard satellite imagery benchmark

### Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Awasthiutk564/satellite-srcnn.git
   cd satellite-srcnn
   ```

2. **Set Up Environment**
   ```bash
   # Create a Python virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies (if requirements.txt exists)
   pip install -r requirements.txt
   ```

3. **Prepare Data**
   ```bash
   # Download UC Merced Land Use Dataset
   python scripts/prepare_data.py

   # Preprocess images into HR/LR patches
   python scripts/preprocess.py
   ```
   
   This creates:
   - High-resolution patches: `data/processed/high_res/`
   - Low-resolution patches: `data/processed/low_res/`

4. **Train the Model**
   ```bash
   python scripts/train.py
   ```
   
   Training parameters:
   - Epochs: 200
   - Batch size: 16
   - Learning rate: 5e-5
   - Device: CUDA (if available) or CPU

5. **Run Evaluation**
   ```bash
   # Bicubic baseline
   python scripts/bicubic_baseline.py

   # SRCNN evaluation
   python scripts/evaluate.py
   ```

6. **Start the Backend API (Optional)**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   
   API endpoints:
   - `POST /api/v1/auth/register` - User registration
   - `POST /api/v1/auth/login` - User login
   - `POST /api/v1/images/upload` - Upload images
   - `POST /api/v1/enhance` - Enhance image using SRCNN

### Results

Evaluation results are saved in `results/metrics/`:

- `loss_history.csv` - Training and validation loss per epoch
- `bicubic_results.csv` - Bicubic baseline metrics (PSNR, MSE, SSIM)
- `evaluation_results.csv` - SRCNN vs Bicubic comparison

Sample metrics format:
| Metric | Bicubic | SRCNN |
|--------|---------|-------|
| PSNR   | ~XX dB  | ~XX dB|
| MSE    | ~XX     | ~XX   |
| SSIM   | ~0.XX   | ~0.XX |

### Architecture Details

The SRCNN model processes low-resolution satellite images through three convolutional layers:

1. **Feature Extraction Layer**: Uses 9x9 kernels to extract features from the blurry input
2. **Non-linear Mapping Layer**: Uses 1x1 kernels to map features to higher-level representations
3. **Reconstruction Layer**: Uses 5x5 kernels to reconstruct the high-resolution output

Input: Grayscale satellite images (1 channel, 99x99 pixels)
Output: Super-resolved image (1 channel, 99x99 pixels)

### Contributing

Contributions, suggestions, and issues are welcome. Feel free to open an issue or submit a pull request.

