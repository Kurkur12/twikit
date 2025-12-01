"""
Test script untuk Cookie Decode API
Pastikan server Flask sudah running di localhost:7777
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:7777"

def test_decode_with_file_only():
    """Test 1: Upload file JSON tanpa username parameter"""
    print("\n=== Test 1: Upload file tanpa username ===")
    
    url = f"{BASE_URL}/decode"
    
    try:
        with open('x.com_cookies.json', 'rb') as f:
            files = [
                ('file', ('x.com_cookies.json', f, 'application/json'))
            ]
            
            response = requests.post(url, files=files)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 200:
                print("✓ Test PASSED")
            else:
                print("✗ Test FAILED")
                
    except FileNotFoundError:
        print("✗ File x.com_cookies.json tidak ditemukan")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_decode_with_username():
    """Test 2: Upload file JSON dengan username parameter"""
    print("\n=== Test 2: Upload file dengan username ===")
    
    url = f"{BASE_URL}/decode"
    
    try:
        with open('x.com_cookies.json', 'rb') as f:
            files = [
                ('file', ('x.com_cookies.json', f, 'application/json'))
            ]
            data = {
                'username': '@TestUser123'
            }
            
            response = requests.post(url, files=files, data=data)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 200:
                result = response.json()
                if 'TestUser123' in result.get('output_file', ''):
                    print("✓ Test PASSED - Username correctly used in filename")
                else:
                    print("✗ Test FAILED - Username not in filename")
            else:
                print("✗ Test FAILED")
                
    except FileNotFoundError:
        print("✗ File x.com_cookies.json tidak ditemukan")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_decode_invalid_file():
    """Test 3: Upload file non-JSON (should fail)"""
    print("\n=== Test 3: Upload file non-JSON (expected to fail) ===")
    
    url = f"{BASE_URL}/decode"
    
    try:
        # Create temporary text file
        with open('test_invalid.txt', 'w') as f:
            f.write("This is not a JSON file")
        
        with open('test_invalid.txt', 'rb') as f:
            files = [
                ('file', ('test_invalid.txt', f, 'text/plain'))
            ]
            
            response = requests.post(url, files=files)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 400:
                print("✓ Test PASSED - Correctly rejected non-JSON file")
            else:
                print("✗ Test FAILED - Should return 400 for non-JSON file")
                
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    finally:
        # Cleanup
        import os
        if os.path.exists('test_invalid.txt'):
            os.remove('test_invalid.txt')

def test_decode_no_file():
    """Test 4: Request tanpa file (should fail)"""
    print("\n=== Test 4: Request tanpa file (expected to fail) ===")
    
    url = f"{BASE_URL}/decode"
    
    try:
        response = requests.post(url)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("✓ Test PASSED - Correctly rejected request without file")
        else:
            print("✗ Test FAILED - Should return 400 for missing file")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_server_running():
    """Test 0: Cek apakah server running"""
    print("\n=== Test 0: Checking server status ===")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print("✓ Server is running")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Server is NOT running. Please start the Flask server first.")
        print("Run: python main.py")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Cookie Decode API - Test Suite")
    print("=" * 60)
    
    # Check server first
    if not test_server_running():
        print("\nPlease start the server and try again.")
        exit(1)
    
    # Run all tests
    test_decode_with_file_only()
    test_decode_with_username()
    test_decode_invalid_file()
    test_decode_no_file()
    
    print("\n" + "=" * 60)
    print("Test Suite Completed")
    print("=" * 60)
