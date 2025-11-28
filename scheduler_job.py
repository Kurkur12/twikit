import requests
from apscheduler.schedulers.background import BackgroundScheduler
from config import SEARCH_URL

hit_counter = 0

def auto_hit():
    global hit_counter
    hit_counter += 1

    print(f"\n🔥 Auto Hit #{hit_counter}")

    print(f"\n🔥 Auto Hit #{hit_counter}")

    from config import db_config
    from utils.account_manager import get_active_account

    account = get_active_account(db_config)
    
    if not account:
        print("⚠️ No active accounts available!")
        return

    query = "produktivitas pertanian lang:id"
    
    body = [
        {
            "username": account['username'],
            "password": account['password'],
            "query": query
        }
    ]

    try:
        res = requests.post(SEARCH_URL, json=body)
        print(res.json())
    except Exception as e:
        print("Error:", e)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_hit, "interval", seconds=20)
    scheduler.start()
