"""
Simplified Feature Mapper
"""

import numpy as np
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class FeatureMapper:
    """
    Simplified feature mapper
    """
    
    def __init__(self):
        """Initialize the mapper"""
        # Feature ranges from original dataset
        self.feature_ranges = {
            'nitrogen': {'min': 0, 'max': 140, 'mean': 50.55},
            'phosphorus': {'min': 5, 'max': 145, 'mean': 53.36},
            'potassium': {'min': 5, 'max': 205, 'mean': 48.15},
            'temperature': {'min': 8.8, 'max': 43.7, 'mean': 25.62},
            'humidity': {'min': 14.3, 'max': 99.9, 'mean': 71.48},
            'ph': {'min': 3.5, 'max': 9.9, 'mean': 6.47},
            'rainfall': {'min': 20.2, 'max': 298.6, 'mean': 103.46}
        }
        logger.info("FeatureMapper initialized")
    
    def map_to_agricultural_features(self, 
                                   processed_embeddings: Dict[str, np.ndarray],
                                   latitude: float = 0,
                                   longitude: float = 0,
                                   year: int = 2024) -> Dict[str, float]:
        """
        Map processed embeddings to agricultural features
        
        Args:
            processed_embeddings: Processed embedding features
            latitude: Latitude for geographic context
            longitude: Longitude for geographic context
            year: Year for temporal context
            
        Returns:
            Dictionary with agricultural features
        """
        # Simple mapping based on embedding statistics
        mean_val = processed_embeddings.get('mean', np.array([0]))[0]
        std_val = processed_embeddings.get('std', np.array([0]))[0]
        energy_val = processed_embeddings.get('energy', np.array([0]))[0]
        
        # Map to agricultural features with geographic adjustments
        features = {}
        
        # Base values from embedding statistics
        for feature, ranges in self.feature_ranges.items():
            base_value = ranges['mean']
            
            # Add variation based on embedding characteristics
            variation = mean_val * 50 + std_val * 30
            
            # Geographic adjustments
            if abs(latitude) > 40:  # Higher latitudes
                if feature == 'temperature':
                    variation -= 5
                elif feature == 'humidity':
                    variation += 10
            
            if abs(latitude) < 20:  # Tropical regions
                if feature == 'temperature':
                    variation += 8
                elif feature == 'rainfall':
                    variation += 50
            
            # Apply variation and clamp to valid range
            final_value = base_value + variation
            final_value = max(ranges['min'], min(ranges['max'], final_value))
            
            features[feature] = float(final_value)
        
        return features