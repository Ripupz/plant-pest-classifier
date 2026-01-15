import streamlit as st
from PIL import Image
import io
import os
import re
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn.functional as F
import numpy as np

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Plant Pest Classifier", page_icon="🌿")

# --- DAFTAR NAMA KELAS ---
CLASS_NAMES = [
    "Beet Armyworm", "Black Hairy", "Cutworm", "Field Cricket",
    "Jute Aphid", "Jute Hairy", "Jute Red Mite", "Jute Semilooper",
    "Jute Stem Girdler", "Jute Stem Weevil", "Leaf Beetle", "Mealybug",
    "Pod Borer", "Scopula Emissaria", "Termite odontotermes (Rambur)",
    "Termite", "Yellow Mite"
]
NUM_CLASSES = len(CLASS_NAMES)

# --- KONFIGURASI PERANGKAT & MODEL ---
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'mobilenet_v2_pure.pth')

@st.cache_resource # Gunakan cache agar model tidak dimuat ulang setiap kali user klik tombol
def load_model_streamlit(path):
    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = torch.nn.Linear(1280, NUM_CLASSES)
    
    if not os.path.exists(path):
        return None

    try:
        checkpoint = torch.load(path, map_location=DEVICE, weights_only=False)
        state = checkpoint.get('state_dict', checkpoint)
        
        # Pembersihan key 'module.'
        new_state = {k.replace('module.', ''): v for k, v in state.items()}
        
        # Mencoba load model
        try:
            model.load_state_dict(new_state)
        except:
            model.load_state_dict(new_state, strict=False)
            
        model.to(DEVICE)
        model.eval()
        return model
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")
        return None

# --- PREPROCESSING ---

mean = [0.485, 0.456, 0.406]
std  = [0.229, 0.224, 0.225]

PREPROCESS = transforms.Compose([
    transforms.Resize((224, 224)), # Samakan dengan training: Resize langsung ke 224x224
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])

# --- ANTARMUKA PENGGUNA (UI) ---
st.title("🌿 Klasifikasi Hama Tanaman")
st.write("Unggah foto hama tanaman Anda untuk mengetahui jenisnya.")

# Load Model
model = load_model_streamlit(MODEL_PATH)

if model is None:
    st.error(f"File model tidak ditemukan di {MODEL_PATH}. Pastikan file .pth sudah diunggah ke folder 'model'.")
else:
    uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Tampilkan Gambar
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, caption='Gambar yang diunggah', use_container_width=True)
        
        if st.button('Klasifikasi Sekarang'):
            with st.spinner('Sedang menganalisis...'):
                # Proses Prediksi
                input_tensor = PREPROCESS(image).unsqueeze(0).to(DEVICE)
                
                with torch.no_grad():
                    outputs = model(input_tensor)
                    probs = F.softmax(outputs, dim=1)
                    topk = torch.topk(probs, k=3) # Ambil 3 prediksi teratas
                    
                    values = topk.values.cpu().numpy()[0]
                    indices = topk.indices.cpu().numpy()[0]

                # Tampilkan Hasil
                st.success("Hasil Analisis:")
                for i in range(len(indices)):
                    name = CLASS_NAMES[indices[i]]
                    confidence = values[i] * 100
                    st.write(f"**{name}**: {confidence:.2f}%")
                    st.progress(int(confidence))