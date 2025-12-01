# Twitter Scraping API - Simple Guide

API untuk scraping Twitter dengan fitur decode cookie otomatis, monitoring, dan database integration.

---

## 🚀 Quick Start (5 Menit)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database (Optional)
```bash
# Update config.py dengan MySQL credentials
# Jalankan schema.sql untuk create tables
```

### 3. Run Server
```bash
python main.py
```

Server running di: `http://localhost:7777`

---

## 📡 API Endpoints

### 1️⃣ Decode Cookie (Upload Cookie dari Browser)

**Untuk apa?** Convert cookie dari browser extension jadi format yang bisa dipakai untuk scraping.

**Endpoint:** `POST /decode`

**Cara pakai:**

#### Python
```python
import requests

with open('x.com_cookies.json', 'rb') as f:
    files = [('file', ('x.com_cookies.json', f, 'application/json'))]
    data = {'username': '@MyAccount'}  # optional
    response = requests.post('http://localhost:7777/decode', files=files, data=data)
    print(response.json())
```

#### cURL
```bash
curl -X POST http://localhost:7777/decode \
  -F "file=@x.com_cookies.json" \
  -F "username=@MyAccount"
```

#### Postman
1. Method: `POST`
2. URL: `http://localhost:7777/decode`
3. Body → `form-data`:
   - `file` (File): pilih `x.com_cookies.json`
   - `username` (Text): `@MyAccount` (optional)
4. Send

**Response:**
```json
{
  "status": "success",
  "message": "Cookie decoded successfully",
  "username": "MyAccount",
  "output_file": "cookies_MyAccount.json",
  "cookies_count": 15
}
```

**Output:** File `cookies_MyAccount.json` siap dipakai untuk scraping.

---

### 2️⃣ Search Tweets (Scraping Twitter)

**Endpoint:** `POST /search`

**Body:**
```json
{
  "query": "keyword lang:id",
  "username": "your_username",
  "password": "your_password"
}
```

**Response:** JSON dengan data tweets + summary.

---

### 3️⃣ Monitoring Dashboard

**Endpoint:** `GET /monitoring`

**Response:** Stats sistem, account health, recent logs.

---

## 🎯 Workflow Lengkap

### Step 1: Export Cookie dari Browser
1. Install extension: [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie) atau [Cookie-Editor](https://cookie-editor.cgagnier.ca/)
2. Login ke x.com (Twitter)
3. Klik extension → Export cookies as JSON
4. Save file: `x.com_cookies.json`

### Step 2: Decode Cookie
```bash
# Test dengan script
python demo_decode.py

# Atau manual dengan Python/cURL/Postman
```

### Step 3: Gunakan untuk Scraping
File `cookies_MyAccount.json` sudah siap digunakan dengan endpoint `/search`.

---

## 🧪 Testing

### Quick Test
```bash
# Demo interaktif
python demo_decode.py

# Test suite lengkap
python test_decode_api.py
```

### Postman
Import collection: `postman_collection.json`
- Buka Postman → Import → pilih file
- Langsung ada 6 request siap pakai

---

## 📂 Project Structure

```
├── main.py                    # Flask server
├── config.py                  # Configuration
├── routes/
│   ├── decode_route.py        # POST /decode
│   ├── search_route.py        # POST /search
│   └── monitoring_route.py    # GET /monitoring
├── services/
│   ├── cookie_service.py      # Cookie processing
│   ├── twitter_service.py     # Twitter scraping
│   └── monitoring_service.py  # Monitoring logic
└── utils/
    ├── database.py            # Database helpers
    └── account_manager.py     # Account management
```

---

## 🔧 Configuration

Edit `config.py`:

```python
# Database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'project'
}

# Server
API_PORT = 7777
```

---

## 📖 Documentation

### Untuk Pemula
- **Quick Start:** Baca README ini (you are here!)
- **Test API:** `python demo_decode.py`
- **Postman Guide:** [POSTMAN_GUIDE.md](POSTMAN_GUIDE.md)

### Untuk Developer
- **API Docs:** [DECODE_API_DOCS.md](DECODE_API_DOCS.md)
- **Flowcharts:** [FLOWCHART_DECODE.md](FLOWCHART_DECODE.md)
- **Cheat Sheet:** [CHEATSHEET_DECODE.md](CHEATSHEET_DECODE.md)

### Lengkap
- **Index:** [DOCS_INDEX.md](DOCS_INDEX.md) - Semua dokumentasi

---

## 💡 Common Use Cases

### Use Case 1: Decode Cookie untuk Scraping
```bash
# 1. Export cookie dari browser → x.com_cookies.json
# 2. Upload ke API
curl -X POST http://localhost:7777/decode -F "file=@x.com_cookies.json"
# 3. Dapat file cookies_username.json
# 4. Gunakan untuk scraping
```

### Use Case 2: Automated Testing
```bash
# Run test suite
python test_decode_api.py

# Semua test case otomatis
```

### Use Case 3: Integration dengan Postman
```bash
# Import collection
Postman → Import → postman_collection.json

# Langsung test semua endpoint
```

---

## 🐛 Troubleshooting

### Server tidak bisa diakses
```bash
# Pastikan server running
python main.py

# Check di browser: http://localhost:7777/
```

### Error "No file uploaded"
- Pastikan parameter `file` ada
- Di Postman: Body → form-data, TYPE harus "File"

### Error "Invalid file type"
- File harus `.json`
- Export ulang dari browser extension

### Cookie tidak valid
- Login ulang ke x.com
- Export cookie baru
- Upload ulang

---

## 🎨 Features

✅ **Cookie Decode API** - Auto-parse cookie dari browser  
✅ **Twitter Scraping** - Search tweets dengan query  
✅ **Monitoring Dashboard** - Real-time stats  
✅ **Database Integration** - Save tweets ke MySQL  
✅ **Account Management** - Auto rotation, status tracking  
✅ **Error Handling** - Handle rate limits & errors  
✅ **Scheduler** - Background automation (optional)  

---

## 📦 Requirements

```
Flask
requests
twikit
mysql-connector-python
```

Install semua: `pip install -r requirements.txt`

---

## 🚦 Quick Commands

```bash
# Start server
python main.py

# Test decode API
python demo_decode.py

# Run test suite
python test_decode_api.py

# Check output files
ls cookies_*.json
```

---

## 🔗 Important Links

| Resource | File | Description |
|----------|------|-------------|
| **Quick Test** | `demo_decode.py` | Interactive demo |
| **Postman** | `postman_collection.json` | Import ke Postman |
| **API Docs** | `DECODE_API_DOCS.md` | Full specification |
| **Cheat Sheet** | `CHEATSHEET_DECODE.md` | Quick reference |
| **Flowcharts** | `FLOWCHART_DECODE.md` | Visual diagrams |

---

## 📞 Support

**Stuck?** Check dokumentasi:
1. [POSTMAN_GUIDE.md](POSTMAN_GUIDE.md) - Cara pakai Postman
2. [QUICKSTART_DECODE.md](QUICKSTART_DECODE.md) - Tutorial lengkap
3. [DOCS_INDEX.md](DOCS_INDEX.md) - Index semua docs

**Still stuck?** Run test script:
```bash
python test_decode_api.py
```

---

## 📝 License & Credits

Project ini untuk automation Twitter scraping dengan fokus pada kemudahan penggunaan dan dokumentasi lengkap.

**Tech Stack:**
- Flask (API Server)
- Twikit (Twitter Scraping)
- MySQL (Database)
- Python 3.x

---

**🎉 Ready to use! Start dengan: `python main.py`**
