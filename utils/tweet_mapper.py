def get_place(place):
    if place is None:
        return None
    return {
        "place_id": place.id,
        "place_type": place.place_type,
        "place_name": place.name,
        "place_full_name": place.full_name,
        "place_country": place.country,
        "place_country_code": place.country_code,
    }


def mapping_tweet_data(tweet):
    return {
        "id": tweet.id,
        "language": tweet.lang,
        "text": tweet.text,
        "created_at": tweet.created_at,
        "timestamp_ms": getattr(tweet, "timestamp", None),
        "location": getattr(tweet.place, "place", None),
        "in_reply_to_status_id": getattr(tweet, "in_reply_to", None),
        "in_reply_to_screen_name": getattr(tweet, "in_reply_to_screen_name", None),
        "retweet_count": tweet.retweet_count,
        "reply_count__s": getattr(tweet, "reply_count", 0),
        "like__s": tweet.favorite_count,
        "view_count": int(tweet.view_count) if tweet.view_count else 0,
        "quote_count": getattr(tweet, "quote_count", 0),
        "media_count": getattr(tweet, "media_count", 0),
        "hashtags": getattr(tweet, "hashtags", []),
        "url__s": f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}",

        # user data
        "user_id": tweet.user.id,
        "user_screen_name": tweet.user.screen_name,
        "user_name": tweet.user.name,
        "user_created_at": str(tweet.user.created_at),
        "user_profile_image_url": tweet.user.profile_image_url,
        "user_profile_banner_url": tweet.user.profile_banner_url,
        "user_description": tweet.user.description,
        "user_followers_count": tweet.user.followers_count,
        "user_following_count": tweet.user.following_count,
        "user_favorites_count": tweet.user.favourites_count,
        "user_listed_count": tweet.user.listed_count,
        "user_fast_followers_count": tweet.user.fast_followers_count,
        "user_normal_followers_count": tweet.user.normal_followers_count,
        "statuses_count": tweet.user.statuses_count,
        "verified__b": tweet.user.verified,

        "mention_screen_name": getattr(tweet, "user_mentions_name", []),
        "mention_name": getattr(tweet, "user_mentions_screen_name", []),
    }
