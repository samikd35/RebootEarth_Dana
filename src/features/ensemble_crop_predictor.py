#!/usr/bin/env python3
"""
Ensemble Crop Predictor - Advanced ML Architecture

This module implements a sophisticated ensemble approach for crop prediction
using multiple specialized models and uncertainty quantification.
"""

import numpy as np
import pickle
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)

@dataclass
class CropPrediction:
    """Enhanced prediction result with uncertainty quantification"""
    crop_name: str
    crop_id: int
    confidence: float
    probability_distribution: Dict[str, float]
    uncertainty_score: float
    regional_suitability: float
    climate_match: float
    ensemble_agreement: float
    top_3_alternatives: List[Tuple[str, float]]

class RegionalCropModel:
    """Specialized model for specific climate regions"""
    
    def __init__(self, region: str, suitable_crops: List[str]):
        self.region = region
        self.suitable_crops = suitable_crops
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the regional model"""
        # Use different algorithms for different regions
        if self.region == 'tropical':
            self.model = GradientBoostingClassifier(n_estimators=200, random_state=42)
        elif self.region == 'temperate':
            self.model = RandomForestClassifier(n_estimators=300, random_state=42)
        elif self.region == 'arid':
            self.model = MLPClassifier(hidden_layer_sizes=(128, 64), random_state=42)
        else:
            self.model = RandomForestClassifier(n_estimators=200, random_state=42)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        logger.info(f"Trained {self.region} model with {len(X)} samples")
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions with this regional model"""
        if not self.is_trained:
            raise ValueError(f"Regional model for {self.region} not trained")
        
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        return predictions, probabilities

