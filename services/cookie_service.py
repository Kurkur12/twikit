import json
import os
from datetime import datetime

def validate_cookie_json(data):
    """
    Validasi apakah data adalah format cookie JSON yang valid.
    Expected format: array of objects dengan field 'name' dan 'value'
    """
    if not isinstance(data, list):
        return False
    
    if len(data) == 0:
        return False
    
    # Cek apakah setiap item memiliki field 'name' dan 'value'
    for item in data:
        if not isinstance(item, dict):
            return False
        if 'name' not in item or 'value' not in item:
            return False
    
    return True

def decode_cookie_data(cookie_data):
    """
    Decode cookie dari format array JSON menjadi key-value pairs.
    Input: array of cookie objects dengan berbagai field
    Output: dictionary dengan hanya name dan value
    """
    result = {
        item["name"]: item["value"]
        for item in cookie_data
        if "name" in item and "value" in item
    }
    
    return result

def extract_username_from_cookies(decoded_cookies):
    """
    Extract username dari cookie 'twid' jika ada.
    Format twid: "u%3D1993194878030036993"
    """
    if 'twid' in decoded_cookies:
        twid = decoded_cookies['twid']
        # Extract user ID dari twid
        if 'u%3D' in twid:
            user_id = twid.split('u%3D')[1]
            return f"user_{user_id}"
    
    # Fallback ke timestamp jika tidak ada twid
    return f"user_{int(datetime.now().timestamp())}"

def save_decoded_cookies(decoded_cookies, username=None):
    """
    Simpan hasil decode ke file cookies_<username>.json
    Returns: path file yang disimpan
    """
    if not username:
        username = extract_username_from_cookies(decoded_cookies)
    
    # Pastikan username tidak mengandung karakter yang tidak valid untuk filename
    # Remove @ jika ada di awal
    if username.startswith('@'):
        username = username[1:]
    
    # Sanitize username untuk filename
    safe_username = "".join(c for c in username if c.isalnum() or c in ('_', '-'))
    
    filename = f"cookies_{safe_username}.json"
    filepath = os.path.join(os.getcwd(), filename)
    
    # Simpan ke file
    with open(filepath, 'w') as f:
        json.dump(decoded_cookies, f, indent=4)
    
    return filename

def get_cookies_count(decoded_cookies):
    """
    Hitung jumlah cookies yang berhasil di-decode
    """
    return len(decoded_cookies)
