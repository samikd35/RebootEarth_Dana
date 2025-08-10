#!/usr/bin/env python3
"""
Analysis Results Manager
Handles saving and retrieving crop analysis results for SMS sending
"""

import os
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json

logger = logging.getLogger(__name__)

@dataclass
class SavedAnalysisResult:
    """Saved analysis result structure"""
    id: str
    timestamp: str
    location_name: str
    latitude: float
    longitude: float
    recommended_crop: str
    confidence_score: float
    satellite_features: Dict[str, float]
    region_info: Dict[str, str]
    farmer_advice_english: Optional[str] = None
    farmer_advice_amharic: Optional[str] = None
    farmer_advice_afaan_oromo: Optional[str] = None
    alternative_crops: List[tuple] = None
    processing_time_ms: float = 0
    
    def __post_init__(self):
        if self.alternative_crops is None:
            self.alternative_crops = []

class AnalysisResultsManager:
    """
    Manages saved analysis results for SMS sending
    """
    
    def __init__(self, data_file: str = "data/saved_analysis_results.json"):
        """Initialize analysis results manager"""
        self.data_file = data_file
        self.results: Dict[str, SavedAnalysisResult] = {}
        self._ensure_data_directory()
        self._load_results()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def _load_results(self):
        """Load saved analysis results from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Convert dict data back to SavedAnalysisResult objects
                for result_id, result_data in data.items():
                    self.results[result_id] = SavedAnalysisResult(**result_data)
                    
                logger.info(f"Loaded {len(self.results)} saved analysis results")
            else:
                logger.info("No existing analysis results file found, starting fresh")
                
        except Exception as e:
            logger.error(f"Failed to load analysis results: {e}")
            self.results = {}
    
    def _save_results(self):
        """Save analysis results to JSON file"""
        try:
            # Convert SavedAnalysisResult objects to dict for JSON serialization
            data = {}
            for result_id, result in self.results.items():
                data[result_id] = asdict(result)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info("Analysis results saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save analysis results: {e}")
    
    def save_analysis_result(self, response, location_name: str = None) -> str:
        """
        Save an analysis result from a CropRecommendationResponse
        
        Args:
            response: CropRecommendationResponse object
            location_name: Optional custom location name
            
        Returns:
            The ID of the saved result
        """
        try:
            # Generate unique ID
            timestamp = datetime.now()
            result_id = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{response.coordinates['latitude']:.4f}_{response.coordinates['longitude']:.4f}"
            
            # Create location name if not provided
            if not location_name:
                location_name = f"{response.coordinates['latitude']:.4f}, {response.coordinates['longitude']:.4f}"
            
            # Create saved result
            saved_result = SavedAnalysisResult(
                id=result_id,
                timestamp=timestamp.isoformat(),
                location_name=location_name,
                latitude=response.coordinates['latitude'],
                longitude=response.coordinates['longitude'],
                recommended_crop=response.recommended_crop,
                confidence_score=response.confidence_score,
                satellite_features=response.satellite_features,
                region_info=response.region_info,
                farmer_advice_english=response.farmer_advice,
                farmer_advice_amharic=response.farmer_advice_amharic,
                farmer_advice_afaan_oromo=response.farmer_advice_afaan_oromo,
                alternative_crops=response.alternative_crops or [],
                processing_time_ms=response.processing_time_ms
            )
            
            # Save to memory and file
            self.results[result_id] = saved_result
            self._save_results()
            
            logger.info(f"Saved analysis result: {result_id} for {location_name}")
            return result_id
            
        except Exception as e:
            logger.error(f"Failed to save analysis result: {e}")
            return None
    
    def get_all_results(self) -> Dict[str, SavedAnalysisResult]:
        """Get all saved analysis results"""
        return self.results
    
    def get_result_by_id(self, result_id: str) -> Optional[SavedAnalysisResult]:
        """Get a specific analysis result by ID"""
        return self.results.get(result_id)
    
    def delete_result(self, result_id: str) -> bool:
        """Delete a saved analysis result"""
        try:
            if result_id in self.results:
                del self.results[result_id]
                self._save_results()
                logger.info(f"Deleted analysis result: {result_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete analysis result: {e}")
            return False
    
    def get_results_summary(self) -> Dict[str, int]:
        """Get summary statistics of saved results"""
        total_results = len(self.results)
        crops_count = {}
        
        for result in self.results.values():
            crop = result.recommended_crop
            crops_count[crop] = crops_count.get(crop, 0) + 1
        
        return {
            'total_results': total_results,
            'unique_crops': len(crops_count),
            'crops_breakdown': crops_count
        }

# Global instance
analysis_results_manager = AnalysisResultsManager()

if __name__ == "__main__":
    # Test the analysis results manager
    print("🔧 Testing Analysis Results Manager...")
    
    # Create a mock result for testing
    from dataclasses import dataclass
    from typing import Dict, Any
    
    @dataclass
    class MockResponse:
        coordinates: Dict[str, float]
        recommended_crop: str
        confidence_score: float
        satellite_features: Dict[str, float]
        region_info: Dict[str, str]
        farmer_advice: str
        farmer_advice_amharic: str
        farmer_advice_afaan_oromo: str
        alternative_crops: List[tuple]
        processing_time_ms: float
    
    mock_response = MockResponse(
        coordinates={'latitude': 9.0320, 'longitude': 38.7469},
        recommended_crop='Maize',
        confidence_score=0.85,
        satellite_features={
            'nitrogen': 45.2, 'phosphorus': 38.7, 'potassium': 42.1,
            'temperature': 28.5, 'humidity': 75.3, 'ph': 6.2, 'rainfall': 120.8
        },
        region_info={'climate_zone': 'tropical'},
        farmer_advice='Test advice in English',
        farmer_advice_amharic='Test advice in Amharic',
        farmer_advice_afaan_oromo='Test advice in Afaan Oromo',
        alternative_crops=[('Rice', 78.2), ('Banana', 72.1)],
        processing_time_ms=1500.0
    )
    
    # Test saving
    result_id = analysis_results_manager.save_analysis_result(mock_response, "Test Location - Addis Ababa")
    print(f"Saved result with ID: {result_id}")
    
    # Test retrieval
    saved_result = analysis_results_manager.get_result_by_id(result_id)
    if saved_result:
        print(f"Retrieved result: {saved_result.location_name} - {saved_result.recommended_crop}")
    
    # Test summary
    summary = analysis_results_manager.get_results_summary()
    print(f"Summary: {summary}")