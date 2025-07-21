from utils.color_utils import rgb_to_cielab, calculate_chroma

class ColorAnalyzer:
    def analyze(self, dominant_colors):
        """
        Analyzes dominant colors to determine undertone, brightness, contrast, chroma, and tonal type.
        """
        if 'skin' not in dominant_colors or 'hair' not in dominant_colors or 'eyes' not in dominant_colors:
            raise ValueError("Incomplete feature data. Skin, hair, and eye color are required.")

        lab_colors = {k: rgb_to_cielab(v) for k, v in dominant_colors.items()}
        l_skin, a_skin, b_skin = lab_colors['skin']
        l_hair = lab_colors['hair'][0]
        
        # 1. Determine Brightness (Value)
        brightness = 'Light' if l_skin > 65 else 'Dark' if l_skin < 45 else 'Medium'

        # 2. Determine Undertone (Hue)
        undertone = 'Warm' if b_skin > a_skin and b_skin > 15.0 else 'Cool'

        # 3. Determine Chroma (Saturation)
        chroma_val = calculate_chroma(a_skin, b_skin)
        chroma = 'Bright' if chroma_val > 40 else 'Soft'

        # 4. Determine Contrast
        l_values = [v[0] for v in lab_colors.values()]
        contrast_val = max(l_values) - min(l_values)
        contrast = 'High' if contrast_val > 55 else 'Low' if contrast_val < 30 else 'Medium'
        
        # 5. Determine Primary Tonal Characteristic
        tonal_type = self._get_tonal_type(brightness, undertone, chroma, contrast)
            
        return {
            'tonal_type': tonal_type,
            'undertone': undertone,
            'brightness': brightness,
            'chroma': chroma,
            'contrast': contrast,
        }

    def _get_tonal_type(self, brightness, undertone, chroma, contrast):
        if brightness == 'Light' and chroma == 'Soft': return 'Light'
        if brightness == 'Dark' and chroma == 'Soft': return 'Deep'
        if undertone == 'Warm' and chroma == 'Soft': return 'Warm'
        if undertone == 'Cool' and chroma == 'Soft': return 'Cool'
        if chroma == 'Bright': return 'Clear'
        if chroma == 'Soft' and contrast == 'Low': return 'Soft'
        return "Medium" # Fallback