#!/usr/bin/env python3
"""
SMS Service for Agricultural Advice
Handles Twilio integration and farmer contact management
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)

@dataclass
class FarmerContact:
    """Farmer contact information"""
    name: str
    phone_number: str
    location: str
    latitude: float
    longitude: float
    preferred_language: str = "english"
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

@dataclass
class SMSRequest:
    """SMS sending request"""
    phone_number: str
    message: str
    language: str
    location: str

@dataclass
class SMSResponse:
    """SMS sending response"""
    success: bool
    message_sid: Optional[str] = None
    error_message: Optional[str] = None
    cost_estimate: Optional[str] = None

class SMSService:
    """
    SMS Service for sending agricultural advice to Ethiopian farmers
    Uses Twilio for SMS delivery with location-based farmer management
    """
    
    def __init__(self):
        """Initialize SMS service with Twilio credentials"""
        self.account_sid = os.getenv('ACCOUNT_SID')
        self.auth_token = os.getenv('AUTH_TOKEN')
        self.twilio_phone = os.getenv('TWILIO_PHONE_NUMBER', '+1234567890')  # Default placeholder
        
        self.client = None
        self.available = False
        
        # Initialize Twilio client
        try:
            if self.account_sid and self.auth_token:
                from twilio.rest import Client
                self.client = Client(self.account_sid, self.auth_token)
                self.available = True
                logger.info("Twilio SMS service initialized successfully")
            else:
                logger.warning("Twilio credentials not found in environment variables")
        except ImportError:
            logger.error("Twilio library not installed. Run: pip install twilio")
        except Exception as e:
            logger.error(f"Failed to initialize Twilio client: {e}")
    
    def is_available(self) -> bool:
        """Check if SMS service is available"""
        return self.available and self.client is not None
    
    def send_agricultural_advice(self, request: SMSRequest) -> SMSResponse:
        """
        Send agricultural advice via SMS to Ethiopian farmers
        
        Args:
            request: SMS request with phone number, message, language, and location
            
        Returns:
            SMSResponse with success status and message details
        """
        if not self.is_available():
            return SMSResponse(
                success=False,
                error_message="SMS service not available. Check Twilio configuration."
            )
        
        try:
            # Format message with header
            language_headers = {
                "english": "🌾 Agricultural Advice",
                "amharic": "🌾 የእርሻ ምክር",
                "afaan_oromo": "🌾 Gorsa Qonnaa"
            }
            
            header = language_headers.get(request.language, "🌾 Agricultural Advice")
            formatted_message = f"{header}\n\nLocation: {request.location}\n\n{request.message}"
            
            # Ensure Ethiopian phone number format
            phone = self._format_ethiopian_phone(request.phone_number)
            
            # Send SMS via Twilio
            message = self.client.messages.create(
                body=formatted_message,
                from_=self.twilio_phone,
                to=phone
            )
            
            logger.info(f"SMS sent successfully to {phone} (SID: {message.sid})")
            
            return SMSResponse(
                success=True,
                message_sid=message.sid,
                cost_estimate="~$0.05 USD"  # Approximate international SMS cost
            )
            
        except Exception as e:
            error_msg = f"Failed to send SMS: {str(e)}"
            logger.error(error_msg)
            
            return SMSResponse(
                success=False,
                error_message=error_msg
            )
    
    def _format_ethiopian_phone(self, phone_number: str) -> str:
        """
        Format Ethiopian phone number for international SMS
        
        Args:
            phone_number: Phone number in various formats
            
        Returns:
            Properly formatted international phone number
        """
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, phone_number))
        
        # Handle Ethiopian phone number formats
        if digits.startswith('251'):
            # Already has country code
            return f"+{digits}"
        elif digits.startswith('0'):
            # Remove leading 0 and add country code
            return f"+251{digits[1:]}"
        elif len(digits) == 9:
            # 9-digit local number, add country code
            return f"+251{digits}"
        else:
            # Return as-is with + prefix
            return f"+{digits}"

class FarmerContactManager:
    """
    Manages farmer contact database for location-based SMS sending
    """
    
    def __init__(self, data_file: str = "data/farmer_contacts.json"):
        """Initialize farmer contact manager"""
        self.data_file = data_file
        self.contacts: Dict[str, List[FarmerContact]] = {}
        self._ensure_data_directory()
        self._load_contacts()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def _load_contacts(self):
        """Load farmer contacts from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Convert dict data back to FarmerContact objects
                for location, contacts_data in data.items():
                    self.contacts[location] = [
                        FarmerContact(**contact_data) for contact_data in contacts_data
                    ]
                    
                logger.info(f"Loaded {sum(len(contacts) for contacts in self.contacts.values())} farmer contacts")
            else:
                logger.info("No existing farmer contacts file found, starting fresh")
                
        except Exception as e:
            logger.error(f"Failed to load farmer contacts: {e}")
            self.contacts = {}
    
    def _save_contacts(self):
        """Save farmer contacts to JSON file"""
        try:
            # Convert FarmerContact objects to dict for JSON serialization
            data = {}
            for location, contacts in self.contacts.items():
                data[location] = [
                    {
                        'name': contact.name,
                        'phone_number': contact.phone_number,
                        'location': contact.location,
                        'latitude': contact.latitude,
                        'longitude': contact.longitude,
                        'preferred_language': contact.preferred_language,
                        'created_at': contact.created_at
                    }
                    for contact in contacts
                ]
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info("Farmer contacts saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save farmer contacts: {e}")
    
    def add_farmer(self, farmer: FarmerContact) -> bool:
        """
        Add a new farmer contact
        
        Args:
            farmer: FarmerContact object
            
        Returns:
            True if added successfully, False otherwise
        """
        try:
            if farmer.location not in self.contacts:
                self.contacts[farmer.location] = []
            
            # Check for duplicate phone numbers in the same location
            existing_phones = [f.phone_number for f in self.contacts[farmer.location]]
            if farmer.phone_number in existing_phones:
                logger.warning(f"Farmer with phone {farmer.phone_number} already exists in {farmer.location}")
                return False
            
            self.contacts[farmer.location].append(farmer)
            self._save_contacts()
            
            logger.info(f"Added farmer {farmer.name} in {farmer.location}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add farmer: {e}")
            return False
    
    def get_farmers_by_location(self, location: str) -> List[FarmerContact]:
        """Get all farmers in a specific location"""
        return self.contacts.get(location, [])
    
    def get_all_locations(self) -> List[str]:
        """Get all available locations"""
        return list(self.contacts.keys())
    
    def get_all_farmers(self) -> Dict[str, List[FarmerContact]]:
        """Get all farmers organized by location"""
        return self.contacts
    
    def remove_farmer(self, location: str, phone_number: str) -> bool:
        """Remove a farmer by location and phone number"""
        try:
            if location in self.contacts:
                self.contacts[location] = [
                    f for f in self.contacts[location] 
                    if f.phone_number != phone_number
                ]
                
                # Remove empty locations
                if not self.contacts[location]:
                    del self.contacts[location]
                
                self._save_contacts()
                logger.info(f"Removed farmer with phone {phone_number} from {location}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to remove farmer: {e}")
            return False

# Global instances
sms_service = SMSService()
farmer_manager = FarmerContactManager()

if __name__ == "__main__":
    # Test SMS service
    print("🔧 Testing SMS Service...")
    print(f"SMS Service Available: {sms_service.is_available()}")
    
    if sms_service.is_available():
        # Test SMS (replace with actual phone number)
        test_request = SMSRequest(
            phone_number="+251911234567",  # Ethiopian test number
            message="Your soil is good for growing Teff. Use organic fertilizer and plant during rainy season.",
            language="english",
            location="Addis Ababa"
        )
        
        response = sms_service.send_agricultural_advice(test_request)
        print(f"Test SMS Result: {response.success}")
        if response.error_message:
            print(f"Error: {response.error_message}")
    
    # Test farmer manager
    print("\n🔧 Testing Farmer Contact Manager...")
    
    test_farmer = FarmerContact(
        name="Abebe Kebede",
        phone_number="+251911234567",
        location="Addis Ababa",
        latitude=9.0320,
        longitude=38.7469,
        preferred_language="amharic"
    )
    
    success = farmer_manager.add_farmer(test_farmer)
    print(f"Added test farmer: {success}")
    
    locations = farmer_manager.get_all_locations()
    print(f"Available locations: {locations}")
