#!/usr/bin/env python3
"""
Test script to diagnose MemMachine connectivity issues.
"""

import requests
import json
from datetime import datetime

MEMMACHINE_URL = "http://localhost:8080"

def test_health():
    """Test if MemMachine is healthy."""
    print("=" * 70)
    print("Testing MemMachine Health")
    print("=" * 70)
    
    try:
        response = requests.get(f"{MEMMACHINE_URL}/v1/health", timeout=5)
        print(f"\n✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Service: {data.get('service')}")
            print(f"✓ Version: {data.get('version')}")
            print(f"✓ Status: {data.get('status')}")
            
            mm = data.get('memory_managers', {})
            print(f"\nMemory Managers:")
            print(f"  - Profile Memory: {mm.get('profile_memory')}")
            print(f"  - Episodic Memory: {mm.get('episodic_memory')}")
            
            return True
        else:
            print(f"✗ Health check failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to MemMachine: {e}")
        print(f"\nMake sure MemMachine is running at: {MEMMACHINE_URL}")
        return False


def test_add_memory():
    """Test adding a memory."""
    print("\n" + "=" * 70)
    print("Testing Add Memory")
    print("=" * 70)
    
    test_data = {
        "session": {
            "user_id": ["test_user"],
            "session_id": "test_session_001",
            "agent_id": ["test_assistant"],
            "group_id": None
        },
        "producer": "test_user",
        "produced_for": "test_assistant",
        "episode_content": "This is a test message",
        "episode_type": "dialog",
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "speaker": "test_user"
        }
    }
    
    print(f"\nSending POST to: {MEMMACHINE_URL}/v1/memories")
    print(f"Payload:")
    print(json.dumps(test_data, indent=2))
    print()
    
    try:
        response = requests.post(
            f"{MEMMACHINE_URL}/v1/memories",
            json=test_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("\n✓ Memory added successfully!")
            return True
        else:
            print(f"\n✗ Failed to add memory")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Request failed: {e}")
        return False


def test_search_memory():
    """Test searching memories."""
    print("\n" + "=" * 70)
    print("Testing Search Memory")
    print("=" * 70)
    
    search_data = {
        "session": {
            "user_id": ["test_user"],
            "session_id": "test_session_001",
            "agent_id": ["test_assistant"],
            "group_id": None
        },
        "query": "test message",
        "limit": 5
    }
    
    print(f"\nSending POST to: {MEMMACHINE_URL}/v1/memories/search")
    print(f"Payload:")
    print(json.dumps(search_data, indent=2))
    print()
    
    try:
        response = requests.post(
            f"{MEMMACHINE_URL}/v1/memories/search",
            json=search_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text[:500]}...")  # First 500 chars
        
        if response.status_code == 200:
            print("\n✓ Search successful!")
            return True
        else:
            print(f"\n✗ Search failed")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Request failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "MemMachine Diagnostic Tool" + " " * 22 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    results = {
        "Health Check": test_health(),
        "Add Memory": test_add_memory(),
        "Search Memory": test_search_memory()
    }
    
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:.<50} {status}")
    
    all_passed = all(results.values())
    
    print()
    if all_passed:
        print("🎉 All tests passed! MemMachine is working correctly.")
    else:
        print("⚠️  Some tests failed. See errors above for details.")
        print("\nTroubleshooting:")
        print("1. Check MemMachine logs for errors")
        print("2. Verify database connections (graph DB, SQL)")
        print("3. Check configuration.yml settings")
        print("4. Restart MemMachine if needed")
    
    print()


if __name__ == "__main__":
    main()

