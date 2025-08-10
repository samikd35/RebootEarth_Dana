#!/usr/bin/env python3
"""
Demo script for SMS Admin Panel and Farmer Management
Tests the complete SMS sharing functionality for agricultural advice
"""

import sys
import os
import json
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from features.sms_service import sms_service, farmer_manager, FarmerContact, SMSRequest

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_farmer_management():
    """Demonstrate farmer contact management"""
    print_header("🧑‍🌾 FARMER CONTACT MANAGEMENT DEMO")
    
    # Test adding farmers
    print_section("Adding Sample Farmers")
    
    sample_farmers = [
        FarmerContact(
            name="Tesfa Bekele",
            phone_number="+251966123456",
            location="Hawassa",
            latitude=7.0469,
            longitude=38.4762,
            preferred_language="amharic"
        ),
        FarmerContact(
            name="Meron Haile",
            phone_number="+251977234567",
            location="Hawassa",
            latitude=7.0500,
            longitude=38.4800,
            preferred_language="english"
        ),
        FarmerContact(
            name="Diriba Gutema",
            phone_number="+251988345678",
            location="Adama",
            latitude=8.5400,
            longitude=39.2675,
            preferred_language="afaan_oromo"
        )
    ]
    
    for farmer in sample_farmers:
        success = farmer_manager.add_farmer(farmer)
        status = "✅ Added" if success else "❌ Failed"
        print(f"{status}: {farmer.name} ({farmer.location}) - {farmer.phone_number}")
    
    # Display all farmers by location
    print_section("Current Farmers by Location")
    all_farmers = farmer_manager.get_all_farmers()
    
    for location, farmers in all_farmers.items():
        print(f"\n📍 {location} ({len(farmers)} farmers):")
        for farmer in farmers:
            lang_emoji = {
                'english': '🇺🇸',
                'amharic': '🇪🇹',
                'afaan_oromo': '🟢'
            }.get(farmer.preferred_language, '❓')
            
            print(f"  • {farmer.name} - {farmer.phone_number} {lang_emoji}")
    
    # Get locations list
    print_section("Available Locations")
    locations = farmer_manager.get_all_locations()
    print(f"Locations: {', '.join(locations)}")
    
    return all_farmers

def demo_sms_service():
    """Demonstrate SMS service functionality"""
    print_header("📱 SMS SERVICE DEMO")
    
    # Check SMS service availability
    print_section("SMS Service Status")
    is_available = sms_service.is_available()
    print(f"SMS Service Available: {'✅ Yes' if is_available else '❌ No'}")
    
    if not is_available:
        print("⚠️  SMS service not available. Check Twilio credentials in .env file:")
        print("   - ACCOUNT_SID")
        print("   - AUTH_TOKEN") 
        print("   - TWILIO_PHONE_NUMBER")
        return
    
    # Test SMS sending (with mock advice)
    print_section("Testing SMS Sending")
    
    sample_advice = {
        'english': """🌾 Agricultural Advice for Your Location

Based on current conditions, we recommend:
• Plant maize and teff this season
• Apply organic fertilizer before planting
• Monitor soil moisture levels
• Expect good yields with proper care

Best regards,
AlphaEarth Agricultural Advisory""",
        
        'amharic': """🌾 የእርሻ ምክር ለእርስዎ አካባቢ

በአሁኑ ሁኔታ መሰረት የምንመክረው:
• በዚህ ወቅት በቆሎ እና ጤፍ ይዝራ
• ከመዝራት በፊት የተፈጥሮ ማዳበሪያ ይተግብሩ
• የአፈር እርጥበት ይከታተሉ
• በትክክለኛ እንክብካቤ ጥሩ ምርት ይጠብቁ

ከሰላምታ ጋር,
አልፋኤርዝ የእርሻ አማካሪ""",
        
        'afaan_oromo': """🌾 Gorsa Qonnaa Naannoo Keessaniif

Haala ammaa irratti hundaa'uun gorsa kenninu:
• Yeroo kana boqqolloo fi xaafii facaasaa
• Osoo hin facaasin dura xurii uumamaa fayyadamaa
• Jiidha biyyee hordofaa
• Kunuunsa sirrii taasifameen oomisha gaarii eegaa

Nagaan,
AlphaEarth Gorsaa Qonnaa"""
    }
    
    # Get farmers from a location for testing
    test_location = "Hawassa"
    farmers = farmer_manager.get_farmers_by_location(test_location)
    
    if not farmers:
        print(f"❌ No farmers found in {test_location} for SMS testing")
        return
    
    print(f"📍 Testing SMS to {len(farmers)} farmers in {test_location}")
    
    # Send test SMS to each farmer in their preferred language
    for farmer in farmers:
        print(f"\n👤 Sending to {farmer.name} ({farmer.preferred_language})...")
        
        advice_text = sample_advice.get(farmer.preferred_language, sample_advice['english'])
        
        sms_request = SMSRequest(
            phone_number=farmer.phone_number,
            message=advice_text,
            language=farmer.preferred_language,
            location=test_location
        )
        
        # Note: This will actually send SMS if Twilio is configured
        # For demo purposes, you might want to comment this out
        # sms_response = sms_service.send_agricultural_advice(sms_request)
        
        # Simulated response for demo
        print(f"   📱 SMS prepared for {farmer.phone_number}")
        print(f"   🌐 Language: {farmer.preferred_language}")
        print(f"   📝 Message length: {len(advice_text)} characters")
        
        # Uncomment below to actually send SMS:
        # if sms_response.success:
        #     print(f"   ✅ SMS sent successfully! SID: {sms_response.message_sid}")
        # else:
        #     print(f"   ❌ SMS failed: {sms_response.error_message}")