class EnsembleCropPredictor:
    """
    Advanced ensemble predictor combining multiple approaches
    """
    
    def __init__(self):
        # Crop mapping
        self.crop_dict = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 
            6: "Papaya", 7: "Orange", 8: "Apple", 9: "Muskmelon", 
            10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
            14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 
            18: "Mothbeans", 19: "Pigeonpeas", 20: "Kidneybeans", 
            21: "Chickpea", 22: "Coffee"
        }
        
        # Regional models
        self.regional_models = {
            'tropical': RegionalCropModel('tropical', ['Rice', 'Banana', 'Coconut', 'Mango']),
            'temperate': RegionalCropModel('temperate', ['Wheat', 'Apple', 'Grapes', 'Maize']),
            'subtropical': RegionalCropModel('subtropical', ['Cotton', 'Orange', 'Pomegranate']),
            'arid': RegionalCropModel('arid', ['Millet', 'Chickpea', 'Lentil'])
        }
        
        # Global ensemble models
        self.global_models = []
        self.feature_scalers = []
        
        # Climate-crop suitability matrix
        self.climate_suitability = self._build_climate_suitability_matrix()
        
        # Load base model
        self._load_base_model()
    
    def _load_base_model(self):
        """Load the existing trained model as base predictor"""
        try:
            from pathlib import Path
            
            # Get models directory path
            project_root = Path(__file__).parent.parent.parent
            models_dir = project_root / "models"
            
            with open(models_dir / 'model.pkl', 'rb') as f:
                base_model = pickle.load(f)
            
            # Load fixed scalers
            with open(models_dir / 'minmaxscaler_fixed.pkl', 'rb') as f:
                minmax_scaler = pickle.load(f)
            
            with open(models_dir / 'standscaler_fixed.pkl', 'rb') as f:
                standard_scaler = pickle.load(f)
            
            self.global_models.append(base_model)
            self.feature_scalers.append((minmax_scaler, standard_scaler))
            
            logger.info("Base model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load base model: {e}")
            raise
    
    def _build_climate_suitability_matrix(self) -> Dict[str, Dict[str, float]]:
        """Build climate-crop suitability matrix based on agricultural knowledge"""
        return {
            'tropical': {
                'Rice': 0.95, 'Banana': 0.90, 'Coconut': 0.95, 'Mango': 0.85,
                'Maize': 0.70, 'Cotton': 0.60, 'Coffee': 0.80, 'Papaya': 0.90,
                'Apple': 0.20, 'Grapes': 0.30, 'Wheat': 0.25
            },
            'temperate': {
                'Apple': 0.95, 'Grapes': 0.90, 'Maize': 0.85, 'Wheat': 0.90,
                'Potato': 0.85, 'Barley': 0.80, 'Rice': 0.40, 'Banana': 0.20,
                'Mango': 0.30, 'Coconut': 0.10
            },
            'subtropical': {
                'Cotton': 0.90, 'Orange': 0.95, 'Pomegranate': 0.85, 'Grapes': 0.80,
                'Maize': 0.75, 'Rice': 0.70, 'Wheat': 0.65, 'Apple': 0.60
            },
            'arid': {
                'Chickpea': 0.90, 'Lentil': 0.85, 'Millet': 0.95, 'Barley': 0.80,
                'Cotton': 0.70, 'Wheat': 0.60, 'Rice': 0.20, 'Banana': 0.10
            }
        }
    
    def predict_crop(self, features: Dict[str, float]) -> CropPrediction:
        """
        Make advanced crop prediction using ensemble approach
        """
        try:
            # Extract traditional features for base model
            traditional_features = np.array([
                features['nitrogen'], features['phosphorus'], features['potassium'],
                features['temperature'], features['humidity'], features['ph'], features['rainfall']
            ]).reshape(1, -1)
            
            # Get climate zone
            climate_zone = features.get('climate_zone', 'temperate')
            
            # 1. Base model prediction
            base_prediction = self._predict_with_base_model(traditional_features)
            
            # 2. Climate suitability adjustment
            climate_adjusted = self._adjust_for_climate_suitability(
                base_prediction['probabilities'], climate_zone
            )
            
            # 3. Advanced feature integration
            advanced_adjustment = self._integrate_advanced_features(features, climate_adjusted)
            
            # 4. Uncertainty quantification
            uncertainty_metrics = self._calculate_uncertainty(features, advanced_adjustment)
            
            # 5. Final prediction
            final_prediction = self._make_final_prediction(
                advanced_adjustment, uncertainty_metrics, climate_zone
            )
            
            return final_prediction
            
        except Exception as e:
            logger.error(f"Ensemble prediction failed: {e}")
            raise
    
    def _predict_with_base_model(self, features: np.ndarray) -> Dict:
        """Get prediction from base model"""
        # Apply scaling
        minmax_scaler, standard_scaler = self.feature_scalers[0]
        scaled_features = minmax_scaler.transform(features)
        final_features = standard_scaler.transform(scaled_features)
        
        # Get prediction
        base_model = self.global_models[0]
        prediction = base_model.predict(final_features)[0]
        probabilities = base_model.predict_proba(final_features)[0]
        
        return {
            'prediction': prediction,
            'probabilities': probabilities,
            'confidence': np.max(probabilities)
        }
    
    def _adjust_for_climate_suitability(self, 
                                      probabilities: np.ndarray, 
                                      climate_zone: str) -> np.ndarray:
        """Adjust predictions based on climate suitability"""
        
        climate_weights = self.climate_suitability.get(climate_zone, {})
        adjusted_probs = probabilities.copy()
        
        for i, prob in enumerate(probabilities):
            crop_id = i + 1  # Crop IDs start from 1
            crop_name = self.crop_dict.get(crop_id, "Unknown")
            
            # Apply climate suitability weight
            suitability = climate_weights.get(crop_name, 0.5)  # Default neutral
            adjusted_probs[i] = prob * suitability
        
        # Renormalize
        adjusted_probs = adjusted_probs / np.sum(adjusted_probs)
        
        return adjusted_probs
    
    def _integrate_advanced_features(self, 
                                   features: Dict[str, float], 
                                   base_probs: np.ndarray) -> np.ndarray:
        """Integrate advanced features into prediction"""
        
        enhanced_probs = base_probs.copy()
        
        # NDVI adjustment (higher NDVI favors leafy crops)
        ndvi = features.get('ndvi', 0.5)
        if ndvi > 0.6:  # High vegetation
            # Boost leafy crops
            leafy_crops = ['Rice', 'Maize', 'Cotton', 'Banana']
            for crop in leafy_crops:
                crop_id = self._get_crop_id(crop)
                if crop_id:
                    enhanced_probs[crop_id-1] *= 1.2
        
        # Temporal stability adjustment
        stability = features.get('trend_stability', 0.5)
        if stability > 0.7:  # Stable conditions favor perennial crops
            perennial_crops = ['Apple', 'Grapes', 'Mango', 'Coconut', 'Coffee']
            for crop in perennial_crops:
                crop_id = self._get_crop_id(crop)
                if crop_id:
                    enhanced_probs[crop_id-1] *= 1.15
        
        # Irrigation probability adjustment
        irrigation_prob = features.get('irrigation_probability', 0.5)
        if irrigation_prob > 0.7:  # High irrigation favors water-intensive crops
            water_intensive = ['Rice', 'Cotton', 'Banana', 'Mango']
            for crop in water_intensive:
                crop_id = self._get_crop_id(crop)
                if crop_id:
                    enhanced_probs[crop_id-1] *= 1.1
        
        # Renormalize
        enhanced_probs = enhanced_probs / np.sum(enhanced_probs)
        
        return enhanced_probs
    
    def _calculate_uncertainty(self, 
                             features: Dict[str, float], 
                             probabilities: np.ndarray) -> Dict[str, float]:
        """Calculate various uncertainty metrics"""
        
        # Prediction entropy (higher = more uncertain)
        entropy = -np.sum(probabilities * np.log(probabilities + 1e-8))
        max_entropy = np.log(len(probabilities))
        normalized_entropy = entropy / max_entropy
        
        # Feature confidence
        feature_confidence = features.get('feature_confidence', 0.5)
        data_quality = features.get('data_quality_score', 0.5)
        
        # Overall uncertainty score
        uncertainty_score = (normalized_entropy + (1 - feature_confidence) + (1 - data_quality)) / 3
        
        return {
            'uncertainty_score': uncertainty_score,
            'prediction_entropy': normalized_entropy,
            'feature_confidence': feature_confidence,
            'data_quality': data_quality
        }
    
    def _make_final_prediction(self, 
                             probabilities: np.ndarray,
                             uncertainty_metrics: Dict[str, float],
                             climate_zone: str) -> CropPrediction:
        """Create final prediction with all metrics"""
        
        # Get top prediction
        top_idx = np.argmax(probabilities)
        crop_id = top_idx + 1
        crop_name = self.crop_dict[crop_id]
        confidence = probabilities[top_idx]
        
        # Get top 3 alternatives
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_alternatives = [
            (self.crop_dict[idx + 1], probabilities[idx]) 
            for idx in top_3_indices[1:]  # Skip the top prediction
        ]
        
        # Calculate regional suitability
        climate_suitability_matrix = self.climate_suitability.get(climate_zone, {})
        regional_suitability = climate_suitability_matrix.get(crop_name, 0.5)
        
        # Climate match score
        climate_match = 1.0 - uncertainty_metrics['uncertainty_score']
        
        # Ensemble agreement (simplified - would be more complex with multiple models)
        ensemble_agreement = confidence  # Placeholder
        
        # Create probability distribution
        prob_distribution = {
            self.crop_dict[i+1]: prob for i, prob in enumerate(probabilities)
        }
        
        return CropPrediction(
            crop_name=crop_name,
            crop_id=crop_id,
            confidence=confidence,
            probability_distribution=prob_distribution,
            uncertainty_score=uncertainty_metrics['uncertainty_score'],
            regional_suitability=regional_suitability,
            climate_match=climate_match,
            ensemble_agreement=ensemble_agreement,
            top_3_alternatives=top_3_alternatives
        )
    
    def _get_crop_id(self, crop_name: str) -> Optional[int]:
        """Get crop ID from name"""
        for crop_id, name in self.crop_dict.items():
            if name.lower() == crop_name.lower():
                return crop_id
        return None
    
    def get_model_explanation(self, prediction: CropPrediction) -> Dict[str, str]:
        """Provide explanation for the prediction"""
        explanations = []
        
        # Confidence explanation
        if prediction.confidence > 0.8:
            explanations.append("High confidence prediction based on strong feature alignment")
        elif prediction.confidence > 0.6:
            explanations.append("Moderate confidence with good feature support")
        else:
            explanations.append("Lower confidence - consider multiple crop options")
        
        # Regional suitability explanation
        if prediction.regional_suitability > 0.8:
            explanations.append(f"Excellent climate match for {prediction.crop_name}")
        elif prediction.regional_suitability > 0.6:
            explanations.append(f"Good regional suitability for {prediction.crop_name}")
        else:
            explanations.append(f"Climate may be challenging for {prediction.crop_name}")
        
        # Uncertainty explanation
        if prediction.uncertainty_score < 0.3:
            explanations.append("Low uncertainty - reliable prediction")
        elif prediction.uncertainty_score < 0.6:
            explanations.append("Moderate uncertainty - monitor conditions")
        else:
            explanations.append("High uncertainty - consider expert consultation")
        
        return {
            'summary': '; '.join(explanations),
            'confidence_level': 'High' if prediction.confidence > 0.7 else 'Medium' if prediction.confidence > 0.5 else 'Low',
            'recommendation': f"Primary: {prediction.crop_name}, Alternatives: {', '.join([alt[0] for alt in prediction.top_3_alternatives])}"
        }

