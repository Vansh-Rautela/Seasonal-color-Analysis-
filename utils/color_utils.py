import cv2
import numpy as np
from sklearn.cluster import KMeans

def get_dominant_color(image, mask):
    """
    Finds the dominant color in a masked region of an image using k-means clustering.
    """
    # Get pixels within the mask
    pixels = image[mask.astype(bool)]
    
    # Reshape for KMeans and handle case with too few pixels
    if len(pixels) < 5:  # Need at least 5 pixels to be meaningful
        return None
    
    # Convert to float32 for k-means
    pixels = np.float32(pixels)
    
    # Cluster to find the single most dominant color
    kmeans = KMeans(n_clusters=1, n_init=10, random_state=0)
    kmeans.fit(pixels)
    
    # Return the dominant color as an integer RGB tuple
    return tuple(kmeans.cluster_centers_[0].astype(int))

def rgb_to_cielab(rgb_color):
    """
    Converts a single RGB color to the CIELAB color space, ensuring correct data types.
    """
    # 1. Create a NumPy array from the tuple and ensure the data type is uint8
    rgb_np_array = np.array(rgb_color, dtype=np.uint8)

    # 2. Reshape the array to the (1, 1, 3) format that cvtColor expects for a single pixel
    rgb_color_3d = np.reshape(rgb_np_array, (1, 1, 3))

    # 3. Perform the color space conversion
    lab_color = cv2.cvtColor(rgb_color_3d, cv2.COLOR_RGB2LAB)

    return lab_color[0][0]