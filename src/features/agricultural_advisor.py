#!/usr/bin/env python3
"""
Agricultural Advisor - LLM-powered farmer-friendly explanations

This module integrates Azure OpenAI GPT-4.1 to provide farmer-friendly explanations
of crop recommendations based on satellite data and soil conditions.
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class AgriculturalAdviceRequest:
    """Request structure for agricultural advice"""
    crop_name: str
    suitability_confidence: float
    nitrogen: float
    phosphorus: float
    potassium: float
    temperature: float
    humidity: float
    ph_level: float
    rainfall: float
    climate_zone: str
    alternative_crops: List[Tuple[str, float]]  # List of (crop_name, confidence) tuples

@dataclass
class AgriculturalAdviceResponse:
    """Response structure with farmer-friendly advice"""
    advice_text: str
    processing_time_ms: float
    success: bool
    advice_text_amharic: Optional[str] = None
    advice_text_afaan_oromo: Optional[str] = None
    translation_time_ms: float = 0
    translation_success: bool = False
    error_message: Optional[str] = None

class AgriculturalAdvisor:
    """
    LLM-powered agricultural advisor that provides farmer-friendly explanations
    """
    
    def __init__(self):
        """Initialize the agricultural advisor with Azure OpenAI"""
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://rootcoz.openai.azure.com/")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt41")
        
        if not self.api_key:
            logger.warning("Azure OpenAI API key not found. Agricultural advice will be unavailable.")
            self.client = None
            return
        
        try:
            # Configure the OpenAI client for Azure
            self.client = openai.AzureOpenAI(
                api_key=self.api_key,
                api_version="2023-12-01-preview",
                azure_endpoint=self.endpoint
            )
            logger.info("Agricultural Advisor initialized successfully with Azure OpenAI")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {e}")
            self.client = None
    
    def get_farmer_advice(self, request: AgriculturalAdviceRequest) -> AgriculturalAdviceResponse:
        """
        Generate farmer-friendly agricultural advice using Azure OpenAI with multi-language support
        
        Args:
            request: Agricultural advice request with crop and soil data
            
        Returns:
            AgriculturalAdviceResponse with farmer-friendly advice in multiple languages
        """
        import time
        start_time = time.time()
        
        if not self.client:
            return AgriculturalAdviceResponse(
                advice_text="Agricultural advice is currently unavailable. Please check your Azure OpenAI configuration.",
                processing_time_ms=0,
                success=False,
                error_message="Azure OpenAI client not initialized"
            )
        
        try:
            # Step 1: Generate English advice
            prompt = self._create_farmer_prompt(request)
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an experienced agricultural extension officer with deep knowledge of farming practices, soil science, and crop management. You specialize in communicating complex agricultural concepts in simple, practical terms that smallholder farmers can easily understand and implement."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7,
            )
            
            advice_text = response.choices[0].message.content.strip()
            processing_time = (time.time() - start_time) * 1000
            
            # Step 2: Translate to Amharic and Afaan Oromo
            translation_start = time.time()
            amharic_advice, afaan_oromo_advice, translation_success = self._translate_advice(advice_text)
            translation_time = (time.time() - translation_start) * 1000
            
            logger.info(f"Generated agricultural advice in {processing_time:.2f}ms, translations in {translation_time:.2f}ms")
            
            return AgriculturalAdviceResponse(
                advice_text=advice_text,
                advice_text_amharic=amharic_advice,
                advice_text_afaan_oromo=afaan_oromo_advice,
                processing_time_ms=processing_time,
                translation_time_ms=translation_time,
                success=True,
                translation_success=translation_success
            )
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            error_msg = f"Failed to generate agricultural advice: {str(e)}"
            logger.error(error_msg)
            
            return AgriculturalAdviceResponse(
                advice_text=self._get_fallback_advice(request),
                processing_time_ms=processing_time,
                success=False,
                error_message=error_msg
            )
    
    def _translate_advice(self, english_advice: str) -> tuple[Optional[str], Optional[str], bool]:
        """
        Translate English agricultural advice to Amharic and Afaan Oromo
        
        Args:
            english_advice: The English advice text to translate
            
        Returns:
            Tuple of (amharic_text, afaan_oromo_text, success_flag)
        """
        if not self.client:
            return None, None, False
            
        try:
            # Translate to Amharic
            amharic_prompt = f"""Translate the following agricultural advice from English to Amharic. 
Keep the same structure and sections. Use simple, farmer-friendly Amharic that rural farmers can understand.
Preserve the formatting with section headers and bullet points.

English text to translate:
{english_advice}

Provide only the Amharic translation, maintaining the same structure and clarity."""

            amharic_response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are a professional translator specializing in agricultural content. You translate English agricultural advice into clear, simple Amharic that Ethiopian farmers can easily understand."},
                    {"role": "user", "content": amharic_prompt}
                ],
                max_tokens=2500,
                temperature=0.3,
            )
            
            # Translate to Afaan Oromo
            afaan_oromo_prompt = f"""Translate the following agricultural advice from English to Afaan Oromo (Oromo language). 
Keep the same structure and sections. Use simple, farmer-friendly Afaan Oromo that rural farmers can understand.
Preserve the formatting with section headers and bullet points.

English text to translate:
{english_advice}

