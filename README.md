## Satellite SRCNN

This repository contains an implementation of a Super-Resolution Convolutional Neural Network (SRCNN) for enhancing the spatial resolution of satellite imagery.

### Project structure

- `data/`: Scripts or datasets for training and evaluation (not tracked if large).
- `models/`: Saved model checkpoints and architectures.
- `scripts/`: Training, evaluation, and baseline scripts (for example bicubic baseline).
- `utils/`: Utility functions (data loading, metrics, visualization helpers).
- `results/`: Generated outputs such as loss curves, comparison images, and metrics plots.

### Key features

- Super-resolution model based on SRCNN architecture.
- Bicubic interpolation baseline for comparison.
- Training and evaluation pipelines for satellite images.
- Visualizations for loss curves, image comparisons, and metric trends.

### Getting started

1. **Clone the repository**
   ```bash
   git clone https://github.com/Awasthiutk564/satellite-srcnn.git
   cd satellite-srcnn
   ```

2. **Set up environment**
   - Create a Python virtual environment.
   - Install dependencies listed in your local environment or requirements file (if present).

3. **Prepare data**
   - Place training and evaluation satellite images under the `data/` directory following your own structure.
   - Update any data paths in scripts under `scripts/` as needed.

4. **Run training or evaluation**
   - Check `scripts/` for example scripts such as training SRCNN or running the bicubic baseline.

### Results

Generated plots and comparison images can be found under `results/`, including:

- Loss curves during training.
- Side-by-side low-resolution vs. bicubic vs. SRCNN outputs.
- Quantitative metrics comparison plots.

### Contributing

Contributions, suggestions, and issues are welcome. Feel free to open an issue or submit a pull request.

