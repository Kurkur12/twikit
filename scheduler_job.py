import requests
import random
from apscheduler.schedulers.background import BackgroundScheduler
from config import SEARCH_URL, db_config
from utils.database import get_connection
from utils.account_manager import get_active_account, check_username_exists

hit_counter = 0

def get_random_keyword(db_config):
    """Fetch a random active keyword from database"""
    conn = None
    cursor = None
    keyword = None
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor(dictionary=True)
        # Get random active keyword
        cursor.execute("SELECT keyword FROM keywords WHERE status='active' ORDER BY RAND() LIMIT 1")
        result = cursor.fetchone()
        if result:
            keyword = result['keyword']
    except Exception as e:
        print(f"Error fetching keyword: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    return keyword

def auto_hit():
    global hit_counter
    hit_counter += 1
    print(f"\n🔥 [Scheduler] Auto Hit #{hit_counter} Started...")

    # 1. Get Active Account
    account = get_active_account(db_config)
    if not account:
        print("⚠️ [Scheduler] Skipped: No active accounts available.")
        return

    # 2. Get Dynamic Keyword
    keyword = get_random_keyword(db_config)
    if not keyword:
        # Fallback if DB is empty
        print("⚠️ [Scheduler] No keywords in DB, using fallback.")
        keyword = "teknologi pertanian lang:id" 

    print(f"   👤 Account: {account['name']}")
    print(f"   🔍 Keyword: {keyword}")

    # 3. Validate Username in DB
    if not check_username_exists(db_config, account['name']):
        print(f"   ❌ Validation Failed: Username '{account['name']}' not found in DB.")
        return

    # 4. Prepare Payload
    body = [{
        "username": account['name'],
        "password": account['password'],
        "query": keyword
    }]

    # 5. Execute Request
    try:
        res = requests.post(SEARCH_URL, json=body, timeout=30)
        if res.status_code == 200:
            data = res.json()
            success = data.get('summary', {}).get('success', 0)
            failed = data.get('summary', {}).get('failed', 0)
            print(f"   ✅ Result: {success} Success, {failed} Failed")
        else:
            print(f"   ❌ HTTP Error: {res.status_code}")
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Randomize interval slightly to avoid pattern detection (20-30s)
    scheduler.add_job(auto_hit, "interval", seconds=25, jitter=5)
    scheduler.start()
    print("🚀 [Scheduler] Service Started (Interval: ~25s)")
