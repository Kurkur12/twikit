"""
Contoh Praktis Penggunaan Cookie Decode API

Script ini menunjukkan cara menggunakan API /decode dalam workflow nyata:
1. Upload cookie file
2. Decode cookie
3. Gunakan hasil decode untuk scraping (optional)
"""

import requests
import json
import os

# Configuration
API_BASE_URL = "http://localhost:7777"
COOKIE_FILE = "x.com_cookies.json"  # File cookie dari browser extension
USERNAME = "@MyTwitterAccount"  # Username untuk penamaan file

def decode_cookie(cookie_file_path, username=None):
    """
    Upload dan decode cookie file
    
    Args:
        cookie_file_path: Path ke file cookie JSON
        username: Username untuk penamaan file output (optional)
    
    Returns:
        dict: Response dari API
    """
    url = f"{API_BASE_URL}/decode"
    
    print(f"📤 Uploading cookie file: {cookie_file_path}")
    
    try:
        with open(cookie_file_path, 'rb') as f:
            files = [
                ('file', (os.path.basename(cookie_file_path), f, 'application/json'))
            ]
            
            data = {}
            if username:
                data['username'] = username
                print(f"👤 Username: {username}")
            
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"   - Output file: {result['output_file']}")
                print(f"   - Cookies count: {result['cookies_count']}")
                print(f"   - Username: {result['username']}")
                return result
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   {response.json()}")
                return None
                
    except FileNotFoundError:
        print(f"❌ File not found: {cookie_file_path}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def verify_output_file(filename):
    """
    Verify bahwa file output ter-generate dengan benar
    
    Args:
        filename: Nama file output
    
    Returns:
        dict: Isi file cookie yang sudah di-decode
    """
    print(f"\n🔍 Verifying output file: {filename}")
    
    try:
        with open(filename, 'r') as f:
            cookies = json.load(f)
            
        print(f"✅ File exists and valid JSON")
        print(f"   - Total cookies: {len(cookies)}")
        print(f"   - Cookie keys: {', '.join(list(cookies.keys())[:5])}...")
        
        # Check important cookies
        important_cookies = ['auth_token', 'ct0', 'twid']
        for cookie_name in important_cookies:
            if cookie_name in cookies:
                print(f"   ✓ {cookie_name}: present")
            else:
                print(f"   ✗ {cookie_name}: missing")
        
        return cookies
        
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in file: {filename}")
        return None

def main():
    """
    Main workflow
    """
    print("=" * 60)
    print("Cookie Decode API - Practical Example")
    print("=" * 60)
    
    # Step 1: Decode cookie
    print("\n📋 Step 1: Decode Cookie")
    print("-" * 60)
    result = decode_cookie(COOKIE_FILE, USERNAME)
    
    if not result:
        print("\n❌ Failed to decode cookie. Exiting.")
        return
    
    # Step 2: Verify output file
    print("\n📋 Step 2: Verify Output File")
    print("-" * 60)
    output_file = result['output_file']
    cookies = verify_output_file(output_file)
    
    if not cookies:
        print("\n❌ Failed to verify output file. Exiting.")
        return
    
    # Step 3: (Optional) Use decoded cookies for scraping
    print("\n📋 Step 3: Ready for Scraping")
    print("-" * 60)
    print(f"✅ Cookie file '{output_file}' is ready to use!")
    print(f"   You can now use this file for:")
    print(f"   - Twitter scraping with /search endpoint")
    print(f"   - Session management")
    print(f"   - Automation scripts")
    
    print("\n" + "=" * 60)
    print("Workflow Completed Successfully! 🎉")
    print("=" * 60)

if __name__ == "__main__":
    main()
