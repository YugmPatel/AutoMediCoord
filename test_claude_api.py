#!/usr/bin/env python3
"""
Test Claude API connection and key validity
"""

import os
import asyncio
from dotenv import load_dotenv
from anthropic import AsyncAnthropic

load_dotenv()

async def test_claude_api():
    """Test Claude API connection"""
    
    print("=" * 70)
    print("Testing Claude API Connection")
    print("=" * 70)
    
    # Check if API key exists
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("\n❌ ANTHROPIC_API_KEY not found in .env file")
        print("\n💡 To fix:")
        print("   1. Get API key from https://console.anthropic.com/")
        print("   2. Add to .env file: ANTHROPIC_API_KEY=sk-ant-...")
        return False
    
    print(f"\n✅ API Key found: {api_key[:20]}...{api_key[-10:]}")
    
    # Test API connection
    print("\n🧪 Testing API connection...")
    
    try:
        client = AsyncAnthropic(api_key=api_key)
        
        response = await client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Respond with just 'OK' if you can read this."
            }]
        )
        
        result = response.content[0].text
        print(f"\n✅ API Response: {result}")
        print("\n✅ Claude API is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ API Error: {str(e)}")
        print(f"\n❌ Error type: {type(e).__name__}")
        
        if "authentication" in str(e).lower() or "api_key" in str(e).lower():
            print("\n💡 API Key Issue:")
            print("   - Check if key is valid")
            print("   - Verify key has not expired")
            print("   - Get new key from https://console.anthropic.com/")
        elif "rate" in str(e).lower():
            print("\n💡 Rate Limit Issue:")
            print("   - Wait a moment and try again")
            print("   - Check your API usage limits")
        else:
            print("\n💡 Unknown Issue:")
            print("   - Check internet connection")
            print("   - Verify Anthropic API status")
        
        return False


if __name__ == "__main__":
    print("\nTesting Claude API...\n")
    
    try:
        success = asyncio.run(test_claude_api())
        
        if success:
            print("\n" + "=" * 70)
            print("✅ All tests passed! Your Claude API is ready.")
            print("=" * 70)
            print("\n💡 You can now run:")
            print("   python simulate_patient_flow.py")
            print("   python stress_test.py")
            print("   python run_all_agents.py")
        else:
            print("\n" + "=" * 70)
            print("❌ Tests failed. Fix the issues above and try again.")
            print("=" * 70)
            
    except KeyboardInterrupt:
        print("\n\nTest interrupted.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
