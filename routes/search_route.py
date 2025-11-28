from flask import Blueprint, request, jsonify
import asyncio
from services.twitter_service import search_tweets

search_bp = Blueprint("search", __name__)

@search_bp.route("/search", methods=["POST"])
def search():
    body = request.json

    if isinstance(body, dict):
        body = [body]

    results = []

    for item in body:
        query = item.get("query")
        username = item.get("username")
        password = item.get("password")

        if not (query and username and password):
            results.append({"status": 400, "message": "query, username, password required"})
            continue

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(search_tweets(query, username, password))
            loop.close()

            if "error" in result:
                results.append({
                    "status": 500,
                    "akun_username": username,
                    "status_akun": "inactive",
                    "error": result["error"]
                })
            else:
                results.append({
                    "status": 200,
                    "akun_username": username,
                    "status_akun": "active",
                    "data": result
                })

        except Exception as e:
            results.append({"status": 500, "username": username, "error": str(e)})

    return jsonify(results)
