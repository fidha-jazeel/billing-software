"""
Test script for API Key Manager
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from travel_billing_software.utils.api_key_manager import get_api_key_manager

def test_api_key_manager():
    """Test the API Key Manager functionality."""
    print("🧪 Testing API Key Manager...")
    print("-" * 50)
    
    # Get manager instance
    manager = get_api_key_manager()
    print("✅ API Key Manager initialized")
    
    # Test 1: Set a test API key
    print("\n📝 Test 1: Setting test API key...")
    test_key = "test_key_12345_abcde"
    result = manager.set_api_key('test_service', test_key)
    if result:
        print("✅ API key saved successfully")
    else:
        print("❌ Failed to save API key")
        return False
    
    # Test 2: Retrieve the API key
    print("\n📖 Test 2: Retrieving API key...")
    retrieved_key = manager.get_api_key('test_service')
    if retrieved_key == test_key:
        print(f"✅ API key retrieved correctly: {retrieved_key[:10]}...")
    else:
        print(f"❌ API key mismatch. Expected: {test_key}, Got: {retrieved_key}")
        return False
    
    # Test 3: Check if key exists
    print("\n🔍 Test 3: Checking if key exists...")
    exists = manager.has_api_key('test_service')
    if exists:
        print("✅ API key exists check passed")
    else:
        print("❌ API key exists check failed")
        return False
    
    # Test 4: Check non-existent key
    print("\n🔍 Test 4: Checking non-existent key...")
    exists = manager.has_api_key('non_existent_service')
    if not exists:
        print("✅ Non-existent key check passed")
    else:
        print("❌ Non-existent key check failed")
        return False
    
    # Test 5: Delete the API key
    print("\n🗑️ Test 5: Deleting API key...")
    result = manager.delete_api_key('test_service')
    if result:
        print("✅ API key deleted successfully")
    else:
        print("❌ Failed to delete API key")
        return False
    
    # Test 6: Verify deletion
    print("\n🔍 Test 6: Verifying deletion...")
    retrieved_key = manager.get_api_key('test_service')
    if retrieved_key == "":
        print("✅ API key deletion verified")
    else:
        print(f"❌ API key still exists: {retrieved_key}")
        return False
    
    # Test 7: Test Google AI key (if configured)
    print("\n🤖 Test 7: Checking Google AI key...")
    google_key = manager.get_api_key('google_ai')
    if google_key:
        print(f"✅ Google AI key is configured: {google_key[:10]}...{google_key[-5:]}")
    else:
        print("⚠️ No Google AI key configured (this is okay for testing)")
    
    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    try:
        success = test_api_key_manager()
        if success:
            print("\n✅ API Key Manager is working correctly!")
        else:
            print("\n❌ Some tests failed")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
