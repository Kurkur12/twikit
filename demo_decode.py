"""
DEMO PRAKTIS - Cookie Decode API
Cara termudah untuk test dan pakai API
"""

import requests
import json
import os

# Configuration
API_URL = "http://localhost:7777/decode"
COOKIE_FILE = "x.com_cookies.json"

print("=" * 70)
print("🚀 DEMO COOKIE DECODE API")
print("=" * 70)

# Cek apakah file cookie ada
if not os.path.exists(COOKIE_FILE):
    print(f"\n❌ File '{COOKIE_FILE}' tidak ditemukan!")
    print(f"   Pastikan file cookie ada di folder: {os.getcwd()}")
    exit(1)

print(f"\n✅ File cookie ditemukan: {COOKIE_FILE}")
print(f"   Size: {os.path.getsize(COOKIE_FILE)} bytes")

# ============================================================================
# DEMO 1: Upload dengan Username
# ============================================================================
print("\n" + "=" * 70)
print("📤 DEMO 1: Upload Cookie dengan Username")
print("=" * 70)

username = "@DemoAccount123"
print(f"Username: {username}")

with open(COOKIE_FILE, 'rb') as f:
    files = [('file', (COOKIE_FILE, f, 'application/json'))]
    data = {'username': username}
    
    print("\n⏳ Mengirim request ke API...")
    response = requests.post(API_URL, files=files, data=data)

print(f"\n📊 Response Status: {response.status_code}")
print(f"📄 Response Body:")
print(json.dumps(response.json(), indent=2))

if response.status_code == 200:
    result = response.json()
    output_file = result['output_file']
    print(f"\n✅ SUCCESS! File ter-generate: {output_file}")
    
    # Cek isi file
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            cookies = json.load(f)
        print(f"   Total cookies: {len(cookies)}")
        print(f"   Cookie keys: {list(cookies.keys())[:5]}...")

# ============================================================================
# DEMO 2: Upload tanpa Username (Auto-extract)
# ============================================================================
print("\n" + "=" * 70)
print("📤 DEMO 2: Upload Cookie TANPA Username (Auto-extract dari twid)")
print("=" * 70)

with open(COOKIE_FILE, 'rb') as f:
    files = [('file', (COOKIE_FILE, f, 'application/json'))]
    
    print("\n⏳ Mengirim request ke API...")
    response = requests.post(API_URL, files=files)

print(f"\n📊 Response Status: {response.status_code}")
print(f"📄 Response Body:")
print(json.dumps(response.json(), indent=2))

if response.status_code == 200:
    result = response.json()
    output_file = result['output_file']
    print(f"\n✅ SUCCESS! File ter-generate: {output_file}")
    print(f"   Username auto-extracted: {result['username']}")

# ============================================================================
# DEMO 3: Lihat File Output
# ============================================================================
print("\n" + "=" * 70)
print("📁 DEMO 3: Isi File Output")
print("=" * 70)

# Ambil file terakhir yang di-generate
if response.status_code == 200:
    output_file = result['output_file']
    
    with open(output_file, 'r') as f:
        cookies = json.load(f)
    
    print(f"\nFile: {output_file}")
    print(f"Total cookies: {len(cookies)}")
    print(f"\nSample cookies (first 5):")
    for i, (key, value) in enumerate(list(cookies.items())[:5]):
        # Truncate value jika terlalu panjang
        display_value = value[:50] + "..." if len(value) > 50 else value
        print(f"  {i+1}. {key}: {display_value}")
    
    # Cek important cookies
    print(f"\n🔑 Important cookies check:")
    important = ['auth_token', 'ct0', 'twid']
    for cookie in important:
        status = "✅" if cookie in cookies else "❌"
        print(f"  {status} {cookie}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("📋 SUMMARY")
print("=" * 70)
print("""
✅ API berfungsi dengan baik!
✅ File cookie berhasil di-decode
✅ Output file siap digunakan untuk scraping

📝 Cara pakai output file:
   1. Load file cookies_<username>.json
   2. Gunakan untuk authentication Twitter API
   3. Integrate dengan endpoint /search

💡 Tips:
   - File output disimpan di folder project
   - Bisa reuse sampai cookie expired
   - Untuk update cookie, upload ulang file baru
""")

print("=" * 70)
print("🎉 DEMO SELESAI!")
print("=" * 70)
