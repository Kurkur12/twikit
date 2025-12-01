from flask import Blueprint, request, jsonify
import json
from services.cookie_service import (
    validate_cookie_json,
    decode_cookie_data,
    save_decoded_cookies,
    get_cookies_count
)

decode_bp = Blueprint("decode", __name__)

@decode_bp.route("/decode", methods=["POST"])
def decode_cookie():
    """
    Endpoint untuk decode cookie dari file JSON yang di-upload.
    
    Parameters:
    - file (required): File JSON cookie
    - username (optional): Username untuk penamaan file output
    
    Returns:
    - JSON response dengan status dan informasi file output
    """
    
    # Step 1: Verifikasi file yang di-upload
    if 'file' not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded. Please upload a JSON file with key 'file'"
        }), 400
    
    file = request.files['file']
    
    # Cek apakah file ada
    if file.filename == '':
        return jsonify({
            "status": "error",
            "message": "No file selected"
        }), 400
    
    # Cek apakah file adalah JSON
    if not file.filename.endswith('.json'):
        return jsonify({
            "status": "error",
            "message": "Invalid file type. Please upload a JSON file"
        }), 400
    
    try:
        # Step 2: Parsing file cookie JSON
        file_content = file.read()
        cookie_data = json.loads(file_content)
        
        # Validasi format cookie
        if not validate_cookie_json(cookie_data):
            return jsonify({
                "status": "error",
                "message": "Invalid cookie JSON format. Expected array of objects with 'name' and 'value' fields"
            }), 400
        
        # Decode cookie data
        decoded_cookies = decode_cookie_data(cookie_data)
        
        # Get username dari request atau None
        username = request.form.get('username', None)
        
        # Step 3: Simpan hasil decode ke file
        output_file = save_decoded_cookies(decoded_cookies, username)
        
        # Step 4: Return response sukses
        cookies_count = get_cookies_count(decoded_cookies)
        
        # Extract username yang digunakan dari filename
        used_username = output_file.replace('cookies_', '').replace('.json', '')
        
        return jsonify({
            "status": "success",
            "message": "Cookie decoded successfully",
            "username": used_username,
            "output_file": output_file,
            "cookies_count": cookies_count
        }), 200
        
    except json.JSONDecodeError as e:
        return jsonify({
            "status": "error",
            "message": f"Invalid JSON format: {str(e)}"
        }), 400
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error processing file: {str(e)}"
        }), 500
