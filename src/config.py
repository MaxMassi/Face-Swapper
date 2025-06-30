# src/config.py

# --- File Paths and Directories ---
INPUT_IMAGE_DIR = "data/input_images"
OUTPUT_DIR = "results/swapped_faces"
MODEL_DIR = "models"
SWAPPER_MODEL_PATH = f"{MODEL_DIR}/inswapper_128.onnx"

# --- Model Configuration ---
FACE_ANALYZER_MODEL = "buffalo_l"
MODEL_URL = "https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx"

# --- Dataset Curation Parameters ---
TOTAL_IMAGES_TO_GENERATE = 100
IMAGES_PER_CATEGORY = 25

# Parameters for selecting similar/dissimilar pairs
SIMILAR_MAX_AGE_DIFF = 10
DISSIMILAR_MIN_AGE_DIFF = 15