def demo_web_api_integration():
    """Demonstrate web API integration"""
    print_header("🌐 WEB API INTEGRATION DEMO")
    
    print_section("Available API Endpoints")
    endpoints = [
        "GET  /admin                    - Admin panel for farmer management",
        "POST /admin/add-farmer        - Add new farmer contact",
        "POST /admin/remove-farmer     - Remove farmer contact",
        "GET  /api/get-locations       - Get all farmer locations",
        "GET  /api/get-farmers-by-location/<location> - Get farmers by location",
        "POST /api/send-advice-sms     - Send advice via SMS to farmers"
    ]
    
    for endpoint in endpoints:
        print(f"  {endpoint}")
    
    print_section("Sample API Usage")
    print("1. Get all locations:")
    print("   curl http://localhost:5000/api/get-locations")
    
    print("\n2. Get farmers in Addis Ababa:")
    print("   curl http://localhost:5000/api/get-farmers-by-location/Addis%20Ababa")
    
    print("\n3. Send SMS advice:")
    print("""   curl -X POST http://localhost:5000/api/send-advice-sms \\
     -H "Content-Type: application/json" \\
     -d '{
       "location": "Addis Ababa",
       "language": "auto",
       "advice_text": "Plant maize this season for best results."
     }'""")

def main():
    """Main demo function"""
    print("🌾 AlphaEarth SMS Admin Panel Demo")
    print("=" * 50)
    
    try:
        # Demo farmer management
        farmers_data = demo_farmer_management()
        
        # Demo SMS service
        demo_sms_service()
        
        # Demo web API integration
        demo_web_api_integration()
        
        print_header("✅ DEMO COMPLETE")
        print("\n🚀 Next Steps:")
        print("1. Start the Flask app: python src/web/app_ultra_integrated.py")
        print("2. Visit http://localhost:5000 for the main app")
        print("3. Visit http://localhost:5000/admin for farmer management")
        print("4. Configure Twilio credentials in .env file for SMS functionality")
        print("\n📋 Required Environment Variables:")
        print("   - ACCOUNT_SID (Twilio)")
        print("   - AUTH_TOKEN (Twilio)")
        print("   - TWILIO_PHONE_NUMBER")
        print("   - AZURE_OPENAI_ENDPOINT")
        print("   - AZURE_OPENAI_API_KEY")
        print("   - AZURE_OPENAI_DEPLOYMENT_NAME")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
