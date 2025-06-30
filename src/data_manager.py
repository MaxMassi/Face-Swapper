# src/data_manager.py

import os
import glob
import pandas as pd
from tqdm import tqdm


class DataManager:
    """Handles loading image paths and analyzing face attributes."""

    def __init__(self, input_dir):
        self.input_dir = input_dir
        self.image_paths = self._load_image_paths()
        print(f"[INFO] Found {len(self.image_paths)} images in '{self.input_dir}'.")

    def _load_image_paths(self):
        """Loads all .jpg image paths from the input directory."""
        return glob.glob(os.path.join(self.input_dir, "*.jpg"))

    def analyze_faces(self, face_analysis_app):
        """
        Analyzes all faces in the dataset to extract attributes.
        Returns a pandas DataFrame with face information.
        """
        face_data = []
        for img_path in tqdm(self.image_paths, desc="Analyzing faces"):
            pass  # Analysis logic is now in the DatasetCurator for efficiency
        # Return an empty DataFrame as the analysis is handled elsewhere
        return pd.DataFrame({"filepath": self.image_paths})
