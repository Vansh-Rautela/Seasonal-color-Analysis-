import cv2
import numpy as np
from sklearn.cluster import KMeans

def correct_color_cast(image):
    """
    Corrects the color cast of an image using the Grey World algorithm.
    """
    # Split the image into its respective channels
    r, g, b = cv2.split(image)
    
    # Calculate the average of each channel
    r_avg = cv2.mean(r)[0]
    g_avg = cv2.mean(g)[0]
    b_avg = cv2.mean(b)[0]
    
    # Calculate the overall average
    avg_gray = (r_avg + g_avg + b_avg) / 3
    
    # Calculate the scaling factors
    r_scale = avg_gray / r_avg
    g_scale = avg_gray / g_avg
    b_scale = avg_gray / b_avg
    
    # Scale the channels
    r = cv2.multiply(r, r_scale).astype('uint8')
    g = cv2.multiply(g, g_scale).astype('uint8')
    b = cv2.multiply(b, b_scale).astype('uint8')
    
    # Merge the channels back
    corrected_image = cv2.merge([r, g, b])
    return corrected_image

def get_dominant_color(image, mask):
    """
    Finds the dominant color in a masked region of an image using k-means clustering.
    """
    pixels = image[mask.astype(bool)]
    if len(pixels) < 10:
        return None
    pixels = np.float32(pixels)
    kmeans = KMeans(n_clusters=1, n_init=10, random_state=0)
    kmeans.fit(pixels)
    return tuple(kmeans.cluster_centers_[0].astype(int))

def rgb_to_cielab(rgb_color):
    """
    Converts a single RGB color to the CIELAB color space, ensuring correct data types.
    """
    rgb_np_array = np.array(rgb_color, dtype=np.uint8)
    rgb_color_3d = np.reshape(rgb_np_array, (1, 1, 3))
    lab_color = cv2.cvtColor(rgb_color_3d, cv2.COLOR_RGB2LAB)
    return lab_color[0][0]

def calculate_chroma(a_star, b_star):
    """
    Calculates the Chroma (C*) value from a* and b* components of CIELAB color space.
    """
    return np.sqrt(a_star**2 + b_star**2)

def calculate_color_difference(lab1, lab2):
    """
    Calculates the perceptual color difference between two CIELAB colors using Delta E 2000.
    This is a simplified implementation for outlier detection.
    """
    return np.linalg.norm(np.array(lab1) - np.array(lab2))