# generate.py

import os
import cv2
from tqdm import tqdm

from src import config
from src.data_manager import DataManager
from src.dataset_curator import DatasetCurator
from src.face_swapper import FaceSwapper
from src.image_processor import apply_preprocessing, apply_postprocessing


def main():
    """
    Main pipeline to generate the face-swapped dataset.
    """
    # 1. Initialize Managers and Loaders
    print("[INFO] Initializing components...")
    data_manager = DataManager(config.INPUT_IMAGE_DIR)
    face_swapper = FaceSwapper(config.SWAPPER_MODEL_PATH, config.FACE_ANALYZER_MODEL)

    # 2. Analyze all faces in the dataset
    print("[INFO] Analyzing all faces in the input directory. This may take a while...")
    face_data_df = data_manager.analyze_faces(face_swapper.app)

    # 3. Curate the dataset to get 100 pairs
    print("[INFO] Curating the 100 image pairs for swapping...")
    curator = DatasetCurator(face_data_df)
    swap_list = curator.generate_swap_pairs()

    # 4. Perform face swapping and save results
    print(f"[INFO] Starting face swap generation for {len(swap_list)} images...")
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    count = 0

    for item in tqdm(swap_list, desc="Generating Swapped Images"):
        source_path = os.path.join(config.INPUT_IMAGE_DIR, item["source_file"])
        target_path = os.path.join(config.INPUT_IMAGE_DIR, item["target_file"])

        source_img = cv2.imread(source_path)
        target_img = cv2.imread(target_path)

        if source_img is None or target_img is None:
            print(
                f"[WARNING] Could not read one of the images: {source_path} or {target_path}"
            )
            continue

        # Apply pre-processing if required
        if item["pre_process"]:
            source_img = apply_preprocessing(source_img)
            target_img = apply_preprocessing(target_img)

        # Perform the swap
        swapped_image = face_swapper.swap(source_img, target_img)

        if swapped_image is None:
            print(
                f"[WARNING] Face swap failed for pair: {os.path.basename(source_path)} -> {os.path.basename(target_path)}"
            )
            continue

        # Apply post-processing if required
        if item["post_process"]:
            swapped_image = apply_postprocessing(swapped_image)

        # Save the result
        output_filename = os.path.join(config.OUTPUT_DIR, f"swapped_{count}.jpg")
        cv2.imwrite(output_filename, swapped_image)
        count += 1

    print(
        f"\n[INFO] Successfully generated {count} face-swapped images in '{config.OUTPUT_DIR}'."
    )
    print("[INFO] Pipeline finished.")


if __name__ == "__main__":
    main()
