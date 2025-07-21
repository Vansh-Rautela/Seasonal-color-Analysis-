# Advanced Seasonal Color Analysis

An AI-powered tool that performs a sophisticated analysis of facial features to suggest highly accurate and personalized color palettes. This upgraded model goes beyond basic rules, integrating advanced color theory, lighting correction, and tonal analysis to provide expert-level recommendations for clothing, makeup, and accessories.

## ✨ Upgraded Features

- **Lighting-Independent Analysis**: Implements a **Grey World** algorithm to neutralize color casts from ambient light, ensuring a true reading of skin tone.
- **High-Accuracy Feature Extraction**: Uses a **6-point skin sampling method** inspired by academic research, with outlier removal to find the most representative skin, hair, and eye colors.
- **Advanced Tonal Classification**: Determines your primary color characteristic (**Light, Deep, Warm, Cool, Clear, or Soft**) for a more personalized and accurate result than the rigid 12-season model.
- **Comprehensive 12-Season Palettes**: Includes a full database of the 12 seasonal archetypes for nuanced and detailed color suggestions.

## 🚀 How to Use

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Vansh-Rautela/Seasonal-color-Analysis-.git](https://github.com/Vansh-Rautela/Seasonal-color-Analysis-.git)
    cd Seasonal-color-Analysis-
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the analysis:**
    ```bash
    python main.py --image path/to/your/image.jpg
    ```