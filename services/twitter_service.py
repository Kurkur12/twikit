import asyncio
from twikit import Client
from utils.tweet_mapper import get_place, mapping_tweet_data

from twikit.errors import TooManyRequests

async def search_tweets(query, username, password):
    try:
        client = Client("en-US")

        await client.login(
            auth_info_1=username,
            password=password,
            cookies_file=f"cookies_{username}.json"
        )

        tweets = await client.search_tweet(query, "Top")
        result = []

        for tweet in tweets:
            place_data = get_place(tweet.place)
            tweet_data = mapping_tweet_data(tweet)

            combined = {**tweet_data, **place_data} if place_data else tweet_data
            result.append(combined)

        return result

    except TooManyRequests as e:
        from config import db_config
        from utils.account_manager import update_account_status
        from datetime import datetime, timedelta
        
        reset_time = datetime.fromtimestamp(e.rate_limit_reset) if e.rate_limit_reset else datetime.now() + timedelta(minutes=15)
        
        update_account_status(db_config, username, "rate_limited", reset_time)
        return {"error": "Rate limit exceeded", "rate_limit_reset": e.rate_limit_reset, "is_rate_limit": True}
    except Exception as e:
        return {"error": str(e)}
