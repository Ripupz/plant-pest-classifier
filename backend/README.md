# Server for Plant Pest Classifier

This folder contains a minimal FastAPI server that loads a PyTorch model and exposes a `/predict` endpoint.

## Requirements

- Python 3.8+
- PyTorch (install proper wheel for your platform; CPU wheel works with `pip install torch torchvision` but you may need a specific command on Windows)

## Install

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Note: Installing `torch` on Windows often requires the correct wheel or using `pip` instructions from https://pytorch.org/get-started/locally/. If `pip install torch` fails, follow the official guide.

## Run

Place your PyTorch model file at `model/mobilenet_v2_pure.pth` (path is relative to repo root).

Start the server:

```bash
uvicorn server.app:app --reload --host 0.0.0.0 --port 8000
```

The frontend (Vite) typically runs on port `5173` and will POST images to `http://localhost:8000/predict`.

## Response format

`POST /predict` returns JSON like:

```json
{
  "predictions": [
    { "className": "class_17", "probability": 0.74 },
    { "className": "class_3", "probability": 0.12 }
  ]
}
```

Replace `class_{idx}` with your own labels if you have a label mapping.
