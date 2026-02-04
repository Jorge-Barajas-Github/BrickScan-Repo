# BrickScan

A production-ready LEGO brick classifier using deep learning.

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/brickscan.git
cd brickscan

# Backend setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
```

## Project Structure

```
brickscan/
├── api/          # FastAPI backend
├── frontend/     # React PWA
├── src/          # ML training code
├── scripts/      # Utility scripts
├── notebooks/    # Exploration notebooks
├── models/       # Trained model artifacts
└── docs/         # Documentation
```

## License
MIT
