import argparse
import json
from analysis.feature_extractor import FacialFeatureExtractor
from analysis.color_analyzer import ColorAnalyzer
from palette.suggester import PaletteSuggester

def main(image_path):
    """
    Main pipeline to run the enhanced seasonal color analysis.
    """
    try:
        # 1. Extract facial features with lighting correction and advanced sampling
        print("💡 Step 1: Applying lighting correction and extracting features...")
        extractor = FacialFeatureExtractor()
        dominant_colors = extractor.extract_features(image_path)
        print(f"🎨 Representative colors found: {dominant_colors}")

        # 2. Analyze color properties for Tonal characteristics
        print("\n🔬 Step 2: Analyzing tonal color properties...")
        analyzer = ColorAnalyzer()
        analysis_results = analyzer.analyze(dominant_colors)
        print(f"📊 Full Analysis: {analysis_results}")

        # 3. Suggest a personalized color palette using the Tonal model
        print("\n🎨 Step 3: Generating personalized Tonal palette...")
        suggester = PaletteSuggester()
        final_palette = suggester.get_palette(analysis_results)
        
        print("\n✨ --- Your Personalized Color Analysis --- ✨")
        print(f"Primary Tonal Type: {analysis_results['tonal_type']}")
        print(f"Refined Seasonal Palette: {final_palette['season']}")
        print(f"\nDescription: {final_palette['description']}")
        print("\nRecommended Palette:")
        print(json.dumps(final_palette, indent=2, sort_keys=False))

    except (FileNotFoundError, ValueError, KeyError) as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform advanced seasonal color analysis on a facial image.")
    parser.add_argument("--image", type=str, required=True, help="Path to the input image.")
    args = parser.parse_args()
    
    main(args.image)