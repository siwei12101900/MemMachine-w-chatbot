#!/usr/bin/env python3
"""
Quick test to verify the group_id fix for profile memory bug.
Tests if setting group_id to a string (instead of None) fixes the 500 error.
"""

import requests
import json
from datetime import datetime

def test_group_id_fix():
    """Test the fixed group_id parameter."""
    
    print("=" * 70)
    print(" Testing group_id Fix for Profile Memory Bug")
    print("=" * 70)
    print()
    
    base_url = "http://localhost:8080"
    user_id = "test_user"
    agent_id = "test_agent"
    session_id = f"session_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # OLD WAY (caused 500 errors)
    print("❌ OLD WAY (group_id: None):")
    old_session = {
        "user_id": [user_id],
        "session_id": session_id + "_old",
        "agent_id": [agent_id],
        "group_id": None  # This was causing issues!
    }
    print(f"   {json.dumps(old_session, indent=2)}")
    print()
    
    # NEW WAY (should fix 500 errors)
    print("✅ NEW WAY (group_id: string):")
    new_session = {
        "user_id": [user_id],  # List
        "session_id": session_id + "_new",
        "agent_id": [agent_id],  # List
        "group_id": user_id  # String, not None!
    }
    print(f"   {json.dumps(new_session, indent=2)}")
    print()
    
    # Test with new format
    print("-" * 70)
    print("Testing NEW format with /v1/memories endpoint...")
    print("-" * 70)
    
    episode_data = {
        "session": new_session,
        "producer": user_id,
        "produced_for": agent_id,
        "episode_content": "Test message with group_id fix",
        "episode_type": "dialog",
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "test": "group_id_fix"
        }
    }
    
    try:
        print(f"\n📤 POST {base_url}/v1/memories")
        response = requests.post(
            f"{base_url}/v1/memories",
            json=episode_data,
            timeout=30
        )
        
        print(f"📥 Response: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! The group_id fix works!")
            print("   Profile memory can now extract facts without 500 errors.")
        elif response.status_code == 500:
            print("❌ FAILED! Still getting 500 errors.")
            print("   The bug might be something else.")
            print(f"\n   Response: {response.text[:500]}")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("=" * 70)
    print(" Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_group_id_fix()

