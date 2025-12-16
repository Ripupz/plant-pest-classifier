from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import xgboost as xgb
from PIL import Image
import io

from feature_extractor import extract_manual_features

# =========================
# App Init
# =========================
app = FastAPI(title="Jute Pest Classifier (XGBoost)")

# Allow frontend access (Railway / Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Load Model
# =========================
model = xgb.Booster()
model.load_model("model/jute_pest_robust.json")

CLASS_NAMES = [
    "Beet Armyworm",                 # 0
    "Black Hairy",                   # 1
    "Cutworm",                       # 2
    "Field Cricket",                 # 3
    "Jute Aphid",                    # 4
    "Jute Hairy",                    # 5
    "Jute Red Mite",                 # 6
    "Jute Semilooper",               # 7
    "Jute Stem Girdler",             # 8
    "Jute Stem Weevil",              # 9
    "Leaf Beetle",                   # 10
    "Mealybug",                      # 11
    "Pod Borer",                     # 12
    "Scopula Emissaria",             # 13
    "Termite odontotermes (Rambur)", # 14
    "Termite",                       # 15
    "Yellow Mite",                   # 16
]

# =========================
# Utils
# =========================
def preprocess_image(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(image)

    features = extract_manual_features(image_np)
    features = features.reshape(1, -1)

    return xgb.DMatrix(features)

# =========================
# Routes
# =========================
@app.get("/")
def health_check():
    return {"status": "Backend is running 🚀"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()

    dmatrix = preprocess_image(image_bytes)
    preds = model.predict(dmatrix)

    pred_idx = int(np.argmax(preds))
    confidence = float(np.max(preds))

    return {
        "prediction": CLASS_NAMES[pred_idx],
        "confidence": round(confidence, 4)
    }
