import time
import json
import requests
from utils.database import get_connection
from config import db_config, SEARCH_URL

def run_monitoring():
    conn = get_connection(db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, PASSWORD FROM DATA_LOGIN")
    users = cursor.fetchall()

    all_results = []

    for i, user in enumerate(users, 1):
        payload = {
            "query": "prabowo",
            "username": user["name"],
            "password": user["PASSWORD"]
        }

        try:
            res = requests.post(SEARCH_URL, json=payload, timeout=(3, 15))

            if res.status_code == 200:
                status = 1
            else:
                status = 0

            up = conn.cursor()
            up.execute("UPDATE DATA_LOGIN SET valid=%s WHERE name=%s", (status, user["name"]))
            conn.commit()
            up.close()

            all_results.append(res.json())

        except Exception as e:
            all_results.append({"name": user["name"], "error": str(e)})

        if i < len(users):
            time.sleep(0.3)

    cursor.close()
    conn.close()

    return all_results
