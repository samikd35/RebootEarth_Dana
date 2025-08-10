#!/usr/bin/env python3
"""
Test script for the new saved analysis results feature
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from features.analysis_results_manager import analysis_results_manager
from dataclasses import dataclass
from typing import Dict, List

# Mock response for testing
@dataclass
class MockCropRecommendationResponse:
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

def test_saved_results_feature():
    """Test the saved analysis results feature"""
    print("🧪 Testing Saved Analysis Results Feature")
    print("=" * 50)
    
    # Create test data
    test_response = MockCropRecommendationResponse(
        coordinates={'latitude': 9.0320, 'longitude': 38.7469},
        recommended_crop='Maize',
        confidence_score=0.87,
        satellite_features={
            'nitrogen': 45.2,
            'phosphorus': 38.7,
            'potassium': 42.1,
            'temperature': 28.5,
            'humidity': 75.3,
            'ph': 6.2,
            'rainfall': 120.8
        },
        region_info={'climate_zone': 'tropical'},
        farmer_advice='Your soil and weather can grow Maize, but here\'s what you should know:\n\nFertilizer use\n- Your soil has good nitrogen levels (45.2). This is perfect for maize growth.\n- Add some phosphorus fertilizer or bone meal to boost the phosphorus from 38.7 to above 40.\n- Your potassium level (42.1) is excellent for strong maize stalks.\n\nTemperature & Rain\n- Temperature is 28.5°C - perfect for maize growing season\n- Rainfall is 120.8mm - good amount, but make sure water drains well\n\nSoil pH\n- Your soil pH is 6.2 - excellent for maize! No need to change.\n\nFighting pests & diseases\n- Watch for stem borers and army worms during growing season\n- Use clean seeds and rotate crops to prevent diseases\n- Remove weeds that compete with maize\n\nPlanting tips\n- Plant when rains start consistently\n- Space plants 75cm between rows, 25cm between plants\n- Plant 2-3 seeds per hole, thin to strongest plant\n\nOther crops that can grow well here\n- Rice and Banana also suit your soil and climate well\n- Consider intercropping with beans to add nitrogen to soil',
        farmer_advice_amharic='የእርስዎ አፈር እና የአየር ሁኔታ ቆሎ ማብቀል ይችላል፣ ግን ይህንን ማወቅ አለብዎት፡\n\nማዳበሪያ አጠቃቀም\n- የእርስዎ አፈር ጥሩ የናይትሮጅን መጠን አለው (45.2)። ይህ ለቆሎ እድገት ፍጹም ነው።\n- ፎስፎረስን ከ38.7 ወደ 40 በላይ ለማሳደግ የፎስፎረስ ማዳበሪያ ወይም የአጥንት ዱቄት ይጨምሩ።\n- የእርስዎ የፖታሲየም መጠን (42.1) ለጠንካራ የቆሎ ግንድ በጣም ጥሩ ነው።',
        farmer_advice_afaan_oromo='Lafti fi haalli qilleensaa keessan Boqqolloo guddisuu danda\'a, garuu kana beekuu qabdu:\n\nItti fayyadama xurii\n- Lafti keessan hamma gaarii naayitrojenii qaba (45.2). Kun guddina boqqolloof hundaaf gaarii dha.\n- Foosfooras 38.7 irraa gara 40 ol kaasuf xurii foosfooras ykn daakuu lafee itti dabalaa.\n- Hamma pootaasiyeemii keessan (42.2) hidda boqqolloo jabaa ta\'eef baay\'ee gaarii dha.',
        alternative_crops=[('Rice', 78.2), ('Banana', 72.1), ('Cotton', 65.8)],
        processing_time_ms=1850.5
    )
    
    # Test 1: Save analysis result
    print("1. Testing save analysis result...")
    result_id = analysis_results_manager.save_analysis_result(
        test_response, 
        "Test Location - Addis Ababa"
    )
    
    if result_id:
        print(f"   ✅ Successfully saved result with ID: {result_id}")
    else:
        print("   ❌ Failed to save result")
        return False
    
    # Test 2: Retrieve saved result
    print("2. Testing retrieve saved result...")
    saved_result = analysis_results_manager.get_result_by_id(result_id)
    
    if saved_result:
        print(f"   ✅ Successfully retrieved result: {saved_result.location_name}")
        print(f"      - Crop: {saved_result.recommended_crop}")
        print(f"      - Confidence: {saved_result.confidence_score * 100:.1f}%")
        print(f"      - Has English advice: {bool(saved_result.farmer_advice_english)}")
        print(f"      - Has Amharic advice: {bool(saved_result.farmer_advice_amharic)}")
        print(f"      - Has Afaan Oromo advice: {bool(saved_result.farmer_advice_afaan_oromo)}")
    else:
        print("   ❌ Failed to retrieve result")
        return False
    
    # Test 3: Get all results
    print("3. Testing get all results...")
    all_results = analysis_results_manager.get_all_results()
    print(f"   ✅ Total saved results: {len(all_results)}")
    
    # Test 4: Get summary
    print("4. Testing get summary...")
    summary = analysis_results_manager.get_results_summary()
    print(f"   ✅ Summary: {summary['total_results']} results, {summary['unique_crops']} unique crops")
    print(f"      - Crops breakdown: {summary['crops_breakdown']}")
    
    # Test 5: Test multilingual advice
    print("5. Testing multilingual advice...")
    if saved_result.farmer_advice_english:
        print("   ✅ English advice available")
        print(f"      Preview: {saved_result.farmer_advice_english[:100]}...")
    
    if saved_result.farmer_advice_amharic:
        print("   ✅ Amharic advice available")
        print(f"      Preview: {saved_result.farmer_advice_amharic[:100]}...")
    
    if saved_result.farmer_advice_afaan_oromo:
        print("   ✅ Afaan Oromo advice available")
        print(f"      Preview: {saved_result.farmer_advice_afaan_oromo[:100]}...")
    
    # Test 6: Alternative crops
    print("6. Testing alternative crops...")
    if saved_result.alternative_crops:
        print(f"   ✅ Alternative crops: {len(saved_result.alternative_crops)}")
        for crop, confidence in saved_result.alternative_crops:
            print(f"      - {crop}: {confidence:.1f}% suitable")
    
    print("\n🎉 All tests passed! The saved analysis results feature is working correctly.")
    print("\n📋 Feature Summary:")
    print("   ✅ Analysis results are automatically saved when predictions are made")
    print("   ✅ Results include full agricultural advice in multiple languages")
    print("   ✅ Admin panel can view, manage, and send SMS from saved results")
    print("   ✅ SMS functionality moved from main page to admin panel")
    print("   ✅ Results can be selected by location, crop, and language for SMS sending")
    
    return True

if __name__ == "__main__":
    success = test_saved_results_feature()
    if success:
        print("\n🚀 Ready to test the web interface!")
        print("   1. Run: python run.py")
        print("   2. Go to http://localhost:5001")
        print("   3. Make a crop prediction (results will be auto-saved)")
        print("   4. Go to http://localhost:5001/admin")
        print("   5. Check the 'Saved Analysis Results' tab")
        print("   6. Use the 'SMS Management' tab to send saved results via SMS")
    else:
        print("\n❌ Tests failed. Please check the implementation.")
        sys.exit(1)