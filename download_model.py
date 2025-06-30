# download_model.py

import os
import requests
from tqdm import tqdm
from src import config


def download_file(url, filepath):
    """Downloads a file from a URL to a given filepath with a progress bar."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))

    with (
        open(filepath, "wb") as f,
        tqdm(
            desc=os.path.basename(filepath),
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar,
    ):
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))
    print(f"\n[INFO] Model downloaded successfully to {filepath}")


def main():
    """
    Checks if the model exists and downloads it if necessary.
    """
    model_dir = os.path.dirname(config.SWAPPER_MODEL_PATH)

    # Create model directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)

    if not os.path.exists(config.SWAPPER_MODEL_PATH):
        print(f"[INFO] Swapper model not found at {config.SWAPPER_MODEL_PATH}.")
        print("[INFO] Downloading inswapper_128.onnx model...")
        download_file(config.MODEL_URL, config.SWAPPER_MODEL_PATH)
    else:
        print(f"[INFO] Swapper model already exists at {config.SWAPPER_MODEL_PATH}.")


if __name__ == "__main__":
    main()
