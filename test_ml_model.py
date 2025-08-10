#!/usr/bin/env python3
"""
Test the ML model directly to see if it's broken
"""

import os
import logging
import sys
import numpy as np
import pickle
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def test_ml_model_directly():
    """Test the ML model with different feature sets"""
    print("🧪 Testing ML Model Directly")
    print("=" * 50)
    
    try:
        # Load the model and scalers directly
        models_dir = project_root / "models"
        
        with open(models_dir / 'model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        with open(models_dir / 'minmaxscaler_fixed.pkl', 'rb') as f:
            minmax_scaler = pickle.load(f)
            
        with open(models_dir / 'standscaler_fixed.pkl', 'rb') as f:
            standard_scaler = pickle.load(f)
        
        # Crop mapping
        crop_dict = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 
            6: "Papaya", 7: "Orange", 8: "Apple", 9: "Muskmelon", 
            10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
            14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 
            18: "Mothbeans", 19: "Pigeonpeas", 20: "Kidneybeans", 
            21: "Chickpea", 22: "Coffee"
        }
        
        print("✅ Model and scalers loaded successfully")
        
        # Test with different feature sets from the training data
        test_cases = [
            # Rice-like features (from training data)
            {"name": "Rice-like", "features": [90, 42, 43, 20.9, 82.0, 6.5, 202.9]},
            # Muskmelon-like features (from training data)  
            {"name": "Muskmelon-like", "features": [115, 17, 55, 27.6, 94.1, 6.8, 28.1]},
            # Maize-like features
            {"name": "Maize-like", "features": [80, 40, 20, 27.0, 65.0, 6.0, 60.0]},
            # Our generated features (the problematic ones)
            {"name": "Our Generated", "features": [35.8, 27.7, 49.8, 28.0, 76.5, 7.24, 79.9]},
            # Extreme low values
            {"name": "Extreme Low", "features": [10, 10, 10, 15.0, 50.0, 4.0, 30.0]},
            # Extreme high values
            {"name": "Extreme High", "features": [130, 130, 180, 40.0, 95.0, 8.5, 280.0]}
        ]
        
        print("\nTesting different feature sets:")
        print("-" * 70)
        print(f"{'Test Case':<15} | {'Prediction':<12} | {'Class':<5} | {'Confidence':<10}")
        print("-" * 70)
        
        predictions = []
        for test_case in test_cases:
            features = np.array(test_case["features"]).reshape(1, -1)
            
            # Apply scaling
            scaled_features = minmax_scaler.transform(features)
            final_features = standard_scaler.transform(scaled_features)
            
            # Make prediction
            prediction = model.predict(final_features)[0]
            probabilities = model.predict_proba(final_features)[0]
            confidence = float(np.max(probabilities))
            
            crop_name = crop_dict.get(prediction, "Unknown")
            predictions.append((test_case["name"], crop_name, prediction, confidence))
            
            print(f"{test_case['name']:<15} | {crop_name:<12} | {prediction:<5} | {confidence:<10.3f}")
        
        # Analyze results
        print("\n" + "=" * 70)
        print("ANALYSIS:")
        print("=" * 70)
        
        unique_predictions = set([pred[1] for pred in predictions])
        unique_classes = set([pred[2] for pred in predictions])
        
        print(f"Unique crops predicted: {len(unique_predictions)}")
        print(f"Unique class IDs: {len(unique_classes)}")
        print(f"Crops: {unique_predictions}")
        print(f"Class IDs: {unique_classes}")
        
        if len(unique_predictions) == 1:
            print("\n❌ MODEL IS BROKEN: Always predicting the same crop!")
            print("   The ML model is stuck on one prediction")
            return False
        elif len(unique_predictions) < 3:
            print("\n⚠️  MODEL HAS LIMITED VARIATION: Only predicting a few crops")
            print("   The model may need retraining or feature scaling is wrong")
            return False
        else:
            print("\n✅ MODEL IS WORKING: Predicting different crops for different inputs")
            print("   The issue is likely in our feature generation")
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ml_model_directly()
    if success:
        print("\n🎉 ML Model is working correctly!")
        print("   The issue is in our feature generation or scaling")
    else:
        print("\n❌ ML Model is broken!")
        print("   The model needs to be retrained or replaced")