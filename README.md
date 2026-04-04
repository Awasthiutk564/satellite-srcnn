# SatEnhance AI – Satellite SRCNN

Deep Learning-Based Super-Resolution for Satellite Imaging Systems with a luxurious, modern web interface.

This repository contains a full-stack application featuring a **Super-Resolution Convolutional Neural Network (SRCNN)** designed to enhance the spatial resolution of satellite imagery. It pairs an AI-powered FastAPI backend serving the model alongside a rich, aesthetically premium React frontend interface.

## Key Features

- **SRCNN Architecture**: Super-Resolution CNN based on Dong et al. (2014) to intelligently unblur images.
- **Multiple Upscaling Options**: Choose between standard Bicubic Baseline mapping or AI-powered SRCNN upscaling (2x, 3x, 4x options).
- **Luxurious UI/UX**: Premium frontend featuring dynamic *Glassmorphism*, frosted text scrolling panels, and interactive micro-animations.
- **Secure Authentication**: Backend-driven JWT authentication with SQLite UUID handling for reliable user registration and login.
- **Real-Time Processing Dashboard**: Drag-and-drop secure image upload, instant inference latency tracking, and side-by-side metric comparison (PSNR, SSIM, MSE).

## Tech Stack
- **Frontend**: React 19, Vite, TailwindCSS (v4), Axios, Lucide Icons.
- **Backend**: FastAPI, SQLAlchemy, SQLite, Uvicorn, Python-Jose (JWT), Bcrypt.
- **Machine Learning**: PyTorch (SRCNN implementation & Metrics), Torchvision.

---

 ## Getting Started

To run the full application locally, you will need to open **two separate terminal windows** (one for the backend and one for the frontend).

### 1. Clone the Repository
```bash
git clone https://github.com/Awasthiutk564/satellite-srcnn.git
cd satellite-srcnn

2. Start the Backend (API Server)
Open your first terminal in the root satellite_srcnn directory.
# Move into backend directory
cd backend

# Create and activate a Virtual Environment (Optional but recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
python -m uvicorn app.main:app --reload --port 8000

3. Start the Frontend (Website)
Open a new, second terminal in the root satellite_srcnn directory.
# Move into frontend directory
cd frontend

# Install necessary Node packages (first time only)
npm install

# Start the Vite development server
npm run dev
Right-click or Ctrl-click the local link provided in your terminal to open the aesthetic UI in your browser!

🧠 Architecture Details
The machine learning pipeline processes satellite imagery patches through three core layers:

1-> Feature Extraction Layer: Uses 9x9 kernels to extract features from the blurry input patch.
2-> Non-linear Mapping Layer: Uses 1x1 kernels to map features into a higher-level structural representation.
3-> Reconstruction Layer: Uses 5x5 kernels to seamlessly reconstruct the high-resolution output.
(Models are trained utilizing the UC Merced Land Use Dataset as a standard satellite imagery benchmark).

📈 Evaluation Results
All outputs and metrics computed against Bicubic baselines are automatically tracked. Your historical uploads are securely saved and can be found evaluated inside /backend/storage/.

Contributions and suggestions are always welcome!