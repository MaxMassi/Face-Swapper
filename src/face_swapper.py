# src/face_swapper.py

import insightface
from insightface.app import FaceAnalysis


class FaceSwapper:
    """Encapsulates the Inswapper model and swapping logic."""

    def __init__(self, model_path, analyzer_name="buffalo_l"):
        print("[INFO] Initializing Face Analysis and Swapper models...")
        self.app = FaceAnalysis(name=analyzer_name, root=".")
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        self.swapper = insightface.model_zoo.get_model(model_path)
        print("[INFO] Models initialized successfully.")

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

    def swap(self, source_img, target_img):
        """Performs a face swap from a source image to a target image."""
        source_faces = self.app.get(source_img)
        target_faces = self.app.get(target_img)

        if not source_faces or not target_faces:
            return None

        source_face = self._get_principal_face(source_faces)
        target_face = self._get_principal_face(target_faces)

        if not source_face or not target_face:
            return None

        # Perform the swap
        result_img = self.swapper.get(
            target_img, target_face, source_face, paste_back=True
        )
        return result_img
