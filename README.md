# Seasonal Color Analysis

A Python-based tool that analyzes facial features and suggests personalized color palettes based on seasonal color theory. The application helps users discover their most flattering colors for clothing, makeup, and accessories.

## 🌟 Features

- **Facial Feature Extraction**: Automatically detects and analyzes facial features
- **Color Analysis**: Determines skin undertones, brightness, and contrast levels
- **Personalized Palette**: Suggests colors that complement your natural features
- **Seasonal Analysis**: Categorizes users into seasonal color palettes (Spring, Summer, Autumn, Winter)

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Vansh-Rautela/Seasonal-color-Analysis-.git
   cd Seasonal-color-Analysis-
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the analysis on an image:
```bash
python main.py --image path/to/your/image.jpg
```

### Example:
```bash
python main.py --image photo.jpg
```

## 🏗️ Project Structure

```
Seasonal-color-Analysis/
├── analysis/               # Facial feature extraction and analysis
│   ├── __init__.py
│   ├── color_analyzer.py   # Color analysis logic
│   └── feature_extractor.py # Feature extraction from images
├── palette/                # Color palette management
│   ├── __init__.py
│   ├── palettes.json       # Color palette definitions
│   └── suggester.py        # Palette suggestion logic
├── utils/                  # Utility functions
│   ├── __init__.py
│   └── color_utils.py      # Color manipulation utilities
├── main.py                 # Main application entry point
└── requirements.txt        # Project dependencies
```

## 📋 Requirements

- Python 3.7+
- OpenCV
- NumPy
- Pillow
- scikit-learn
- Matplotlib
- MediaPipe

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📬 Contact

For any questions or feedback, please open an issue on GitHub.