Provide only the Afaan Oromo translation, maintaining the same structure and clarity."""

            afaan_oromo_response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are a professional translator specializing in agricultural content. You translate English agricultural advice into clear, simple Afaan Oromo (Oromo language) that Ethiopian farmers can easily understand."},
                    {"role": "user", "content": afaan_oromo_prompt}
                ],
                max_tokens=2500,
                temperature=0.3,
            )
            
            amharic_text = amharic_response.choices[0].message.content.strip()
            afaan_oromo_text = afaan_oromo_response.choices[0].message.content.strip()
            
            logger.info("Successfully translated advice to Amharic and Afaan Oromo")
            return amharic_text, afaan_oromo_text, True
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return None, None, False

    def _create_farmer_prompt(self, request: AgriculturalAdviceRequest) -> str:
        """Create the farmer-friendly prompt template"""
        
        # Format alternative crops list
        alternatives_text = ""
        if request.alternative_crops:
            alternatives_list = [f"{crop} ({confidence:.1f}% suitable)" 
                               for crop, confidence in request.alternative_crops[:3]]
            alternatives_text = f"\n\nAlternative crops that could also work: {', '.join(alternatives_list)}"
        
        prompt = f"""You are an agricultural extension officer speaking to a smallholder farmer with little or no formal education.

Here is the soil, weather, and crop suitability information for the farmer's land:

Crop: {request.crop_name}
Suitability Confidence: {request.suitability_confidence:.1f}%
Nitrogen: {request.nitrogen:.1f}
Phosphorus: {request.phosphorus:.1f}
Potassium: {request.potassium:.1f}
Temperature: {request.temperature:.1f}°C
Humidity: {request.humidity:.1f}%
pH Level: {request.ph_level:.2f}
Rainfall: {request.rainfall:.1f}mm
Climate Zone: {request.climate_zone}{alternatives_text}

Your task:
- ALWAYS be positive and supportive about the recommended crop.
- The crop recommendation is GOOD for this location - reinforce this.
- Explain in very simple, farmer-friendly language.
- Avoid technical jargon.
- Use short, direct sentences.
- Give clear instructions the farmer can follow.
- Organize the advice into the following sections: Fertilizer use, Temperature & Rain, Soil pH, Fighting pests & diseases, Planting tips, Other crops that can grow well here.

Output format example:

Your soil and weather are PERFECT for growing [Crop]! Here's how to get the best results:

Fertilizer use
- Simple advice based on Nitrogen, Phosphorus, and Potassium values.
- Fertilizer recommendation in farmer language (e.g., "Give more nitrogen using UREA or manure" if low nitrogen).
- Advice on compost/manure for soil health.

Temperature & Rain
- Comment on whether the temperature is good for the crop.
- Comment on rainfall amount, drainage needs, or irrigation.

Soil pH
- Say if pH is good for the crop or needs changing.

Fighting pests & diseases
- Warn about likely pests/diseases based on humidity and climate zone.
- Give simple prevention tips.

Planting tips
- Advice on site selection, spacing, and crop rotation.
- Any other best practices.

Other crops that can grow well here
- List other crops that match the soil and climate.

Now write the farmer advice in the exact style and tone shown in the example."""

        return prompt
    
    def _get_fallback_advice(self, request: AgriculturalAdviceRequest) -> str:
        """Provide basic fallback advice when LLM is unavailable"""
        return f"""Your soil and weather are PERFECT for growing {request.crop_name}! Here's how to get the best results:

Fertilizer use
- Your soil has nitrogen: {request.nitrogen:.1f}, phosphorus: {request.phosphorus:.1f}, potassium: {request.potassium:.1f}
- Add compost or manure to improve soil health
- Consider balanced fertilizer for better growth

Temperature & Rain
- Temperature is {request.temperature:.1f}°C - {"good" if 15 <= request.temperature <= 35 else "may need attention"}
- Rainfall is {request.rainfall:.1f}mm - {"adequate" if request.rainfall > 50 else "may need irrigation"}

Soil pH
- Your soil pH is {request.ph_level:.2f} - {"good for most crops" if 6.0 <= request.ph_level <= 7.5 else "may need adjustment"}

Planting tips
- Choose a sunny location with good drainage
- Follow proper spacing for your crop
- Consider crop rotation for soil health

Note: Detailed agricultural advice is currently unavailable. Please consult with local agricultural extension services for specific recommendations."""
    
    def is_available(self) -> bool:
        """Check if the agricultural advisor is available"""
        return self.client is not None

# Example usage
if __name__ == "__main__":
    print("🌾 Testing Agricultural Advisor")
    print("=" * 40)
    
    # Create test request
    test_request = AgriculturalAdviceRequest(
        crop_name="Rice",
        suitability_confidence=85.5,
        nitrogen=45.2,
        phosphorus=38.7,
        potassium=42.1,
        temperature=28.5,
        humidity=75.3,
        ph_level=6.2,
        rainfall=120.8,
        climate_zone="tropical",
        alternative_crops=[("Maize", 78.2), ("Banana", 72.1), ("Coconut", 68.9)]
    )
    
    # Initialize advisor
    advisor = AgriculturalAdvisor()
    
    if advisor.is_available():
        print("✅ Azure OpenAI connection successful")
        
        # Get advice
        response = advisor.get_farmer_advice(test_request)
        
        if response.success:
            print(f"✅ Advice generated in {response.processing_time_ms:.2f}ms")
            print("\n" + "="*60)
            print("FARMER ADVICE:")
            print("="*60)
            print(response.advice_text)
        else:
            print(f"❌ Failed to generate advice: {response.error_message}")
            print("\nFallback advice:")
            print(response.advice_text)
    else:
        print("❌ Azure OpenAI not available - check your .env configuration")
        print("Creating fallback advice...")
        
        response = advisor.get_farmer_advice(test_request)
        print(response.advice_text)
