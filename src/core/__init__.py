"""
Core System Components

This module contains the core integration and Earth Engine components
for the AlphaEarth crop recommendation system.
"""

from .integration_bridge import UltraIntegrationBridge, CropRecommendationRequest
from .earth_engine_integration import AlphaEarthFeatureExtractor

__all__ = [
    'UltraIntegrationBridge',
    'CropRecommendationRequest',
    'AlphaEarthFeatureExtractor'
]