#!/usr/bin/env python3
"""
Test WhatsApp notifications directly with Twilio
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_twilio_whatsapp():
    """Test Twilio WhatsApp integration directly"""
    
    # Get credentials
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    
    print("🔧 Testing Twilio WhatsApp Integration")
    print("=" * 50)
    print(f"Account SID: {account_sid[:10]}..." if account_sid else "❌ Not found")
    print(f"Auth Token: {auth_token[:10]}..." if auth_token else "❌ Not found")
    print()
    
    if not account_sid or not auth_token:
        print("❌ Twilio credentials not found in .env file")
        return
    
    try:
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        
        # Test phone numbers
        test_numbers = ["+14082109942", "+16693409734"]
        
        print("📱 Testing WhatsApp messages...")
        print()
        
        for i, phone_number in enumerate(test_numbers, 1):
            try:
                print(f"Sending test message {i}/2 to {phone_number}...")
                
                message = client.messages.create(
                    from_='whatsapp:+14155238886',  # Twilio sandbox number
                    body=f"🧪 EDFlow AI Test Message\n\nThis is a test notification from your emergency department coordination system.\n\nTime: {os.popen('date').read().strip()}\n\nIf you receive this, WhatsApp notifications are working!",
                    to=f'whatsapp:{phone_number}'
                )
                
                print(f"✅ Message sent successfully!")
                print(f"   Message SID: {message.sid}")
                print(f"   Status: {message.status}")
                print(f"   To: {phone_number}")
                print()
                
            except Exception as e:
                print(f"❌ Failed to send to {phone_number}")
                print(f"   Error: {str(e)}")
                print()
                
                # Check if it's a sandbox error
                if "not a valid WhatsApp number" in str(e):
                    print(f"💡 Solution: {phone_number} needs to join Twilio sandbox")
                    print(f"   Send 'join <sandbox-code>' to +1 415 523 8886")
                elif "Authenticate" in str(e):
                    print("💡 Solution: Check your Twilio credentials")
                print()
        
        print("🔍 Troubleshooting Tips:")
        print("1. Both phone numbers must join Twilio sandbox")
        print("2. Send 'join <code>' to +1 415 523 8886 from each phone")
        print("3. Check Twilio console for sandbox participants")
        print("4. Verify phone numbers have WhatsApp installed")
        print()
        
    except ImportError:
        print("❌ Twilio library not installed")
        print("Run: pip install twilio")
    except Exception as e:
        print(f"❌ Twilio connection failed: {str(e)}")

if __name__ == "__main__":
    test_twilio_whatsapp()