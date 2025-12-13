from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os
import re
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn.functional as F

app = FastAPI(title="Plant Pest Classifier API")

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

# Allow CORS for local frontend (vite typically runs on 5173)
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attempt to locate model file in repo: ../model/mobilenet_v2_pure.pth
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'mobilenet_v2_pure.pth')


# Prepare device
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load model helper
def load_model(path: str):
    # Create a mobilenet_v2 architecture
    NUM_CLASSES = 17  # 

    model = models.mobilenet_v2(pretrained=False)
    model.classifier[1] = torch.nn.Linear(1280, NUM_CLASSES)

    try:
        checkpoint = torch.load(path, map_location=DEVICE)
    except Exception as e:
        raise RuntimeError(f"Error loading model file: {e}")

    # checkpoint may be a state_dict or full model
    if isinstance(checkpoint, dict):
        # support checkpoints saved with or without `state_dict` key
        state = checkpoint.get('state_dict', checkpoint)
        # strip 'module.' prefix if present
        new_state = {}
        for k, v in state.items():
            new_key = k.replace('module.', '')
            new_state[new_key] = v
        # Try loading directly. If keys don't match due to extra numeric nesting
        # (e.g. 'classifier.1.1.weight' vs expected 'classifier.1.weight'),
        # attempt to normalize those keys and retry. Finally fall back to
        # non-strict loading so weights with slightly different naming still
        # load where possible.
        try:
            model.load_state_dict(new_state)
        except Exception:
            # Normalize double numeric segments like '.1.1.' -> '.1.'
            adjusted_state = {}
            for k, v in new_state.items():
                # replace patterns like '.1.1.' or '.2.3.' with '.1.' or '.2.'
                k2 = re.sub(r"\.(\d+)\.(\d+)\.", r'.\1.', k)
                # also handle trailing double numeric like '.1.1' at end
                k2 = re.sub(r"\.(\d+)\.(\d+)$", r'.\1', k2)
                adjusted_state[k2] = v
            try:
                model.load_state_dict(adjusted_state)
            except Exception:
                try:
                    # try loading original checkpoint dict with non-strict
                    model.load_state_dict(new_state, strict=False)
                except Exception:
                    # last resort: try loading the raw state mapping
                    model.load_state_dict(state)
    else:
        # checkpoint is not a dict -> try to load directly
        try:
            model.load_state_dict(checkpoint)
        except Exception:
            # as fallback, assume checkpoint is the whole model
            model = checkpoint

    model.to(DEVICE)
    model.eval()
    return model

# Load model at startup if present
MODEL = None
if os.path.exists(MODEL_PATH):
    try:
        MODEL = load_model(MODEL_PATH)
        print(f"Loaded model from {MODEL_PATH} on {DEVICE}")
    except Exception as e:
        print(f"Failed to load model: {e}")
else:
    print(f"Model file not found at {MODEL_PATH}. Please place your .pth there.")

# Basic preprocessing matching common MobileNet training
PREPROCESS = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.5, 0.5, 0.5],
        std=[0.5, 0.5, 0.5]
    ),
])


@app.post('/predict')
async def predict(file: UploadFile = File(...)):



    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model not loaded on server")

    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert('RGB')
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    input_tensor = PREPROCESS(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = MODEL(input_tensor)
        if outputs.dim() == 1:
            outputs = outputs.unsqueeze(0)
        probs = F.softmax(outputs, dim=1)
        topk = torch.topk(probs, k=min(5, probs.shape[1]))
        values = topk.values.cpu().numpy().tolist()[0]
        indices = topk.indices.cpu().numpy().tolist()[0]

    # If you have a label map, replace 'class_{idx}' with real labels
    preds = []
    for idx, prob in zip(indices, values):
        preds.append({
            'className': CLASS_NAMES[idx],
            'probability': float(prob),
        })

    return {'predictions': preds}

@app.get('/')
def root():
    return {'status': 'ok', 'model_loaded': MODEL is not None}

@app.get("/health")
def health():
    return {"status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
