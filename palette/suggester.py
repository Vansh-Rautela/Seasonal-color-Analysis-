import json
from pathlib import Path

class PaletteSuggester:
    def __init__(self):
        palette_path = Path(__file__).parent / 'palettes.json'
        with open(palette_path, 'r') as f:
            self.palettes = json.load(f)

    def get_palette(self, analysis_results):
        """
        Suggests a palette using a Tonal-first approach.
        """
        tonal_type = analysis_results['tonal_type']
        undertone = analysis_results['undertone']
        brightness = analysis_results['brightness']
        chroma = analysis_results['chroma']

        # Determine the final season based on the primary tonal characteristic
        final_season = "Unknown"
        if tonal_type == 'Clear':
            final_season = 'Clear Winter' if undertone == 'Cool' else 'Clear Spring'
        elif tonal_type == 'Cool':
            final_season = 'Cool Summer' if brightness == 'Light' else 'Cool Winter'
        elif tonal_type == 'Warm':
            final_season = 'Warm Spring' if brightness == 'Light' else 'Warm Autumn'
        elif tonal_type == 'Soft':
            final_season = 'Soft Summer' if undertone == 'Cool' else 'Soft Autumn'
        elif tonal_type == 'Light':
            final_season = 'Light Summer' if undertone == 'Cool' else 'Light Spring'
        elif tonal_type == 'Deep':
            final_season = 'Deep Winter' if undertone == 'Cool' else 'Deep Autumn'
        
        # Fallback for medium types
        if final_season == "Unknown":
            if undertone == 'Cool':
                final_season = 'Cool Summer' if chroma == 'Soft' else 'Cool Winter'
            else:
                final_season = 'Warm Autumn' if chroma == 'Soft' else 'Warm Spring'
        
        palette = self.palettes.get(final_season)
        if not palette:
            raise KeyError(f"Palette for '{final_season}' not found in palettes.json")
            
        return {'season': final_season, **palette}