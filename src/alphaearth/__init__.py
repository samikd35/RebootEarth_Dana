"""
AlphaEarth module for Google Satellite Embedding integration
"""

from .alpha_earth_extractor import AlphaEarthExtractor
from .embedding_processor import EmbeddingProcessor
from .feature_mapper import FeatureMapper

__version__ = "1.0.0"
__all__ = ["AlphaEarthExtractor", "EmbeddingProcessor", "FeatureMapper"]