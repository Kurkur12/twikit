import requests
from apscheduler.schedulers.background import BackgroundScheduler
from config import SEARCH_URL

hit_counter = 0

def auto_hit():
    global hit_counter
    hit_counter += 1

    print(f"\n🔥 Auto Hit #{hit_counter}")

    body = [
        {"password": "1q2w3e4r5T.", "query": "produktivitas pertanian lang:id", "username": "@Fake01Proj68697"},
        {"password": "1q2w3e4r5T.", "query": "produktivitas pertanian lang:id", "username": "@PFake0281129"},
        {"password": "1q2w3e4r5T.", "query": "produktivitas pertanian lang:id", "username": "@PFake0379178"}
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
