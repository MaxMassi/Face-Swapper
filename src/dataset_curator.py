# src/dataset_curator.py

import os
import random
import cv2
import pandas as pd


class DatasetCurator:
    """Contains the logic for selecting the 100 image pairs."""

    def __init__(self, face_data_df):
        self.df = face_data_df
        self.image_paths = self.df["filepath"].tolist()
        self.face_attributes = {}  # Cache for face analysis results
        self.used_pairs = set()

    def _get_face_attributes(self, img_path, app):
        """Analyzes a face and caches the result."""
        if img_path in self.face_attributes:
            return self.face_attributes[img_path]

        img = cv2.imread(img_path)
        if img is None:
            return None

        faces = app.get(img)
        self.face_attributes[img_path] = faces
        return faces

    def _get_principal_face(self, faces):
        """Returns the largest face from a list of detected faces."""
        if not faces:
            return None
        return sorted(
            faces,
            key=lambda face: (face.bbox[2] - face.bbox[0])
            * (face.bbox[3] - face.bbox[1]),
            reverse=True,
        )[0]

    def _select_similar_pair(self, app, max_age_diff=10):
        while True:
            path1, path2 = random.sample(self.image_paths, 2)

            faces1 = self._get_face_attributes(path1, app)
            faces2 = self._get_face_attributes(path2, app)

            if faces1 and faces2:
                face1 = self._get_principal_face(faces1)
                face2 = self._get_principal_face(faces2)
                if (
                    face1
                    and face2
                    and face1.gender == face2.gender
                    and abs(face1.age - face2.age) <= max_age_diff
                ):
                    return os.path.basename(path1), os.path.basename(path2)

    def _select_dissimilar_pair(self, app, min_age_diff=15):
        while True:
            path1, path2 = random.sample(self.image_paths, 2)

            faces1 = self._get_face_attributes(path1, app)
            faces2 = self._get_face_attributes(path2, app)

            if faces1 and faces2:
                face1 = self._get_principal_face(faces1)
                face2 = self._get_principal_face(faces2)
                if (
                    face1
                    and face2
                    and (
                        face1.gender != face2.gender
                        or abs(face1.age - face2.age) >= min_age_diff
                    )
                ):
                    return os.path.basename(path1), os.path.basename(path2)

    def generate_swap_pairs(self, app, num_per_category=25):
        """Generates the final list of 100 source/target pairs."""
        swap_list = []

        # Category 1: Similar Pairs
        for _ in range(num_per_category):
            source, target = self._select_similar_pair(app)
            swap_list.append(
                {
                    "source_file": source,
                    "target_file": target,
                    "pre_process": False,
                    "post_process": False,
                }
            )

        # Category 2: Dissimilar Pairs
        for _ in range(num_per_category):
            source, target = self._select_dissimilar_pair(app)
            swap_list.append(
                {
                    "source_file": source,
                    "target_file": target,
                    "pre_process": False,
                    "post_process": False,
                }
            )

        # Category 3: Random Pairs
        for _ in range(num_per_category):
            source, target = random.sample(self.image_paths, 2)
            swap_list.append(
                {
                    "source_file": os.path.basename(source),
                    "target_file": os.path.basename(target),
                    "pre_process": False,
                    "post_process": False,
                }
            )

        # Category 4: Processed Random Pairs
        for _ in range(num_per_category):
            source, target = random.sample(self.image_paths, 2)
            swap_list.append(
                {
                    "source_file": os.path.basename(source),
                    "target_file": os.path.basename(target),
                    "pre_process": True,
                    "post_process": True,
                }
            )

        return swap_list
