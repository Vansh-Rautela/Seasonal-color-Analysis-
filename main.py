import argparse
import json
from analysis.feature_extractor import FacialFeatureExtractor
from analysis.color_analyzer import ColorAnalyzer
from palette.suggester import PaletteSuggester

def main(image_path):
    """
    Main pipeline to run the seasonal color analysis.
    """
    try:
        # 1. Extract facial features and dominant colors
        print("🔍 Step 1: Extracting facial features...")
        extractor = FacialFeatureExtractor()
        dominant_colors = extractor.extract_features(image_path)
        print(f"🎨 Dominant colors found: {dominant_colors}")

        # 2. Analyze colors for undertone, brightness, contrast
        print("\n🔬 Step 2: Analyzing color properties...")
        analyzer = ColorAnalyzer()
        analysis_results = analyzer.analyze(dominant_colors)
        print(f"📊 Analysis results: {analysis_results}")

        # 3. Suggest a personalized color palette
        print("\n🎨 Step 3: Generating personalized palette...")
        suggester = PaletteSuggester()
        final_palette = suggester.get_palette(analysis_results)
        
        print("\n✨ --- Your Personalized Color Analysis --- ✨")
        print(f"Season: {final_palette['season']}")
        print(f"Description: {final_palette['description']}")
        print("\nRecommended Palette:")
        # Pretty print the final JSON result
        print(json.dumps(final_palette, indent=2))

    except (FileNotFoundError, ValueError, KeyError) as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform seasonal color analysis on a facial image.")
    parser.add_argument("--image", type=str, required=True, help="Path to the input image.")
    args = parser.parse_args()
    
    main(args.image)