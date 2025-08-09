"""
Simplified AlphaEarth Extractor that works with existing Earth Engine integration
"""

import numpy as np
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class AlphaEarthExtractor:
    """
    Simplified AlphaEarth extractor that uses our existing Earth Engine integration
    """
    
    def __init__(self, service_account_key: Optional[str] = None, project_id: Optional[str] = None):
        """Initialize the extractor"""
        self.service_account_key = service_account_key
        self.project_id = project_id
        
        # Try to import and use our existing Earth Engine integration
        try:
            from core.earth_engine_integration import AlphaEarthFeatureExtractor
            self.ee_extractor = AlphaEarthFeatureExtractor(
                service_account_key=service_account_key,
                project_id=project_id
            )
            self.use_real_ee = True
            logger.info(f"Using real Earth Engine integration (project: {project_id})")
        except Exception as e:
            logger.warning(f"Earth Engine not available, using mock: {e}")
            try:
                import sys
                from pathlib import Path
                # Add tests to path for mock fallback
                tests_path = Path(__file__).parent.parent.parent / "tests"
                if str(tests_path) not in sys.path:
                    sys.path.append(str(tests_path))
                from test_with_mock_ee import MockAlphaEarthFeatureExtractor
                self.ee_extractor = MockAlphaEarthFeatureExtractor()
                self.use_real_ee = False
            except ImportError:
                # Fallback if test module not available
                logger.error("No fallback extractor available")
                raise e
    
    def extract_agricultural_features(self, 
                                    latitude: float, 
                                    longitude: float, 
                                    year: int = 2024) -> Dict[str, float]:
        """
        Extract agricultural features from satellite data
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            year: Year for analysis
            
        Returns:
            Dictionary with agricultural features
        """
        try:
            # Use our existing extractor
            features = self.ee_extractor.extract_agricultural_features(
                latitude, longitude, year
            )
            
            logger.info(f"Extracted features for ({latitude}, {longitude})")
            return features
            
        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")
            # Return default features as fallback
            # return {
            # #     'nitrogen': 50.0,
            # #     'phosphorus': 53.0,
            # #     'potassium': 48.0,
            # #     'temperature': 25.6,
            # #     'humidity': 71.5,
            # #     'ph': 6.47,
            # #     'rainfall': 103.5
            # # }
    
    def extract_embedding_vector(self, 
                                latitude: float, 
                                longitude: float, 
                                year: int = 2024) -> np.ndarray:
        """
        Extract 64-dimensional embedding vector (simulated for now)
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            year: Year for analysis
            
        Returns:
            64-dimensional numpy array
        """
        # For now, return a simulated embedding vector
        # In a real implementation, this would extract actual AlphaEarth embeddings
        np.random.seed(int(abs(latitude * longitude * 1000)) % 2**32)
        embedding = np.random.normal(0, 0.3, 64)
        
        # Normalize to unit length (as AlphaEarth embeddings are)
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def get_dataset_info(self) -> Dict:
        """Get information about the dataset"""
        return {
            'dataset_id': 'GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL',
            'embedding_dimensions': 64,
            'available_years': [2022, 2023, 2024],
            'extractor_type': 'real' if self.use_real_ee else 'mock'
        }