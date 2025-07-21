import json
from pathlib import Path

class PaletteSuggester:
    def __init__(self):
        palette_path = Path(__file__).parent / 'palettes.json'
        with open(palette_path, 'r') as f:
            self.palettes = json.load(f)

    def get_palette(self, analysis_results):
        undertone = analysis_results['undertone']
        contrast = analysis_results['contrast']
        
        # Main seasonal classification
        if undertone == 'Cool':
            season = 'Winter' if contrast == 'High' else 'Summer'
        else: # Warm undertone
            season = 'Spring' if contrast == 'High' else 'Autumn'
        
        # Fine-tuning to a specific archetype (simple example)
        # This can be expanded with more rules based on brightness
        if season == 'Winter':
            final_season = 'Cool Winter'
        elif season == 'Summer':
            final_season = 'Soft Summer'
        elif season == 'Spring':
            final_season = 'Light Spring'
        else: # Autumn
            final_season = 'Warm Autumn'

        palette = self.palettes.get(final_season)
        if not palette:
            raise KeyError(f"Palette for '{final_season}' not found in palettes.json")
            
        return {'season': final_season, **palette}