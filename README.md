# 🌾 AlphaEarth Crop Recommender

An advanced crop recommendation system that combines **Google Earth Engine's AlphaEarth satellite embeddings** with **machine learning** to provide intelligent, location-specific crop recommendations.

## 🚀 Features

- **🛰️ Real Satellite Data**: Uses Google's AlphaEarth 64-dimensional satellite embeddings
- **🌍 Global Coverage**: Works anywhere on Earth with satellite coverage  
- **🤖 Advanced ML**: Ensemble prediction with uncertainty quantification
- **⚡ Fast Processing**: Optimized for real-time recommendations
- **🌐 Web Interface**: Interactive map-based interface
- **📊 Rich Analytics**: Confidence scores, alternatives, and regional suitability
- **🤖 AI Agricultural Advisor**: LLM-powered farmer-friendly explanations (NEW!)
- **🌾 Alternative Crops**: Top 3 alternative crop recommendations with confidence scores
- **👨‍🌾 Farmer-Friendly Language**: Simple, actionable advice in plain language

## 🏗️ Project Structure

```
📁 alphaearth-crop-recommender/
├── 📁 src/                          # Source code
│   ├── 📁 core/                     # Core system components
│   │   ├── integration_bridge.py   # Main integration logic
│   │   └── earth_engine_integration.py # Satellite data extraction
│   ├── 📁 features/                 # Advanced feature extraction
│   │   ├── advanced_feature_extractor.py # Next-gen features
│   │   └── ensemble_crop_predictor.py # Advanced ML
│   ├── 📁 alphaearth/              # AlphaEarth satellite processing
│   └── 📁 web/                     # Web application
│       └── app_ultra_integrated.py # Flask web app
├── 📁 models/                      # ML models and training data
│   ├── model.pkl                   # Trained model
│   ├── minmaxscaler_fixed.pkl     # Feature scalers
│   └── Crop_recommendation.csv    # Training data
├── 📁 scripts/                     # Setup and utility scripts
├── 📁 tests/                       # Tests and demos
├── 📁 docs/                        # Documentation
├── launch.py                       # 🚀 Main launcher
├── setup.py                        # Setup script
└── requirements.txt                # Dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Earth Engine Authentication
```bash
python setup.py
```

### 3. Configure Azure OpenAI (Optional - for AI Agricultural Advisor)
Create a `.env` file with your Azure OpenAI credentials:
```bash
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt41
GOOGLE_CLOUD_PROJECT=your-project-id
```

### 4. Launch the System
```bash
python run.py
```
*Alternative: `python launch.py`*

### 5. Open Your Browser
The system will automatically open at `http://localhost:5001`

## 🧪 Testing & Demo

### Run Tests
```bash
python test.py
```

### Run Interactive Demo
```bash
python demo.py
```

## 🌍 How It Works

### 1. **Satellite Data Extraction**
- Connects to Google Earth Engine
- Extracts AlphaEarth 64-dimensional embeddings
- Processes real satellite imagery data

### 2. **Feature Engineering**
- Converts satellite embeddings to agricultural features
- Extracts spectral indices (NDVI, EVI, SAVI)
- Analyzes temporal patterns and spatial context

### 3. **ML Prediction**
- Uses ensemble of Random Forest, Gradient Boosting, and Neural Networks
- Provides uncertainty quantification
- Suggests alternative crops with confidence scores

### 4. **Regional Adaptation**
- Climate zone classification (tropical, temperate, arid)
- Region-specific crop suitability matrices
- Local agricultural knowledge integration

## 📊 Supported Crops

The system can recommend from 22 different crops:
- **Cereals**: Rice, Maize, Wheat, Barley
- **Legumes**: Chickpea, Lentil, Blackgram, Mungbean
- **Fruits**: Apple, Orange, Mango, Banana, Grapes
- **Cash Crops**: Cotton, Coffee, Jute
- **And more**: Coconut, Papaya, Pomegranate, etc.

## 🌐 Web Interface

### Interactive Features
- **🗺️ World Map**: Click anywhere to get crop recommendations
- **📍 Coordinate Input**: Enter specific latitude/longitude
- **📊 Rich Results**: Confidence scores, alternatives, regional suitability
- **🔍 Detailed Analysis**: Spectral indices, temporal patterns, uncertainty metrics

### API Endpoints
- `GET /` - Main web interface
- `POST /api/recommend` - Crop recommendation API
- `GET /api/health` - System health check
- `GET /api/stats` - Performance statistics

## 🔧 Configuration

### Environment Variables
```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
```

### Google Earth Engine Setup
1. Create a Google Cloud Project
2. Enable Earth Engine API
3. Run authentication: `earthengine authenticate`
4. Register project for Earth Engine access

## 🧪 Development

### Project Structure
- **`src/core/`**: Core integration and Earth Engine components
- **`src/features/`**: Advanced feature extraction and ML models
- **`src/alphaearth/`**: AlphaEarth satellite processing modules
- **`src/web/`**: Flask web application and templates
- **`models/`**: Trained ML models and training data
- **`tests/`**: Test suites, demos, and verification scripts

### Adding New Features
1. Add feature extractors to `src/features/`
2. Update integration in `src/core/integration_bridge.py`
3. Add tests to `tests/`
4. Update documentation

## 📈 Performance

- **Processing Time**: 2-5 seconds per prediction
- **Accuracy**: 85%+ validated accuracy
- **Coverage**: Global satellite coverage
- **Confidence**: 70-90% average confidence scores

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Earth Engine** for AlphaEarth satellite embeddings
- **Scikit-learn** for machine learning algorithms
- **Flask** for web framework
- **Agricultural research community** for domain knowledge

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Check the documentation in `docs/`
- Run `python test.py` for system verification

---

**🌾 Empowering agriculture with satellite intelligence and AI! 🚀**