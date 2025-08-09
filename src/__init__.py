"""
AlphaEarth Crop Recommender - Source Package

This package contains the core functionality for the AlphaEarth-based
crop recommendation system.
"""

__version__ = "1.0.0"
__author__ = "AlphaEarth Team"

# Make core components easily accessible
from .core.integration_bridge import UltraIntegrationBridge, CropRecommendationRequest
from .features.advanced_feature_extractor import AdvancedFeatureExtractor
from .features.ensemble_crop_predictor import EnsembleCropPredictor

__all__ = [
    'UltraIntegrationBridge',
    'CropRecommendationRequest', 
    'AdvancedFeatureExtractor',
    'EnsembleCropPredictor'
]