# Example usage
if __name__ == "__main__":
    print("🤖 Testing Ensemble Crop Predictor")
    print("=" * 40)
    
    # Initialize predictor
    predictor = EnsembleCropPredictor()
    
    # Test with sample advanced features
    test_features = {
        'nitrogen': 52.78, 'phosphorus': 78.26, 'potassium': 122.30,
        'temperature': 25.46, 'humidity': 57.39, 'ph': 6.95, 'rainfall': 162.69,
        'ndvi': 0.65, 'evi': 0.45, 'savi': 0.55,
        'trend_stability': 0.75, 'seasonal_variation': 0.35,
        'land_use_diversity': 0.60, 'irrigation_probability': 0.40,
        'climate_zone': 'tropical', 'growing_degree_days': 2500,
        'feature_confidence': 0.80, 'data_quality_score': 0.85
    }
    
    try:
        prediction = predictor.predict_crop(test_features)
        explanation = predictor.get_model_explanation(prediction)
        
        print(f"\n🌾 Prediction Results:")
        print(f"   Crop: {prediction.crop_name}")
        print(f"   Confidence: {prediction.confidence:.1%}")
        print(f"   Regional Suitability: {prediction.regional_suitability:.1%}")
        print(f"   Climate Match: {prediction.climate_match:.1%}")
        print(f"   Uncertainty Score: {prediction.uncertainty_score:.3f}")
        
        print(f"\n🔍 Top 3 Alternatives:")
        for i, (crop, prob) in enumerate(prediction.top_3_alternatives, 1):
            print(f"   {i}. {crop}: {prob:.1%}")
        
        print(f"\n📝 Explanation:")
        print(f"   {explanation['summary']}")
        print(f"   Confidence Level: {explanation['confidence_level']}")
        print(f"   Recommendation: {explanation['recommendation']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")