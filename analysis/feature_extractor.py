import cv2
import mediapipe as mp
import numpy as np
from utils.color_utils import get_dominant_color

# Define landmark indices for facial features (these are examples and can be refined)
LANDMARK_INDICES = {
    'skin': [234, 127, 356, 454, 152, 10, 338], # Forehead, cheeks, chin
    'left_eye': [33, 160, 158, 133, 153, 144],
    'right_eye': [362, 385, 387, 263, 373, 380],
    'hair': [10, 338, 297, 334, 105, 103, 54, 107] # Hairline approximation
}

class FacialFeatureExtractor:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

    def _create_mask(self, landmarks, image_shape):
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        points = np.array([[int(pt.x * image_shape[1]), int(pt.y * image_shape[0])] for pt in landmarks])
        cv2.fillConvexPoly(mask, points, 255)
        return mask

    def extract_features(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at {image_path}")
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            raise ValueError("No face detected in the image.")

        face_landmarks = results.multi_face_landmarks[0].landmark
        
        dominant_colors = {}
        for feature, indices in LANDMARK_INDICES.items():
            feature_landmarks = [face_landmarks[i] for i in indices]
            mask = self._create_mask(feature_landmarks, image_rgb.shape)
            
            # For hair, we sample from the top of the mask
            if feature == 'hair':
                y_coords = [int(pt.y * image_rgb.shape[0]) for pt in feature_landmarks]
                mask[:min(y_coords), :] = 0 # Mask out the face below hairline

            color = get_dominant_color(image_rgb, mask)
            if color:
                dominant_colors[feature] = color
        
        return dominant_colors