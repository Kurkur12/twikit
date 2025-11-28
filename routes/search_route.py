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
    summary = {
        "total": len(body),
        "success": 0,
        "failed": 0,
        "error_details": {}
    }

    for item in body:
        query = item.get("query")
        username = item.get("username")
        password = item.get("password")

        if not (query and username and password):
            results.append({"status": 400, "message": "query, username, password required"})
            summary["failed"] += 1
            summary["error_details"]["validation_error"] = summary["error_details"].get("validation_error", 0) + 1
            continue

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(search_tweets(query, username, password))
            loop.close()

            if "error" in result:
                is_rate_limit = result.get("is_rate_limit")
                status_code = 429 if is_rate_limit else 500
                error_type = "rate_limit" if is_rate_limit else "execution_error"
                
                results.append({
                    "status": status_code,
                    "akun_username": username,
                    "status_akun": "inactive",
                    "error": result["error"]
                })
                summary["failed"] += 1
                summary["error_details"][error_type] = summary["error_details"].get(error_type, 0) + 1
            else:
                results.append({
                    "status": 200,
                    "akun_username": username,
                    "status_akun": "active",
                    "data": result
                })
                summary["success"] += 1

        except Exception as e:
            results.append({"status": 500, "username": username, "error": str(e)})
            summary["failed"] += 1
            summary["error_details"]["unhandled_exception"] = summary["error_details"].get("unhandled_exception", 0) + 1

    return jsonify({
        "summary": summary,
        "results": results
    })
