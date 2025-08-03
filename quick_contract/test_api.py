#!/usr/bin/env python3
"""
Simple test script to test the contract creation API
"""
import requests
import json

# Test data
test_contract = {
    "contract_type": "Test Agreement",
    "party_a": {
        "name": "John Doe",
        "email": "",  # Empty email to test the fix
        "address": "123 Main St"
    },
    "party_b": {
        "name": "Jane Smith", 
        "email": "",  # Empty email to test the fix
        "address": "456 Oak Ave"
    },
    "terms": "This is a test contract with all required fields for validation.",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "additional_clauses": ["Test clause 1", "Test clause 2"],
    "recipient_email": ""  # Empty email to test the fix
}

def test_json_request():
    """Test JSON request without signature"""
    print("Testing JSON request...")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/contracts",
            json=test_contract,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ JSON request successful!")
            result = response.json()
            print(f"Contract ID: {result.get('contract_id')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_json_with_signature():
    """Test JSON request with base64 signature"""
    print("\nTesting JSON request with signature...")
    # Simple test signature (small red square)
    test_signature = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    contract_with_signature = test_contract.copy()
    contract_with_signature["signature_base64"] = test_signature
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/contracts",
            json=contract_with_signature,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ JSON request with signature successful!")
            result = response.json()
            print(f"Contract ID: {result.get('contract_id')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_health():
    """Test if server is running"""
    print("Testing server health...")
    try:
        response = requests.get("http://localhost:8000/docs")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
        else:
            print(f"❌ Server not responding properly: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Contract Creation API ===")
    
    if test_health():
        test_json_request()
        test_json_with_signature()
    else:
        print("❌ Server is not running. Please start the FastAPI server first.")
        print("Run: python main.py")