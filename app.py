import streamlit as st
from PIL import Image
import io
import os
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn.functional as F

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Plant Pest Classifier", page_icon="🌿")

# --- DAFTAR NAMA KELAS ---
# PENTING: Urutan ini harus sama persis dengan urutan folder saat training (Alfabetis)
CLASS_NAMES = [
    "Beet Armyworm", "Black Hairy", "Cutworm", "Field Cricket",
    "Jute Aphid", "Jute Hairy", "Jute Red Mite", "Jute Semilooper",
    "Jute Stem Girdler", "Jute Stem Weevil", "Leaf Beetle", "Mealybug",
    "Pod Borer", "Scopula Emissaria", "Termite odontotermes (Rambur)",
    "Termite", "Yellow Mite"
]
NUM_CLASSES = len(CLASS_NAMES)

# --- KONFIGURASI PERANGKAT ---
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'mobilenet_v2_pure.pth')

@st.cache_resource
def load_model_streamlit(path):
    # 1. Inisialisasi Arsitektur Standar
    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = torch.nn.Linear(1280, NUM_CLASSES)
    
    if not os.path.exists(path):
        return None

    try:
        # 2. Load state_dict
        state_dict = torch.load(path, map_location=DEVICE, weights_only=False)
        
        # 3. Perbaikan Nama Layer (Remapping)
        new_state_dict = {}
        for k, v in state_dict.items():
            # Hapus prefix 'module.' jika ada
            name = k.replace('module.', '')
            
            # FIX: Ubah 'classifier.1.1' menjadi 'classifier.1' agar cocok dengan arsitektur
            # Ini menangani error "Missing key classifier.1.weight"
            name = name.replace('classifier.1.1.', 'classifier.1.')
            
            new_state_dict[name] = v
        
        # 4. Load ke model dengan strict=True untuk memastikan kecocokan
        model.load_state_dict(new_state_dict, strict=True)
        
        model.to(DEVICE)
        model.eval()
        return model
    except Exception as e:
        st.error(f"⚠️ Gagal memuat bobot model: {e}")
        return None

# --- PREPROCESSING (Sesuai Training Pipeline) ---
mean = [0.485, 0.456, 0.406]
std  = [0.229, 0.224, 0.225]
PREPROCESS = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])

# --- ANTARMUKA PENGGUNA ---
st.title("🌿 Plant Pest Classifier")
st.markdown("---")

model = load_model_streamlit(MODEL_PATH)

if model is None:
    st.error("Gagal memuat model. Periksa folder `model/` di GitHub Anda.")
else:
    uploaded_file = st.file_uploader("Unggah foto hama tanaman", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert('RGB')
        
        # Tampilkan kolom kiri (gambar) dan kanan (hasil)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Gambar Input", use_container_width=True)

        with col2:
            if st.button('Mulai Klasifikasi'):
                with st.spinner('Menganalisis...'):
                    # Prediksi
                    input_tensor = PREPROCESS(image).unsqueeze(0).to(DEVICE)
                    with torch.no_grad():
                        outputs = model(input_tensor)
                        probs = F.softmax(outputs, dim=1)
                        topk_prob, topk_idx = torch.topk(probs, k=5)

                    st.success("Hasil Prediksi:")
                    for i in range(3):
                        p = topk_prob[0][i].item()
                        idx = topk_idx[0][i].item()
                        
                        # Menghindari error jika p > 1.0 karena float precision
                        confidence = min(p, 1.0) 
                        
                        st.write(f"**{CLASS_NAMES[idx]}**")
                        st.progress(confidence) # Menggunakan float 0.0 - 1.0
                        st.write(f"Tingkat Keyakinan: {confidence*100:.2f}%")

# --- FOOTER ---
st.markdown("---")
st.caption("Pastikan pencahayaan gambar cukup untuk hasil maksimal.")