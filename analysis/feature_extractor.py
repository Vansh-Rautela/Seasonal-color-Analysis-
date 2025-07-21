import cv2
import mediapipe as mp
import numpy as np
from utils.color_utils import get_dominant_color, correct_color_cast, rgb_to_cielab, calculate_color_difference

# CORRECTED: Updated iris landmark indices to the official 468-478 range.
LANDMARK_INDICES = {
    'left_cheek': [234, 132, 127],
    'right_cheek': [454, 361, 356],
    'forehead': [10, 107, 105],
    'chin': [152, 172, 148],
    # The official MediaPipe iris landmarks are from 468 to 477.
    # Right eye is 468-472, Left eye is 473-477.
    'left_eye_iris': list(range(473, 478)),
    'right_eye_iris': list(range(468, 473)),
    'hairline': [10, 338, 297, 334, 109]
}

class FacialFeatureExtractor:
    def __init__(self):
        # Refined the Face Mesh call for better performance.
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True, # This MUST be True to get iris landmarks.
            min_detection_confidence=0.5
        )

    def _create_mask(self, landmarks, image_shape):
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        # Ensure landmarks are valid before creating points
        if not landmarks or any(l is None for l in landmarks):
            return mask
        points = np.array([[int(pt.x * image_shape[1]), int(pt.y * image_shape[0])] for pt in landmarks])
        if len(points) > 2:
            cv2.fillConvexPoly(mask, points, 255)
        return mask

    def extract_features(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at {image_path}")

        corrected_image = correct_color_cast(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        results = self.face_mesh.process(corrected_image)
        if not results.multi_face_landmarks:
            raise ValueError("No face detected in the image.")

        face_landmarks = results.multi_face_landmarks[0].landmark
        
        # Check if the number of landmarks is sufficient for iris detection
        if len(face_landmarks) < 478:
            raise ValueError("Could not refine landmarks for iris detection. Ensure a clear, well-lit frontal face picture.")

        # Advanced 6-point skin sampling with outlier removal
        skin_points_rgb = []
        skin_sampling_areas = ['left_cheek', 'right_cheek', 'forehead', 'chin']
        for area in skin_sampling_areas:
            indices = LANDMARK_INDICES[area]
            feature_landmarks = [face_landmarks[i] for i in indices]
            mask = self._create_mask(feature_landmarks, corrected_image.shape)
            color = get_dominant_color(corrected_image, mask)
            if color:
                skin_points_rgb.append(color)

        if not skin_points_rgb:
            raise ValueError("Could not extract sufficient skin color data.")

        skin_points_lab = [rgb_to_cielab(c) for c in skin_points_rgb]
        avg_lab = np.mean(skin_points_lab, axis=0)
        distances = [calculate_color_difference(p, avg_lab) for p in skin_points_lab]
        
        std_dev = np.std(distances)
        filtered_points_rgb = [skin_points_rgb[i] for i, d in enumerate(distances) if d < np.mean(distances) + std_dev]
        
        if not filtered_points_rgb:
             filtered_points_rgb = skin_points_rgb

        avg_skin_color = np.mean(filtered_points_rgb, axis=0).astype(int)

        dominant_colors = {'skin': tuple(avg_skin_color)}
        
        # Extract Eye color using corrected indices
        left_eye_lms = [face_landmarks[i] for i in LANDMARK_INDICES['left_eye_iris']]
        right_eye_lms = [face_landmarks[i] for i in LANDMARK_INDICES['right_eye_iris']]
        eye_mask = self._create_mask(left_eye_lms + right_eye_lms, corrected_image.shape)
        eye_color = get_dominant_color(corrected_image, eye_mask)
        if eye_color:
            dominant_colors['eyes'] = eye_color

        # Hair color
        hair_lms = [face_landmarks[i] for i in LANDMARK_INDICES['hairline']]
        y_coords = [int(pt.y * corrected_image.shape[0]) for pt in hair_lms]
        hair_mask = np.zeros(corrected_image.shape[:2], dtype=np.uint8)
        hair_mask[0:min(y_coords), :] = 255
        hair_color = get_dominant_color(corrected_image, hair_mask)
        if hair_color:
            dominant_colors['hair'] = hair_color
            
        return dominant_colors