import cv2
import numpy as np
from skimage.feature import hog, local_binary_pattern

# =========================
# Constants (KEEP SAME AS TRAINING)
# =========================
IMAGE_SIZE = (128, 128)

# HSV Histogram bins
H_BINS = 32
S_BINS = 32
V_BINS = 32

# LBP params
LBP_RADIUS = 3
LBP_POINTS = 8 * LBP_RADIUS
LBP_BINS = LBP_POINTS + 2  # uniform patterns

# =========================
# Feature Extractor
# =========================
def extract_manual_features(image_numpy: np.ndarray) -> np.ndarray:
    """
    Extract handcrafted features from an RGB image.
    
    Features:
    - HSV color histogram
    - HOG (shape)
    - LBP (texture)
    
    Args:
        image_numpy (np.ndarray): RGB image (H, W, 3)
    
    Returns:
        np.ndarray: 1D feature vector (float32)
    """

    # -------------------------
    # 1. Resize
    # -------------------------
    image_resized = cv2.resize(image_numpy, IMAGE_SIZE)

    # -------------------------
    # 2. COLOR FEATURES (HSV)
    # -------------------------
    hsv = cv2.cvtColor(image_resized, cv2.COLOR_RGB2HSV)

    hist_h = cv2.calcHist([hsv], [0], None, [H_BINS], [0, 180])
    hist_s = cv2.calcHist([hsv], [1], None, [S_BINS], [0, 256])
    hist_v = cv2.calcHist([hsv], [2], None, [V_BINS], [0, 256])

    # Normalize histograms
    cv2.normalize(hist_h, hist_h)
    cv2.normalize(hist_s, hist_s)
    cv2.normalize(hist_v, hist_v)

    color_features = np.concatenate(
        [hist_h.flatten(), hist_s.flatten(), hist_v.flatten()]
    )

    # -------------------------
    # 3. TEXTURE & SHAPE
    # -------------------------
    gray = cv2.cvtColor(image_resized, cv2.COLOR_RGB2GRAY)

    # HOG (Shape)
    hog_features = hog(
        gray,
        orientations=9,
        pixels_per_cell=(16, 16),
        cells_per_block=(2, 2),
        visualize=False,
        feature_vector=True
    )

    # LBP (Texture)
    lbp = local_binary_pattern(
        gray,
        LBP_POINTS,
        LBP_RADIUS,
        method="uniform"
    )

    lbp_hist, _ = np.histogram(
        lbp.ravel(),
        bins=np.arange(0, LBP_BINS + 1),
        range=(0, LBP_BINS)
    )

    lbp_hist = lbp_hist.astype("float")
    lbp_hist /= (lbp_hist.sum() + 1e-6)

    # -------------------------
    # 4. COMBINE ALL FEATURES
    # -------------------------
    features = np.concatenate(
        [color_features, hog_features, lbp_hist]
    )

    return features.astype(np.float32)
