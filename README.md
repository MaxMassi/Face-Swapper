# Robust Face-Swap Dataset Generator using Inswapper

This project provides an automated pipeline for generating a high-quality, robust dataset of 100 face-swapped images. The primary goal is to create a diverse dataset that can be used to train a powerful binary classifier capable of detecting face-swaps created with the `insightface` Inswapper model.

## Project Overview

In the face of advancing face-swap attacks, building robust detection models is crucial. However, the performance of these models heavily depends on the quality and diversity of the training data. This project tackles the critical first step: **intelligent dataset creation**.

Instead of generating random swaps, this pipeline employs a strategic curation process to create a dataset that covers a wide range of potential attack scenarios, ensuring a resulting classifier is difficult to fool.

### Dataset Curation Strategy

To build a robust dataset, the 100 face-swaps are generated across four distinct categories (25 images each):

1.  **Similar Face Swaps**: Swaps between faces of the same gender and with a small age difference. This teaches the classifier to detect subtle manipulations.
2.  **Dissimilar Face Swaps**: Swaps between faces with different genders or a large age gap, forcing the model to learn from more obvious artifacts.
3.  **Random Face Swaps**: Provides a baseline of randomly paired faces.
4.  **Processed Random Swaps**: Simulates real-world scenarios where attackers might use pre/post-processing to hide swap artifacts. This includes adjustments to brightness/contrast, sharpening, and blurring.

The initial dataset was also balanced by incorporating faces of Brown and Black ethnicity from the UTKFace dataset to counter the imbalance in the provided source images.

## Features

-   **Automated Pipeline**: Generate the entire 100-image dataset with a single command.
-   **Intelligent Curation**: Automatically selects face pairs based on similarity, dissimilarity, and randomness.
-   **Efficient Analysis**: Analyzes all face attributes (age, gender) once at startup to speed up the pair selection process.
-   **Image Processing**: Includes pre-processing (sharpening, contrast) and post-processing (blur) to create challenging examples for the classifier.
-   **Modular & OOP**: The code is structured professionally using classes for data management, face swapping, and curation, making it easy to read and extend.

## Project Structure

-   **`generate.py`**: The main executable script to start the dataset generation.
-   **`download_model.py`**: A one-time setup script to download the pre-trained `inswapper_128.onnx` model.
-   **`src/config.py`**: Central configuration for all file paths and generation parameters.
-   **`src/data_manager.py`**: Manages loading image paths and analyzing face attributes with `insightface`.
-   **`src/dataset_curator.py`**: Contains the core logic for selecting the 100 image pairs across the four categories.
-   **`src/face_swapper.py`**: A class that encapsulates the Inswapper model and the face-swapping functionality.
-   **`src/image_processor.py`**: Contains all image pre- and post-processing functions.
-   **`requirements.txt`**: A list of all Python packages required to run the project.

## Getting Started

### Prerequisites

-   Python 3.8+
-   `pip` and `virtualenv`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-link>
    cd Face-Swap-Dataset-Generator
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Setup

1.  **Download the ONNX Model:**
    Run the download script. This will download `inswapper_128.onnx` into the `models/` directory.
    ```bash
    python download_model.py
    ```

2.  **Add Input Images:**
    Place all your source face images (e.g., the 500+ images from FFHQ and UTKFace) inside the `data/input_images/` directory.

## Usage

To generate the full dataset of 100 face-swapped images, simply run the main script. The output images will be saved in the `results/swapped_faces/` directory.

```bash
python generate.py
```

You can change the input and output directories, as well as other parameters, in the `src/config.py` file.