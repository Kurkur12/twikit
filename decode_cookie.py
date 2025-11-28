import json

# Baca file JSON
with open('x.com_cookies.json', 'r') as f:
    data = json.load(f)

# Daftar field yang ingin dihapus (jika ingin bersih-bersih dulu)
fields_to_remove = [
    "domain", "expirationDate", "hostOnly", "httpOnly",
    "path", "sameSite", "secure", "session", "storeId"
]

# Bersihkan dan ambil hanya name dan value
result = {
    item["name"]: item["value"]
    for item in data
    if "name" in item and "value" in item
}

# Simpan hasil ke file baru
with open('medan_master_clean.json', 'w') as f:
    json.dump(result, f, indent=4)

# Tampilkan output juga di terminal (opsional)
print(json.dumps(result, indent=4))

