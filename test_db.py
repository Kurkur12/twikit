# test_db.py
import mysql.connector

def test_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # atau user lain
            password=''   # password MySQL Anda
        )
        print("✅ Koneksi berhasil!")
        
        # Cek database
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("📊 Databases yang tersedia:")
        for db in databases:
            print(f" - {db[0]}")
            
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()